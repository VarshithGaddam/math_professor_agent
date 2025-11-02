# Math Professor Agent - Demo Video Script

## Video Information
- **Duration**: 7-10 minutes
- **Target Audience**: Technical evaluators, educators, developers
- **Format**: Screen recording with voiceover
- **Resolution**: 1920x1080 (Full HD)

---

## Video Structure & Timeline

### **INTRO SECTION (0:00 - 1:00)**

#### **Opening Slide (0:00 - 0:15)**
**[SCREEN: Title slide with project logo]**

**SCRIPT:**
"Welcome to the Math Professor Agent demonstration. I'm presenting a complete Agentic-RAG system that replicates a mathematical professor, providing step-by-step solutions through intelligent routing between a knowledge base and web search, with AI guardrails and human-in-the-loop feedback."

#### **Architecture Overview (0:15 - 1:00)**
**[SCREEN: Architecture diagram from docs/ARCHITECTURE.md]**

**SCRIPT:**
"Let me show you the system architecture. The Math Professor Agent uses a 6-node LangGraph workflow: Input Guardrails filter inappropriate content, the Router decides between Knowledge Base or Web Search, Solution Generator creates step-by-step explanations, and Output Guardrails ensure quality. The system includes 515 JEE Advanced questions in Qdrant vector database, Tavily web search via MCP, and DSPy optimization for continuous learning."

---

### **LIVE DEMO SECTION (1:00 - 5:00)**

#### **System Startup (1:00 - 1:30)**
**[SCREEN: Terminal showing system startup]**

**SCRIPT:**
"Let's start the system. First, I'll launch Qdrant vector database, then start the FastAPI backend, and finally the React frontend."

**ACTIONS:**
1. Open terminal
2. Run: `docker run -d -p 6333:6333 qdrant/qdrant`
3. Run: `uvicorn backend.main:app --reload --port 8000`
4. Open new terminal
5. Run: `cd frontend && npm start`
6. Show both terminals running

#### **Knowledge Base Demo (1:30 - 2:30)**
**[SCREEN: Browser showing frontend at localhost:3000]**

**SCRIPT:**
"Now let's test the knowledge base functionality. I'll ask a question about Planck's constant, which should be found in our JEE Advanced dataset."

**ACTIONS:**
1. Navigate to http://localhost:3000
2. Type: "What is Planck's constant from photoelectric effect?"
3. Click "Get Solution"
4. **HIGHLIGHT**: Show "knowledge_base" route badge
5. **HIGHLIGHT**: Show confidence score (should be 70%+)
6. **HIGHLIGHT**: Show step-by-step solution with LaTeX rendering
7. **HIGHLIGHT**: Show final boxed answer

**SCRIPT CONTINUATION:**
"Perfect! The system routed to the knowledge base with 71% confidence, found similar JEE questions, and generated a detailed 6-step solution with proper mathematical notation. Notice the LaTeX rendering for formulas and the final boxed answer."

#### **Web Search Demo (2:30 - 3:30)**
**[SCREEN: Same browser, new query]**

**SCRIPT:**
"Now let's test web search functionality with a question not in our knowledge base."

**ACTIONS:**
1. Clear previous question
2. Type: "Explain the Riemann Hypothesis in simple terms"
3. Click "Get Solution"
4. **HIGHLIGHT**: Show "web_search" route badge
5. **HIGHLIGHT**: Show confidence score (should be 60-80%)
6. **HIGHLIGHT**: Show web sources at bottom
7. **HIGHLIGHT**: Show educational explanation

**SCRIPT CONTINUATION:**
"Excellent! The system intelligently routed to web search, found educational sources from Wikipedia and MathWorld, and provided a clear explanation suitable for students. Notice the source attribution at the bottom."

#### **Feedback System Demo (3:30 - 4:30)**
**[SCREEN: Same browser, feedback interface]**

**SCRIPT:**
"Let's demonstrate the human-in-the-loop feedback system."

**ACTIONS:**
1. Click "Provide Feedback" button
2. **HIGHLIGHT**: Show feedback form
3. Set rating to 5 stars
4. Check "The answer is correct"
5. Type feedback: "Excellent step-by-step explanation!"
6. Click "Submit Feedback"
7. Show success message

**SCRIPT CONTINUATION:**
"The feedback system collects user ratings, correctness flags, and text comments. This data is used for DSPy optimization to continuously improve the system's responses."

#### **Guardrails Demo (4:30 - 5:00)**
**[SCREEN: Same browser, testing guardrails]**

