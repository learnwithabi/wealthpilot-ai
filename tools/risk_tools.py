import json
import os
from langchain_core.tools import tool

_DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/clients.json")

def _load_data() -> dict:
    with open(_DATA_FILE) as f:
        return json.load(f)


@tool
def calculate_risk_metrics(client_id: str) -> str:
    """Calculate risk metrics and suitability assessment for a client."""
    data = _load_data()
    client = data["clients"].get(client_id)
    if not client:
        return f"No client found with ID '{client_id}'."

    equity_pct = client["portfolio"]["equity"]["percentage"]
    risk_profile = client["risk_profile"]
    benchmark = data["risk_benchmarks"].get(risk_profile, {})
    max_equity = benchmark.get("max_equity", 100)
    sharpe_target = benchmark.get("sharpe_target", 1.0)

    volatility = round(10 + equity_pct * 0.15, 1)
    sharpe = round(sharpe_target - (equity_pct - max_equity) * 0.01, 2) if equity_pct > max_equity else sharpe_target
    max_drawdown = round(-(equity_pct * 0.20), 1)
    compliant = equity_pct <= max_equity

    return (
        f"Client: {client['name']} ({client_id}) | Risk Profile: {risk_profile}\n"
        f"Equity Allocation: {equity_pct}% (Max allowed: {max_equity}%)\n"
        f"Portfolio Volatility: {volatility}%\n"
        f"Sharpe Ratio: {sharpe}\n"
        f"Max Drawdown Estimate: {max_drawdown}%\n"
        f"Suitability Compliant: {'YES' if compliant else 'NO — rebalancing required'}"
    )
