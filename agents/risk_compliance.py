from langgraph.prebuilt import create_react_agent
from config.settings import llm
from tools.risk_tools import calculate_risk_metrics

risk_compliance = create_react_agent(
    model=llm,
    tools=[calculate_risk_metrics],
    name="risk_compliance",
    prompt="You are a Risk & Compliance Officer. Focus on suitability, regulatory compliance, and risk control. Always pass the client_id when calling calculate_risk_metrics."
)
