"""Main agent system using LangGraph for routing and orchestration."""
import json
from typing import TypedDict, Annotated, Sequence
from datetime import datetime
import operator
from loguru import logger
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from backend.config import settings
from backend.models import RouteDecision, QueryResponse, RetrievedDocument
from backend.guardrails import GuardrailSystem
from backend.knowledge_base import KnowledgeBase
from backend.web_search import WebSearchMCP

class AgentState(TypedDict):
    """State for the agent graph."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    question: str
    route_decision: str
    retrieved_docs: list
    web_results: list
    answer: str
    step_by_step_solution: str
    confidence_score: float
    sources: list
    guardrail_passed: bool
    query_id: str

class MathProfessorAgent:
    """Main agent orchestrating the math tutoring system."""
    
    def __init__(self):
        """Initialize the agent system."""
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.temperature,
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            max_tokens=settings.max_tokens
        )
        self.guardrails = GuardrailSystem()
        self.kb = KnowledgeBase()
        self.web_search = WebSearchMCP()
        self.graph = self._build_graph()
        
        logger.info("MathProfessorAgent initialized")

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("input_guardrail", self.input_guardrail_node)
        workflow.add_node("router", self.router_node)
        workflow.add_node("kb_retrieval", self.kb_retrieval_node)
        workflow.add_node("web_search", self.web_search_node)
        workflow.add_node("solution_generator", self.solution_generator_node)
        workflow.add_node("output_guardrail", self.output_guardrail_node)
        
        # Define edges
        workflow.set_entry_point("input_guardrail")
        
        workflow.add_conditional_edges(
            "input_guardrail",
            lambda x: "router" if x["guardrail_passed"] else END
        )
        
        workflow.add_conditional_edges(
            "router",
            lambda x: "kb_retrieval" if x["route_decision"] == "knowledge_base" else "web_search"
        )
        
        workflow.add_edge("kb_retrieval", "solution_generator")
        workflow.add_edge("web_search", "solution_generator")
        workflow.add_edge("solution_generator", "output_guardrail")
        workflow.add_edge("output_guardrail", END)
        
        return workflow.compile()
    
    async def input_guardrail_node(self, state: AgentState) -> AgentState:
        """Check input guardrails."""
        logger.info("Node: input_guardrail")
        
        result = await self.guardrails.check_input_guardrail(state["question"])
        state["guardrail_passed"] = result.passed
        
        if not result.passed:
            logger.warning(f"Input guardrail failed: {result.reason}")
            state["answer"] = f"I cannot process this question. Reason: {result.reason}"
            state["route_decision"] = RouteDecision.REJECT.value
        
        return state

    def router_node(self, state: AgentState) -> AgentState:
        """Route to knowledge base or web search."""
        logger.info("Node: router")
        
        # First try knowledge base retrieval
        docs = self.kb.search(state["question"], top_k=settings.top_k_retrieval)
        
        if docs:
            best_score = docs[0].score
            logger.info(f"KB search results: best_score={best_score:.3f}, threshold={settings.similarity_threshold}")
            for i, doc in enumerate(docs[:3]):
                logger.info(f"  {i+1}. Score: {doc.score:.3f}, Subject: {doc.subject}, Question: {doc.question[:50]}...")
        
        if docs and docs[0].score >= settings.similarity_threshold:
            logger.info(f"✓ Routing to KB (best score: {docs[0].score:.3f} >= {settings.similarity_threshold})")
            state["route_decision"] = RouteDecision.KNOWLEDGE_BASE.value
            state["retrieved_docs"] = [doc.dict() for doc in docs]
        else:
            if docs:
                logger.info(f"✗ Routing to web search (best score: {docs[0].score:.3f} < {settings.similarity_threshold})")
            else:
                logger.info("✗ Routing to web search (no KB results found)")
            state["route_decision"] = RouteDecision.WEB_SEARCH.value
        
        return state
    
    def kb_retrieval_node(self, state: AgentState) -> AgentState:
        """Retrieve from knowledge base (already done in router)."""
        logger.info("Node: kb_retrieval")
        logger.info(f"KB documents available: {len(state.get('retrieved_docs', []))}")
        # Documents already retrieved in router
        return state
    
    async def web_search_node(self, state: AgentState) -> AgentState:
        """Perform web search."""
        logger.info("Node: web_search")
        logger.info(f"Performing web search for: {state['question'][:50]}...")
        
        results = await self.web_search.search(state["question"])
        state["web_results"] = results
        state["sources"] = [r.get("url", "") for r in results]
        
        return state

    def solution_generator_node(self, state: AgentState) -> AgentState:
        """Generate step-by-step solution."""
        logger.info("Node: solution_generator")
        logger.info(f"Route decision: {state['route_decision']}")
        logger.info(f"Retrieved docs count: {len(state.get('retrieved_docs', []))}")
        logger.info(f"Web results count: {len(state.get('web_results', []))}")
        
        # Load few-shot examples
        with open(settings.data_dir / "few_shot_examples.json", 'r') as f:
            few_shot = json.load(f)
        
        # Build context based on route
        if state["route_decision"] == RouteDecision.KNOWLEDGE_BASE.value:
            context = self._build_kb_context(state["retrieved_docs"], few_shot)
        else:
            context = self._build_web_context(state["web_results"], few_shot)
        
        # Generate solution
        prompt = f"""{context}

