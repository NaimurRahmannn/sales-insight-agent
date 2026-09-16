# AI-Powered Sales Intelligence Platform

This project is an end-to-end AI-powered business analytics platform that transforms raw sales data into actionable insights using Machine Learning, a PostgreSQL Data Warehouse, and a LangGraph AI Agent.

## Architecture

1. **Python Data Pipeline**: Cleans, transforms, and engineers features from raw CSV sales data.
2. **PostgreSQL Database**: A robust star-schema data warehouse serving as the single source of truth for the AI Agent.
3. **Machine Learning Model**: An XGBoost time-series forecaster that predicts future revenue trends.
4. **LangGraph AI Agent**: A ReAct-based AI agent powered by Gemini 3.1 Flash Lite that intelligently routes natural language questions to deterministic SQL and CSV tools.
5. **Streamlit Chat Interface**: A user-friendly frontend allowing non-technical business users to chat with their data.

## How to run the Streamlit App

1. Ensure your PostgreSQL database is running (via Docker or local installation) and the data is loaded.
2. Ensure you have installed all dependencies (including `streamlit`) and your `.env` file is properly configured with your PostgreSQL credentials and `GEMINI_API_KEY`.
3. Run the Streamlit application from the root directory:
   ```bash
   streamlit run app.py
   ```
4. Open the provided local URL in your web browser.

## Example Questions to Ask

Once the app is running, try asking the AI:
- "What are total sales?"
- "Which region has highest profit?"
- "Why is Furniture underperforming?"
- "What are next 3 months forecast?"
