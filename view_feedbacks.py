"""View submitted feedbacks in a nice format."""
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

def view_feedbacks():
    """Display all feedbacks in a readable format."""
    feedback_file = Path("data/feedback.json")
    
    if not feedback_file.exists():
        print("❌ No feedback file found. Submit some feedback first!")
        return
    
    with open(feedback_file, 'r') as f:
        data = json.load(f)
    
    feedbacks = data.get("feedback", [])
    stats = data.get("statistics", {})
    
    print("=" * 80)
    print("📊 FEEDBACK SUMMARY")
    print("=" * 80)
    
    if stats:
        print(f"Total Feedbacks: {stats.get('total_feedback', 0)}")
        print(f"Overall Accuracy: {stats.get('accuracy', 0):.1%}")
        print(f"Average Rating: {stats.get('avg_rating', 0):.1f}/5.0")
        print(f"Last Updated: {stats.get('last_updated', 'Unknown')}")
        
        # Route performance
        route_perf = stats.get('route_performance', {})
        if route_perf:
            print("\n📈 Route Performance:")
            for route, perf in route_perf.items():
                accuracy = perf['correct'] / perf['total'] if perf['total'] > 0 else 0
                print(f"  {route}: {perf['correct']}/{perf['total']} ({accuracy:.1%})")
    
    print("\n" + "=" * 80)
    print("💬 INDIVIDUAL FEEDBACKS")
    print("=" * 80)
    
    if not feedbacks:
        print("No feedbacks submitted yet.")
        return
    
    for i, feedback in enumerate(feedbacks, 1):
        print(f"\n--- Feedback #{i} ---")
        print(f"Query ID: {feedback['query_id']}")
        print(f"Timestamp: {feedback['timestamp']}")
        print(f"Question: {feedback['original_question'][:100]}...")
        print(f"Answer: {feedback['original_answer']}")
        print(f"Route Used: {feedback['route_used']}")
        print(f"Rating: {feedback['rating']}/5 ⭐")
        print(f"Correct: {'✅ Yes' if feedback['is_correct'] else '❌ No'}")
        
        if feedback['feedback_text']:
            print(f"Comment: \"{feedback['feedback_text']}\"")
        
        if feedback['suggested_answer']:
            print(f"Suggested Answer: {feedback['suggested_answer']}")
        
        print("-" * 50)

if __name__ == "__main__":
    view_feedbacks()