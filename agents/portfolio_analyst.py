from langgraph.prebuilt import create_react_agent
from config.settings import llm
from tools.portfolio_tools import get_portfolio_holdings

portfolio_analyst = create_react_agent(
    model=llm,
    tools=[get_portfolio_holdings],
    name="portfolio_analyst",
    prompt="You are an expert Portfolio Analyst at Fidelity International."
)