**SCRIPT:**
"Let me demonstrate the AI guardrails by asking an inappropriate question."

**ACTIONS:**
1. Type: "How to hack into computer systems?"
2. Click "Get Solution"
3. **HIGHLIGHT**: Show rejection message
4. **HIGHLIGHT**: Show reason for rejection

**SCRIPT CONTINUATION:**
"The multi-layer guardrails correctly identified and blocked inappropriate content, ensuring the system stays focused on educational mathematics."

---

### **CODE WALKTHROUGH SECTION (5:00 - 8:00)**

#### **Backend Architecture (5:00 - 6:30)**
**[SCREEN: VS Code showing backend files]**

**SCRIPT:**
"Now let's examine the code architecture. The backend consists of 9 main modules."

**ACTIONS & HIGHLIGHTS:**

1. **Show main.py (5:00 - 5:20)**
   - **HIGHLIGHT**: FastAPI app initialization
   - **HIGHLIGHT**: API endpoints (/query, /feedback, /benchmark)
   - **HIGHLIGHT**: Component initialization

**SCRIPT:**
"Main.py is our FastAPI application with 5 key endpoints. Notice the comprehensive startup validation that checks API keys and provides helpful error messages."

2. **Show agent.py (5:20 - 5:50)**
   - **HIGHLIGHT**: LangGraph workflow definition
   - **HIGHLIGHT**: AgentState TypedDict
   - **HIGHLIGHT**: Router node logic

**SCRIPT:**
"Agent.py contains our LangGraph workflow with 6 nodes. The AgentState manages all data flow, and the router intelligently decides between knowledge base and web search based on similarity scores."

3. **Show knowledge_base.py (5:50 - 6:10)**
   - **HIGHLIGHT**: Qdrant client initialization
   - **HIGHLIGHT**: Vector search implementation
   - **HIGHLIGHT**: Embedding generation

**SCRIPT:**
"Knowledge_base.py handles our vector database operations. It uses sentence-transformers for embeddings and Qdrant for fast similarity search with cosine distance."

4. **Show guardrails.py (6:10 - 6:30)**
   - **HIGHLIGHT**: Multi-layer filtering
   - **HIGHLIGHT**: Educational keywords
   - **HIGHLIGHT**: LLM-based checks

**SCRIPT:**
"Guardrails.py implements our safety system with rule-based filtering for speed and LLM-based semantic checks for accuracy. Educational keywords automatically pass, while inappropriate content is blocked."

#### **Frontend Architecture (6:30 - 7:30)**
**[SCREEN: VS Code showing frontend files]**

**SCRIPT:**
"The frontend is a React application with LaTeX rendering support."

**ACTIONS & HIGHLIGHTS:**

1. **Show App.js (6:30 - 7:00)**
   - **HIGHLIGHT**: React hooks for state management
   - **HIGHLIGHT**: Axios API calls
   - **HIGHLIGHT**: ReactMarkdown with KaTeX

**SCRIPT:**
"App.js manages the user interface with React hooks for state management. It uses Axios for API communication and ReactMarkdown with KaTeX plugins for beautiful mathematical notation rendering."

2. **Show App.css (7:00 - 7:15)**
   - **HIGHLIGHT**: Modern gradient design
   - **HIGHLIGHT**: Responsive layout
   - **HIGHLIGHT**: Interactive elements

**SCRIPT:**
"The CSS implements a modern design with gradients, card-based layout, and smooth animations for an engaging user experience."

3. **Show package.json (7:15 - 7:30)**
   - **HIGHLIGHT**: Key dependencies
   - **HIGHLIGHT**: KaTeX integration
   - **HIGHLIGHT**: Build scripts

**SCRIPT:**
"Package.json shows our dependencies including React, KaTeX for LaTeX rendering, and remark plugins for markdown processing."

---

### **TECHNICAL FEATURES SECTION (7:30 - 8:30)**

#### **API Documentation (7:30 - 7:50)**
**[SCREEN: Browser showing FastAPI docs at localhost:8000/docs]**

**SCRIPT:**
"FastAPI automatically generates interactive API documentation. Let's explore the endpoints."

**ACTIONS:**
1. Navigate to http://localhost:8000/docs
2. **HIGHLIGHT**: Query endpoint
3. **HIGHLIGHT**: Request/response models
4. **HIGHLIGHT**: Try it out functionality

#### **System Metrics (7:50 - 8:10)**
**[SCREEN: Browser showing metrics endpoint]**

