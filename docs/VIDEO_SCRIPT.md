# Demo Video Script

## Duration: 5-7 minutes

---

## Scene 1: Introduction (30 seconds)

**Visual**: Title slide with project name and architecture diagram

**Narration**:
"Welcome to the Math Professor Agent - an intelligent tutoring system that combines knowledge base retrieval, web search, and human feedback to provide step-by-step solutions to mathematical problems. This system uses cutting-edge AI technologies including LangGraph, GPT-4, and DSPy to create an adaptive learning experience."

---

## Scene 2: Architecture Overview (1 minute)

**Visual**: Animated architecture flowchart

**Narration**:
"Let's walk through the system architecture. When a user submits a question, it first passes through input guardrails powered by Claude 3 Sonnet, which filters inappropriate content and ensures educational relevance.

Next, the router agent makes an intelligent decision: should we search our knowledge base of 515 JEE Advanced questions, or perform a web search for information not in our database?

If the question matches our knowledge base with high confidence, we retrieve similar problems from Qdrant vector database. Otherwise, we use Tavily API through the Model Context Protocol to search the web.

The solution generator then uses GPT-4 with few-shot learning to create detailed, step-by-step explanations. Finally, output guardrails verify the quality before presenting to the user."

---

## Scene 3: Knowledge Base Demo (1 minute)

**Visual**: Screen recording of frontend with KB question

**Narration**:
"Let's see it in action. Here's a physics question from JEE Advanced about calculating Planck's constant from photoelectric effect data.

[Type question and submit]

Notice the system routes this to the knowledge base, retrieves similar problems, and generates a comprehensive solution with step-by-step reasoning. The final answer is clearly marked, and we can see the confidence score is high at 87%."

**Show**:
- Question input
- Loading state
- Response with route badge showing "knowledge_base"
- Step-by-step solution with LaTeX rendering
- Final answer highlighted
- Confidence score

---

## Scene 4: Web Search Demo (1 minute)

**Visual**: Screen recording with web search question

**Narration**:
"Now let's try a question that's not in our knowledge base - asking about recent developments in quantum computing algorithms.

[Type question and submit]

The system recognizes this isn't in the knowledge base and automatically routes to web search. It queries educational sources like Wikipedia and academic sites, then synthesizes the information into a clear explanation. Notice the sources are listed at the bottom for verification."

**Show**:
- Question about quantum computing
- Route badge showing "web_search"
- Solution with web-sourced information
- Source URLs listed

---

## Scene 5: Guardrails Demo (45 seconds)

**Visual**: Screen recording showing guardrail rejection

**Narration**:
"The system includes robust guardrails. Watch what happens when we try an inappropriate or off-topic question.

[Type inappropriate question]

The input guardrail immediately rejects it, explaining why it cannot process the request. This ensures the system stays focused on educational mathematics content."

**Show**:
- Inappropriate question attempt
- Error message from guardrail
- Explanation of rejection

---

## Scene 6: Human-in-the-Loop Feedback (1 minute)

**Visual**: Screen recording of feedback submission

**Narration**:
"One of the most powerful features is the human-in-the-loop feedback mechanism. Users can rate responses, mark correctness, and provide suggestions.

[Click 'Provide Feedback' button]

Let's say this answer needs improvement. We can mark it as incorrect, provide a rating, and add comments. The system uses DSPy to automatically refine the response based on this feedback.

[Submit feedback]

Notice how the system immediately generates an improved solution incorporating our feedback. This creates a continuous learning loop that makes the agent better over time."

**Show**:
- Feedback button
- Feedback form with rating slider
- Correctness checkbox
- Text feedback field
- Refined response generation

---

## Scene 7: Metrics Dashboard (30 seconds)

**Visual**: API metrics endpoint or dashboard

**Narration**:
"The system tracks comprehensive metrics including overall accuracy, route distribution, average confidence scores, and user satisfaction ratings. This data helps us understand system performance and identify areas for improvement."

**Show**:
- Metrics API response
- Statistics: total queries, accuracy, route distribution
- Feedback statistics

---

## Scene 8: Benchmark Results (1 minute)

**Visual**: Benchmark results visualization

**Narration**:
"We evaluated the system on the full JEE Bench dataset of 515 questions. The results show strong performance across all subjects:

- Overall accuracy: 78%
- Mathematics: 82% accuracy
- Physics: 77% accuracy  
- Chemistry: 74% accuracy

The system correctly routes 90% of queries to the knowledge base, with the remaining 10% handled by web search. Average response time is under 4 seconds, making it practical for real-time tutoring."

**Show**:
- Benchmark results table
- Subject-wise accuracy chart
- Route distribution pie chart
- Response time metrics

---

## Scene 9: Technology Stack (30 seconds)

**Visual**: Technology logos and stack diagram

**Narration**:
"The system is built with modern AI technologies:
- LangGraph for agent orchestration
- GPT-4 for solution generation
- Claude 3 for guardrails
- Qdrant for vector storage
- DSPy for optimization
- FastAPI backend and React frontend

All code is open source and well-documented."

---

## Scene 10: Conclusion (30 seconds)

**Visual**: Summary slide with key features

**Narration**:
"To summarize, the Math Professor Agent successfully implements:
- Multi-layer AI guardrails for safety
- Intelligent routing between knowledge base and web search
- Step-by-step solution generation
- Human-in-the-loop feedback with DSPy optimization
- Comprehensive benchmarking on JEE dataset

This creates a robust, adaptive tutoring system that continuously improves through user interaction. Thank you for watching!"

**Show**:
- Checkmarks for each feature
- GitHub repository link
- Contact information

---

## Recording Tips

1. **Screen Resolution**: 1920x1080 for clarity
2. **Mouse Highlighting**: Enable cursor highlighting
3. **Smooth Transitions**: Use fade effects between scenes
4. **Background Music**: Subtle, non-distracting
5. **Pace**: Speak clearly, not too fast
6. **Captions**: Add subtitles for accessibility
7. **Code Snippets**: Zoom in when showing code
8. **Loading States**: Speed up long waits in editing

## Required Footage

- [ ] Architecture diagram animation
- [ ] Frontend demo with KB question
- [ ] Frontend demo with web search question
- [ ] Guardrail rejection example
- [ ] Feedback submission and refinement
- [ ] Metrics/statistics display
- [ ] Benchmark results visualization
- [ ] Technology stack slide
- [ ] Summary and conclusion

## Post-Production

1. Add intro/outro animations
2. Include background music
3. Add text overlays for key points
4. Include captions/subtitles
5. Color grade for consistency
6. Export in 1080p, 30fps
7. Upload to YouTube/platform
8. Add timestamps in description
