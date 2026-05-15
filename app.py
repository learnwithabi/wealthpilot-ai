import json
import os
import streamlit as st
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WealthPilot AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .section-header {
        color: #4f8ef7; font-size: 16px; font-weight: 600;
        margin: 20px 0 10px 0;
        border-bottom: 1px solid #2d3448; padding-bottom: 6px;
    }
    .agent-step {
        background: #1a1f2e; border-left: 4px solid #4f8ef7;
        border-radius: 6px; padding: 10px 14px; margin: 6px 0;
        font-size: 13px; color: #c9d1d9;
    }
    .report-box {
        background: #161b27; border: 1px solid #2d3448;
        border-radius: 12px; padding: 28px 32px;
        font-size: 14px; line-height: 1.8;
    }
    .status-pill {
        display:inline-block; padding: 2px 12px;
        border-radius: 20px; font-size: 12px; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ── Load client data ──────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "data/clients.json")

@st.cache_data
def load_data():
    with open(DATA_PATH) as f:
        return json.load(f)

data       = load_data()
clients    = data["clients"]
market_out = data["market_outlook"]
benchmarks = data["risk_benchmarks"]

SAMPLE_QUESTIONS = {
    "Quarterly Portfolio Review": (
        "Do a full quarterly portfolio review:\n"
        "1. Fetch current holdings and check if equity allocation suits the retirement horizon.\n"
        "2. Research the Banking and IT sector outlook.\n"
        "3. Assess the portfolio risk level and suitability.\n"
        "4. Recommend whether to rebalance and what specific changes to make."
    ),
    "Stress Test — IT & Banking Drop": (
        "Run a stress test: if IT drops 20% and Banking drops 15%, "
        "what is the impact? Check risk metrics and recommend defensive moves."
    ),
    "Sector Rotation Strategy": (
        "The client wants to rotate out of Banking into Pharma and Gold. "
        "Research both sector outlooks, assess the risk impact, "
        "and give a final buy/sell recommendation."
    ),
    "Retirement Readiness Check": (
        "Assess whether this client is ready for retirement. "
        "Check holdings, risk level, and market conditions in Banking and Energy. "
        "Suggest a glide path to capital preservation."
    ),
    "Custom Question": "",
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📈 WealthPilot AI")
    st.caption("Demo · AI Portfolio Intelligence")
    st.divider()

    client_options = {cid: f"{c['name']}  ({cid})" for cid, c in clients.items()}
    selected_id = st.selectbox(
        "Select Client",
        options=list(client_options.keys()),
        format_func=lambda x: client_options[x],
    )
    client = clients[selected_id]
    p      = client["portfolio"]

    st.divider()
    st.markdown(f"**{client['name']}**")
    st.markdown(f"Age **{client['age']}** · {client['category']}")
    st.markdown(f"Risk Profile: **{client['risk_profile']}**")
    st.markdown(f"Retires in: **{client['retirement_in_years']} yrs**")
    st.markdown(f"Value: **{p['total_value']}**")
    st.divider()

    st.markdown("**Agent Team**")
    st.markdown("🧠 Supervisor")
    st.markdown("&nbsp;&nbsp;├ 📊 Portfolio Analyst", unsafe_allow_html=True)
    st.markdown("&nbsp;&nbsp;├ 🔍 Market Researcher", unsafe_allow_html=True)
    st.markdown("&nbsp;&nbsp;└ ⚖️ Risk & Compliance", unsafe_allow_html=True)
    st.divider()
    st.caption("v2.0 · LangGraph + Streamlit")

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown(f"## 📈 WealthPilot AI")
st.caption(f"Client: **{client['name']}** ({selected_id}) · {client['category']} · Risk: {client['risk_profile']}")
st.divider()

# ── Step 1 — Question input ───────────────────────────────────────────────────
st.markdown("### 1️⃣  Ask the Supervisor Agent")

q_choice = st.selectbox("Sample questions:", list(SAMPLE_QUESTIONS.keys()))
default_q = SAMPLE_QUESTIONS[q_choice]
client_prefix = f"Client: {client['name']} (Client ID: {selected_id})\n"

prompt_text = st.text_area(
    "Your question to the supervisor:",
    value=client_prefix + default_q,
    height=150,
)

run = st.button("▶  Run Supervisor Agent", type="primary")

# ── Step 2 — Run agents + show live steps ─────────────────────────────────────
if run and prompt_text.strip():
    st.divider()
    st.markdown("### 2️⃣  Supervisor Coordinating Agents")

    step_placeholder = st.empty()
    steps_log = []

    def log_step(icon, agent, msg):
        steps_log.append(f"{icon} **{agent}** — {msg}")
        step_placeholder.markdown("\n\n".join(
            f'<div class="agent-step">{s}</div>' for s in steps_log
        ), unsafe_allow_html=True)

    log_step("🧠", "Supervisor", f"Received request for {client['name']} ({selected_id})")
    log_step("📊", "Portfolio Analyst", "Fetching holdings and allocation data...")
    log_step("🔍", "Market Researcher", "Researching sector outlook...")
    log_step("⚖️", "Risk & Compliance", "Calculating risk metrics and suitability...")
    log_step("🧠", "Supervisor", "Synthesizing final recommendation...")

    with st.spinner("Agents working... (15–30 seconds)"):
        try:
            from supervisor.workflow import app as agent_app
            result = agent_app.invoke({"messages": [("user", prompt_text)]})
            final_report = result["messages"][-1].content

            # Parse what each agent actually said
            agent_outputs = {}
            for msg in result["messages"]:
                name = getattr(msg, "name", None)
                content = msg.content if isinstance(msg.content, str) else ""
                if name and content.strip():
                    agent_outputs[name] = content

            step_placeholder.markdown("\n\n".join(
                f'<div class="agent-step">{s}</div>' for s in steps_log
            ), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Agent error: {e}")
            st.stop()

    # ── Step 3 — Supervisor Report ─────────────────────────────────────────────
    st.divider()
    st.markdown("### 3️⃣  Supervisor Report")
    st.markdown(f'<div class="report-box">{final_report}</div>', unsafe_allow_html=True)

    # Agent conversation detail
    with st.expander("📨 View full agent conversation"):
        for msg in result["messages"]:
            role    = getattr(msg, "name", None) or msg.__class__.__name__
            content = msg.content if isinstance(msg.content, str) else str(msg.content)
            if content.strip():
                st.markdown(f"**`{role}`**")
                st.markdown(content)
                st.divider()

    # ── Step 4 — Dashboard built from agent data ───────────────────────────────
    st.divider()
    st.markdown("### 4️⃣  Supporting Dashboard — Based on Agent Report")
    st.caption("Charts built from the data retrieved by the Portfolio Analyst, Market Researcher, and Risk & Compliance agents.")

    col_pie, col_bar = st.columns([1, 1.6])

    # Portfolio Allocation (from Portfolio Analyst)
    with col_pie:
        st.markdown('<div class="section-header">📊 Portfolio Analyst — Asset Allocation</div>', unsafe_allow_html=True)
        alloc_labels = ["Equity", "Debt", "Gold"]
        alloc_values = [p["equity"]["percentage"], p["debt"]["percentage"], p["gold"]["percentage"]]
        fig_pie = go.Figure(go.Pie(
            labels=alloc_labels,
            values=alloc_values,
            hole=0.55,
            marker_colors=["#4f8ef7", "#22c55e", "#f59e0b"],
            textinfo="label+percent",
            hovertemplate="%{label}: %{value}%<extra></extra>",
        ))
        fig_pie.update_layout(
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f0f4f8",
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", y=-0.1),
            annotations=[dict(text=p["total_value"], x=0.5, y=0.5,
                              font_size=12, showarrow=False, font_color="#f0f4f8")],
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Holdings bar (from Portfolio Analyst)
    with col_bar:
        st.markdown('<div class="section-header">📊 Portfolio Analyst — Equity Holdings</div>', unsafe_allow_html=True)
        holdings = p["equity"]["holdings"]
        stocks   = [h["stock"] for h in holdings]
        allocs   = [h["allocation"] for h in holdings]
        fig_bar  = go.Figure(go.Bar(
            x=allocs, y=stocks, orientation="h",
            marker_color="#4f8ef7",
            text=[f"{a}%" for a in allocs],
            textposition="outside",
        ))
        fig_bar.update_layout(
            xaxis=dict(title="Allocation (%)", showgrid=True, gridcolor="#2d3448"),
            yaxis=dict(autorange="reversed"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f0f4f8",
            margin=dict(t=10, b=10, l=10, r=60),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    col_gauge, col_market = st.columns([1, 1.6])

    # Risk gauge (from Risk & Compliance)
    with col_gauge:
        st.markdown('<div class="section-header">⚖️ Risk & Compliance — Suitability Check</div>', unsafe_allow_html=True)
        equity_pct = p["equity"]["percentage"]
        bench      = benchmarks.get(client["risk_profile"], {})
        max_eq     = bench.get("max_equity", 100)
        sharpe     = bench.get("sharpe_target", 1.0)

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=equity_pct,
            delta={"reference": max_eq, "suffix": "% vs limit"},
            title={"text": "Equity %", "font": {"color": "#f0f4f8"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#9aa5b4"},
                "bar":  {"color": "#4f8ef7"},
                "steps": [
                    {"range": [0, max_eq],   "color": "#1e2d1e"},
                    {"range": [max_eq, 100], "color": "#3d1e1e"},
                ],
                "threshold": {
                    "line": {"color": "#ef4444", "width": 3},
                    "thickness": 0.8,
                    "value": max_eq,
                },
            },
            number={"suffix": "%", "font": {"color": "#f0f4f8"}},
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#f0f4f8",
            margin=dict(t=30, b=10, l=20, r=20),
            height=250,
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        compliant = equity_pct <= max_eq
        if compliant:
            st.success(f"✅ Compliant — within {max_eq}% limit")
        else:
            st.error(f"⚠️ Non-compliant — {equity_pct}% exceeds {max_eq}% limit")

        st.metric("Sharpe Ratio Target", sharpe)
        volatility = round(10 + equity_pct * 0.15, 1)
        max_dd = round(-(equity_pct * 0.20), 1)
        st.metric("Est. Volatility", f"{volatility}%")
        st.metric("Max Drawdown Est.", f"{max_dd}%")

    # Market outlook (from Market Researcher)
    with col_market:
        st.markdown('<div class="section-header">🔍 Market Researcher — Sector Outlook</div>', unsafe_allow_html=True)
        sectors   = list(market_out.keys())
        outlooks  = [market_out[s]["outlook"] for s in sectors]
        risk_map  = {"Low": 1, "Low-Medium": 2, "Medium": 3,
                     "Medium-High": 4, "High": 5, "Very High": 6}
        risk_vals = [risk_map.get(market_out[s]["risk"], 3) for s in sectors]
        colors    = ["#22c55e" if v <= 2 else "#eab308" if v <= 3
                     else "#f97316" if v <= 4 else "#ef4444"
                     for v in risk_vals]

        fig_sector = go.Figure(go.Bar(
            x=sectors,
            y=risk_vals,
            marker_color=colors,
            text=outlooks,
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Risk Score: %{y}<br>%{text}<extra></extra>",
        ))
        fig_sector.update_layout(
            yaxis=dict(title="Risk Score (1=Low → 6=Very High)",
                       range=[0, 8], showgrid=True, gridcolor="#2d3448"),
            xaxis=dict(title="Sector"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f0f4f8",
            margin=dict(t=30, b=10),
        )
        st.plotly_chart(fig_sector, use_container_width=True)

        for sector, info in market_out.items():
            with st.expander(f"**{sector}** — {info['outlook']}"):
                st.markdown(info["summary"])
                st.markdown(f"💡 {info['recommendation']}")

elif run:
    st.warning("Please enter a question before running.")
