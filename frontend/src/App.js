import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [rating, setRating] = useState(5);
  const [feedbackText, setFeedbackText] = useState('');
  const [isCorrect, setIsCorrect] = useState(true);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);
    setShowFeedback(false);

    try {
      const res = await axios.post(`${API_BASE_URL}/api/query`, {
        question: question
      });
      setResponse(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async () => {
    if (!response) return;

    try {
      const feedbackRes = await axios.post(`${API_BASE_URL}/api/feedback`, {
        query_id: response.query_id,
        rating: rating,
        feedback_text: feedbackText,
        is_correct: isCorrect,
        suggested_answer: null
      });

      if (feedbackRes.data.updated_response) {
        setResponse(feedbackRes.data.updated_response);
      }
      
      alert('Feedback submitted successfully!');
      setShowFeedback(false);
    } catch (err) {
      alert('Error submitting feedback');
    }
  };

  const sampleQuestions = [
    "The diameter of a cylinder is measured using a vernier callipers...",
    "What is Planck's constant from photoelectric effect?",
    "Explain the Riemann Hypothesis in simple terms"
  ];

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎓 Math Professor Agent</h1>
        <p>AI-powered mathematical tutoring with step-by-step solutions</p>
      </header>

      <main className="App-main">
        <div className="query-section">
          <form onSubmit={handleSubmit}>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Enter your mathematical question here..."
              rows="4"
              disabled={loading}
            />
            <button type="submit" disabled={loading || !question.trim()}>
              {loading ? 'Processing...' : 'Get Solution'}
            </button>
          </form>

          <div className="sample-questions">
            <p>Try these sample questions:</p>
            {sampleQuestions.map((q, idx) => (
              <button
                key={idx}
                onClick={() => setQuestion(q)}
                className="sample-btn"
              >
                {q.substring(0, 50)}...
              </button>
            ))}
          </div>
        </div>

        {error && (
          <div className="error-box">
            <strong>Error:</strong> {error}
          </div>
        )}

        {response && (
          <div className="response-section">
            <div className="response-header">
              <h2>Solution</h2>
              <div className="metadata">
                <span className="badge">{response.route_used}</span>
                <span className="confidence">
                  Confidence: {(response.confidence_score * 100).toFixed(0)}%
                </span>
              </div>
            </div>

            <div className="solution-content">
              {response.step_by_step_solution?.trim() ? (
                <ReactMarkdown
                  remarkPlugins={[remarkMath]}
                  rehypePlugins={[rehypeKatex]}
                >
                  {response.step_by_step_solution}
                </ReactMarkdown>
              ) : (
                <p className="no-solution-message">
                  {response.answer?.trim() || "No solution available for this question."}
                </p>
              )}
            </div>

            {response.sources && response.sources.length > 0 && (
              <div className="sources">
                <strong>Sources:</strong>
                <ul>
                  {response.sources.map((source, idx) => (
                    <li key={idx}>
                      <a href={source} target="_blank" rel="noopener noreferrer">
                        {source}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="feedback-section">
              {!showFeedback ? (
                <button onClick={() => setShowFeedback(true)} className="feedback-btn">
                  Provide Feedback
                </button>
              ) : (
                <div className="feedback-form">
                  <h3>Your Feedback</h3>
                  
                  <label>
                    <input
                      type="checkbox"
                      checked={isCorrect}
                      onChange={(e) => setIsCorrect(e.target.checked)}
                    />
                    The answer is correct
                  </label>

                  <label>
                    Rating: {rating}/5
                    <input
                      type="range"
                      min="1"
                      max="5"
                      value={rating}
                      onChange={(e) => setRating(parseInt(e.target.value))}
                    />
                  </label>

                  <textarea
                    value={feedbackText}
                    onChange={(e) => setFeedbackText(e.target.value)}
                    placeholder="Additional comments..."
                    rows="3"
                  />

                  <div className="feedback-buttons">
                    <button onClick={handleFeedback}>Submit Feedback</button>
                    <button onClick={() => setShowFeedback(false)}>Cancel</button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>Powered by LangGraph, OpenAI, and Qdrant</p>
      </footer>
    </div>
  );
}

export default App;
