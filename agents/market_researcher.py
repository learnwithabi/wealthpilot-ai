from langgraph.prebuilt import create_react_agent
from config.settings import llm
from tools.market_tools import get_market_research

market_researcher = create_react_agent(
    model=llm,
    tools=[get_market_research],
    name="market_researcher",
    prompt="You are a Senior Market Researcher. Provide concise, actionable insights."
)