Now solve this question with detailed step-by-step explanation:

Question: {state["question"]}

Provide:
1. A clear step-by-step solution
2. Mathematical reasoning for each step
3. Final answer in \\boxed{{}} format

Solution:"""
        
        try:
            logger.info("Calling LLM for solution generation...")
            response = self.llm.invoke([HumanMessage(content=prompt)])
            solution = response.content
            logger.info(f"LLM response received: {len(solution)} characters")
            
            # Extract final answer
            import re
            boxed_match = re.search(r'\\boxed\{([^}]+)\}', solution)
            final_answer = boxed_match.group(1) if boxed_match else "Answer not found"
            
            state["step_by_step_solution"] = solution
            state["answer"] = final_answer
            state["confidence_score"] = self._calculate_confidence(state)
            
            logger.info(f"Solution generated successfully. Answer: {final_answer}")
            
        except Exception as e:
            logger.error(f"Error in solution generation: {e}")
            state["step_by_step_solution"] = f"Error generating solution: {str(e)}"
            state["answer"] = "Error occurred"
            state["confidence_score"] = 0.0
        
        return state

    async def output_guardrail_node(self, state: AgentState) -> AgentState:
        """Check output guardrails."""
        logger.info("Node: output_guardrail")
        logger.info(f"Checking solution of length: {len(state.get('step_by_step_solution', ''))}")
        
        result = await self.guardrails.check_output_guardrail(
            state["step_by_step_solution"],
            state["question"]
        )
        
        if not result.passed:
            logger.warning(f"Output guardrail failed: {result.reason}")
            state["answer"] = "I generated a response but it didn't pass quality checks. Please rephrase your question."
            state["confidence_score"] = 0.0
        
        return state
    
    def _build_kb_context(self, docs: list, few_shot: dict) -> str:
        """Build context from knowledge base documents."""
        context = "You are a mathematical professor helping students. Here are similar problems:\n\n"
        
        for doc in docs[:2]:
            context += f"Question: {doc['question']}\n"
            context += f"Answer: {doc['gold']}\n\n"
        
        # Add few-shot example
        context += "\nExample of how to format your solution:\n\n"
        context += f"Problem: {few_shot['math']['MCQ']['problem']}\n\n"
        context += f"Solution: {few_shot['math']['MCQ']['solution']}\n\n"
        
        return context
    
    def _build_web_context(self, results: list, few_shot: dict) -> str:
        """Build context from web search results."""
        context = "You are a mathematical professor. Use these web resources:\n\n"
        context += self.web_search.format_search_results(results)
        
        # Add few-shot example
        context += "\nExample solution format:\n\n"
        context += f"Problem: {few_shot['math']['MCQ']['problem']}\n\n"
        context += f"Solution: {few_shot['math']['MCQ']['solution']}\n\n"
        
        return context

    def _calculate_confidence(self, state: AgentState) -> float:
        """Calculate confidence score for the response."""
        confidence = 0.5  # Base confidence
        
        try:
            if state["route_decision"] == RouteDecision.KNOWLEDGE_BASE.value:
                if state["retrieved_docs"]:
                    best_score = state["retrieved_docs"][0]["score"]
                    confidence = min(best_score, 0.95)
                    logger.info(f"KB confidence calculated: {confidence:.3f} from score {best_score:.3f}")
            else:
                if state["web_results"]:
                    confidence = 0.7
                else:
                    confidence = 0.3
                logger.info(f"Web search confidence: {confidence:.3f}")
            
            # Check if solution has proper structure
            if "\\boxed" in state.get("step_by_step_solution", ""):
                confidence += 0.05
                logger.info("Added 0.05 confidence for proper solution structure")
                
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            confidence = 0.5
        
        return round(confidence, 2)
    
    async def process_query(self, question: str) -> QueryResponse:
        """
        Process a user query through the agent system.
        
        Args:
            question: User's math question
            
        Returns:
            QueryResponse with answer and metadata
        """
        logger.info(f"Processing query: {question[:100]}...")
        
        # Initialize state
        initial_state = {
            "messages": [],
            "question": question,
            "route_decision": "",
            "retrieved_docs": [],
            "web_results": [],
            "answer": "",
            "step_by_step_solution": "",
            "confidence_score": 0.0,
            "sources": [],
            "guardrail_passed": True,
            "query_id": datetime.now().strftime("%Y%m%d%H%M%S%f")
        }
        
        # Run graph
        final_state = await self.graph.ainvoke(initial_state)
        
        # Build response
        response = QueryResponse(
            query_id=final_state["query_id"],
            question=question,
            answer=final_state["answer"],
            step_by_step_solution=final_state["step_by_step_solution"],
            route_used=final_state["route_decision"],
            retrieved_docs=[RetrievedDocument(**doc) for doc in final_state.get("retrieved_docs", [])],
            confidence_score=final_state["confidence_score"],
            sources=final_state.get("sources"),
            timestamp=datetime.now().isoformat()
        )
        
        return response