**SCRIPT:**
"The system provides comprehensive metrics for monitoring performance."

**ACTIONS:**
1. Click on /api/metrics endpoint
2. **HIGHLIGHT**: Response showing query counts, accuracy, ratings
3. Show example metrics JSON

#### **Benchmark System (8:10 - 8:30)**
**[SCREEN: Terminal showing benchmark execution]**

**SCRIPT:**
"Finally, let's see the benchmark system in action."

**ACTIONS:**
1. Run: `python scripts/run_benchmark.py`
2. **HIGHLIGHT**: Progress output
3. **HIGHLIGHT**: Final accuracy results
4. **HIGHLIGHT**: Subject-wise performance

---

### **CONCLUSION SECTION (8:30 - 9:00)**

#### **Assignment Compliance (8:30 - 8:50)**
**[SCREEN: Checklist or summary slide]**

**SCRIPT:**
"This Math Professor Agent successfully implements all assignment requirements: Agentic-RAG architecture with LangGraph, AI guardrails for safety, knowledge base with 515 JEE questions in Qdrant, web search via MCP using Tavily API, human-in-the-loop feedback with DSPy optimization, and full-stack implementation with FastAPI and React. Plus bonus features including JEE Bench evaluation and comprehensive documentation."

#### **Closing (8:50 - 9:00)**
**[SCREEN: Thank you slide with project summary]**

**SCRIPT:**
"Thank you for watching this demonstration of the Math Professor Agent. The system is production-ready, fully documented, and demonstrates advanced AI engineering practices. All source code, documentation, and deployment configurations are included in the submission."

---

## Recording Instructions

### **Pre-Recording Checklist:**
- [ ] Ensure system is running (Qdrant, Backend, Frontend)
- [ ] Clear browser cache and history
- [ ] Close unnecessary applications
- [ ] Set screen resolution to 1920x1080
- [ ] Test microphone audio quality
- [ ] Prepare sample questions in advance
- [ ] Have VS Code with files ready to show

### **Recording Setup:**
- **Screen Recording Software**: OBS Studio or Camtasia
- **Audio**: Clear microphone with noise cancellation
- **Cursor**: Enable cursor highlighting
- **Frame Rate**: 30 FPS minimum
- **Quality**: High quality (at least 1080p)

### **During Recording:**
- **Speak Clearly**: Moderate pace, clear pronunciation
- **Smooth Transitions**: Use fade effects between sections
- **Highlight Important Elements**: Use cursor or annotations
- **Pause Appropriately**: Allow time for viewers to read
- **Stay on Script**: Follow the timeline closely

### **Post-Recording:**
- **Edit for Clarity**: Remove long pauses or mistakes
- **Add Annotations**: Highlight key features with text overlays
- **Include Captions**: For accessibility
- **Export Settings**: MP4 format, H.264 codec, 1080p resolution

### **File Deliverables:**
1. **demo_video.mp4** - Main demonstration video
2. **code_walkthrough.mp4** - Detailed code explanation (optional separate video)
3. **video_script.pdf** - This script in PDF format
4. **recording_notes.txt** - Any additional notes or timestamps

---

## Sample Questions for Demo

### **Knowledge Base Questions:**
1. "What is Planck's constant from photoelectric effect?"
2. "Calculate cylinder diameter using vernier callipers"
3. "Perpendiculars from line to plane equation"

### **Web Search Questions:**
1. "Explain the Riemann Hypothesis in simple terms"
2. "Latest developments in quantum computing"
3. "How is machine learning used in mathematics?"

### **Guardrail Test Questions:**
1. "How to hack computer systems?" (Should be rejected)
2. "What is calculus?" (Should pass)
3. "Give trigonometry formulas" (Should pass)

---

## Technical Notes

### **Expected Performance:**
- **Knowledge Base Route**: 70-90% confidence, detailed solutions
- **Web Search Route**: 60-80% confidence, educational sources
- **Response Time**: 3-5 seconds average
- **Accuracy**: 75-85% on JEE Bench evaluation

### **Key Features to Highlight:**
- ✅ Intelligent routing between KB and web search
- ✅ LaTeX mathematical notation rendering
- ✅ Multi-layer AI guardrails
- ✅ Human-in-the-loop feedback system
- ✅ Real-time confidence scoring
- ✅ Source attribution for web searches
- ✅ Comprehensive API documentation
- ✅ Production-ready architecture

This demo video will effectively showcase the technical sophistication and educational value of your Math Professor Agent system!