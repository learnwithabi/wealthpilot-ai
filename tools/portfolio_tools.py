import json
import os
from langchain_core.tools import tool

_DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/clients.json")

def _load_data() -> dict:
    with open(_DATA_FILE) as f:
        return json.load(f)


@tool
def get_portfolio_holdings(client_id: str) -> str:
    """Get current portfolio holdings for a client."""
    data = _load_data()
    client = data["clients"].get(client_id)
    if not client:
        return f"No client found with ID '{client_id}'. Available IDs: {', '.join(data['clients'].keys())}"

    p = client["portfolio"]
    equity_lines = "\n".join(
        f"      {h['stock']}: {h['allocation']}%"
        for h in p["equity"]["holdings"]
    )
    debt_lines = "\n".join(
        f"      {h['instrument']}: {h['allocation']}%"
        for h in p["debt"]["holdings"]
    )
    gold_lines = "\n".join(
        f"      {h['instrument']}: {h['allocation']}%"
        for h in p["gold"]["holdings"]
    )

    return f"""
    Client: {client['name']} ({client_id})
    Age: {client['age']} | Category: {client['category']} | Risk Profile: {client['risk_profile']}
    Retirement In: {client['retirement_in_years']} years
    Portfolio Value: {p['total_value']}

    Allocation:
      Equity ({p['equity']['percentage']}%):
{equity_lines}
      Debt ({p['debt']['percentage']}%):
{debt_lines}
      Gold ({p['gold']['percentage']}%):
{gold_lines}
    """
