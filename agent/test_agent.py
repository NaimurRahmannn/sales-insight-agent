import sys
import os

# Ensure the parent directory is in the path so we can import the agent package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.agent import ask

def run_tests():
    print("==================================================")
    print("--- Testing LangGraph AI Analytics Agent ---")
    print("==================================================")
    
    test_questions = [
        {
            "id": 1,
            "q": "What were total sales?",
            "expected_tool": "query_sales"
        },
        {
            "id": 2,
            "q": "Which region generates the highest profit?",
            "expected_tool": "regional_analysis"
        },
        {
            "id": 3,
            "q": "Why is Furniture underperforming?",
            "expected_tool": "business_insight"
        },
        {
            "id": 4,
            "q": "What are forecasted sales for the next 3 months?",
            "expected_tool": "get_forecast"
        }
    ]
    
    for test in test_questions:
        print(f"\n[Question {test['id']}] {test['q']}")
        print(f"(Expected to use: {test['expected_tool']})")
        print("-" * 50)
        
        try:
            answer = ask(test['q'])
            print(answer)
        except Exception as e:
            print(f"Error: {e}")
            
        print("=" * 50)

if __name__ == "__main__":
    run_tests()
