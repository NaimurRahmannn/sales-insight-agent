from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

from . import config
from .prompts import SYSTEM_PROMPT
from .tools import (
    query_sales,
    category_analysis,
    regional_analysis,
    get_forecast,
    business_insight
)

# Initialize the Gemini model
# Temperature is set to 0 for highly deterministic, factual analytical responses
llm = ChatGoogleGenerativeAI(
    model=config.GEMINI_MODEL,
    temperature=0,
    google_api_key=config.GEMINI_API_KEY
)

# Register all analytical tools
tools = [
    query_sales,
    category_analysis,
    regional_analysis,
    get_forecast,
    business_insight
]

# Create the LangGraph ReAct agent
app = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT
)

def ask(question: str) -> str:
    """
    Passes a natural language question to the AI Agent.
    The agent autonomously decides which PostgreSQL or CSV tools to use,
    executes them, and returns a natural language business answer.
    """
    inputs = {"messages": [HumanMessage(content=question)]}
    
    try:
        # Stream or invoke the agent
        # We use invoke to get the final state
        result = app.invoke(inputs)
        
        content = result["messages"][-1].content
        if isinstance(content, list):
            return content[0].get("text", str(content))
        return content
    except Exception as e:
        return f"Agent encountered an error: {str(e)}"
