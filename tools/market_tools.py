import json
import os
from langchain_core.tools import tool

_DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/clients.json")

def _load_data() -> dict:
    with open(_DATA_FILE) as f:
        return json.load(f)


@tool
def get_market_research(sector: str) -> str:
    """Get latest market outlook for a sector."""
    data = _load_data()
    outlooks = data["market_outlook"]

    matched = next(
        (v for k, v in outlooks.items() if k.lower() == sector.strip().lower()),
        None
    )
    if not matched:
        available = ", ".join(outlooks.keys())
        return f"No data found for sector '{sector}'. Available sectors: {available}"

    return (
        f"Sector: {sector}\n"
        f"Outlook: {matched['outlook']}\n"
        f"Summary: {matched['summary']}\n"
        f"Recommendation: {matched['recommendation']}\n"
        f"Risk Level: {matched['risk']}"
    )
