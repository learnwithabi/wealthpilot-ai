from langgraph_supervisor import create_supervisor
from config.settings import llm
from agents.portfolio_analyst import portfolio_analyst
from agents.market_researcher import market_researcher
from agents.risk_compliance import risk_compliance

supervisor_prompt = """
You are the Senior Portfolio Supervisor at Demo AI Portfolio Intelligence.
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

app = workflow.compile()
