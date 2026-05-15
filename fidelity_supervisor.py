import os
from dotenv import load_dotenv

# LangChain & LangGraph
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent  # noqa: F401 — still valid in langgraph 1.x
from langgraph_supervisor import create_supervisor
from langchain_core.tools import tool

load_dotenv()

# ================== CONFIG ==================
# Switch USE_GOOGLE to True once the Google API key quota resets
USE_GOOGLE = False

if USE_GOOGLE:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not set in .env")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        temperature=0.1,
        google_api_key=GOOGLE_API_KEY,
        max_tokens=1024
    )
else:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set in .env")
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        api_key=GROQ_API_KEY,
        max_tokens=1024
    ).bind(parallel_tool_calls=False)

# ================== TOOLS ==================
@tool
def get_portfolio_holdings(client_id: str) -> str:
    """Get current portfolio holdings for a client."""
    # Mock data for demo
    return f"""
    Client {client_id} Portfolio:
    - Equity: 65% (HDFC Bank 12%, Reliance 10%, TCS 8%)
    - Debt: 25%
    - Gold: 10%
    Current Value: ₹8.4 Crore
    """

@tool
def get_market_research(sector: str) -> str:
    """Get latest market outlook for a sector."""
    return f"Market Outlook for {sector}: Strong growth expected in next 6 months due to ..."

@tool
def calculate_risk_metrics() -> str:
    """Calculate basic risk metrics for the current portfolio."""
    return "Portfolio Volatility: 18.4% | Sharpe Ratio: 1.12 | Max Drawdown: -12.5% | Risk Level: Moderate-High"

# ================== WORKER AGENTS ==================
portfolio_analyst = create_react_agent(
    model=llm,
    tools=[get_portfolio_holdings],
    name="portfolio_analyst",
    prompt="You are an expert Portfolio Analyst at Fidelity International."
)

market_researcher = create_react_agent(
    model=llm,
    tools=[get_market_research],
    name="market_researcher",
    prompt="You are a Senior Market Researcher. Provide concise, actionable insights."
)

risk_compliance = create_react_agent(
    model=llm,
    tools=[calculate_risk_metrics],
    name="risk_compliance",
    prompt="You are a Risk & Compliance Officer. Focus on suitability, regulatory compliance, and risk control."
)

# ================== SUPERVISOR ==================
supervisor_prompt = """
You are the Senior Portfolio Supervisor at Fidelity International.
Your job is to coordinate a team to conduct a professional quarterly portfolio review.

Available Agents:
- portfolio_analyst: Good for holdings, performance, and basic analysis
- market_researcher: Good for market trends and sector outlook
- risk_compliance: Good for risk assessment and compliance

IMPORTANT: Delegate to ONE agent at a time. Wait for each response before calling the next.
After all agents have responded, synthesize a final recommendation.
Be professional, conservative, and client-focused.
"""

workflow = create_supervisor(
    agents=[portfolio_analyst, market_researcher, risk_compliance],
    model=llm,
    prompt=supervisor_prompt,
)

# Compile the graph
app = workflow.compile()

# ================== RUN ==================
if __name__ == "__main__":
    print("Fidelity International - Portfolio Review Supervisor\n")
    
    client_input = """
    Client: Rahul Sharma (Client ID: C001, High Net Worth, retiring in 3 years)
    Do a full quarterly portfolio review:
    1. Fetch current holdings and check if the equity allocation is too high given the retirement horizon.
    2. Research the Banking and IT sector outlook.
    3. Assess the portfolio risk level and check if it suits a client approaching retirement.
    4. Recommend whether to rebalance and what specific changes to make.
    """

    try:
        result = app.invoke({
            "messages": [("user", client_input)]
        })
        print("\n" + "="*60)
        print("FINAL SUPERVISOR OUTPUT:")
        print("="*60)
        # Last message is the supervisor's final synthesis
        print(result["messages"][-1].content)
    except Exception as e:
        print(f"Error during portfolio review: {e}")
        raise