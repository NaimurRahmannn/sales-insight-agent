# LangGraph AI Analytics Agent

This package contains the AI intelligence layer for the Sales Intelligence Platform, built with LangGraph, LangChain, and the Google Gemini 3.1 Flash Lite model.

## AI Agent Architecture

The agent acts as a conversational business analyst, providing insights derived exclusively from the PostgreSQL database and XGBoost forecast results. It follows a ReAct (Reasoning and Acting) execution pattern:

```text
User Question
      ↓
Gemini 3.1 Flash Lite (Reasoning)
      ↓
LangGraph ReAct Agent (Routing)
      ↓
Analytical Tools (SQL/CSV execution)
      ↓
Final Business Answer
```

## Available Tools

To ensure deterministic, hallucination-free analytics, the LLM is restricted from writing arbitrary SQL. It relies on the following predefined tools:

- `query_sales`: Retrieves total sales, profit, margin, and order counts (with optional filters).
- `category_analysis`: Aggregates profitability metrics grouped by product categories.
- `regional_analysis`: Compares performance across geographic regions.
- `get_forecast`: Retrieves forward-looking sales expectations from the `forecast_results.csv`.
- `business_insight`: Provides pre-calculated qualitative reasoning for specific anomalies (e.g., Furniture losses, discount impacts).

## Setup Instructions

1. Ensure the PostgreSQL database is running and populated (see the `database/` directory).
2. Ensure you have your `GEMINI_API_KEY` defined in the root `.env` file.
3. Install dependencies:
   ```bash
   pip install langchain langgraph langchain-google-genai pydantic
   ```

## Example Conversations

You can programmatically interact with the agent using the `ask()` function in `agent.py`:

```python
from agent.agent import ask

# Example 1: Historical Sales Query
response = ask("What were total sales in the West region?")
print(response)

# Example 2: Qualitative Insight
response = ask("Why is Furniture underperforming?")
print(response)

# Example 3: Forward-Looking Forecast
response = ask("What are the predicted sales for the next 3 months?")
print(response)
```

## Testing

Run the automated test suite to verify the agent's tool selection and reasoning:
```bash
python -m agent.test_agent
```
