# Sample Questions — Fidelity Portfolio Review Supervisor

To try any question, replace `client_input` in `main.py` with the text below.

---

## Single Agent Questions

### Portfolio Analyst
```
Client: Priya Mehta (Client ID: C002)
What is her current portfolio allocation? Is she over-invested in any single sector?
```

```
Client: Arjun Nair (Client ID: C003)
Show me the current holdings breakdown and total portfolio value.
```

---

### Market Researcher
```
Research the Pharma and FMCG sector outlook for the next 6 months.
Should a conservative investor increase exposure to these sectors?
```

```
What is the current market outlook for the IT sector?
Is now a good time to buy or reduce TCS and Infosys positions?
```

---

### Risk & Compliance
```
Client: Rahul Sharma (Client ID: C001)
Run a risk assessment on his portfolio. Is the current risk level suitable for a 60-year-old retiree?
```

```
Assess the portfolio risk metrics and flag any compliance concerns for a client
who is a government employee with restrictions on equity trading.
```

---

## Multi-Agent Questions (Best for Demo)

### Quarterly Review
```
Client: Rahul Sharma (Client ID: C001, High Net Worth, retiring in 3 years)
Do a full quarterly portfolio review:
1. Fetch current holdings and check if the equity allocation is too high given the retirement horizon.
2. Research the Banking and IT sector outlook.
3. Assess the portfolio risk level and check if it suits a client approaching retirement.
4. Recommend whether to rebalance and what specific changes to make.
```

### Stress Test Scenario
```
Client: Rahul Sharma (Client ID: C001)
Run a stress test scenario: if the IT sector drops 20% and Banking drops 15%,
what is the impact on the portfolio? Check the risk metrics and recommend
defensive moves to protect capital.
```

### Aggressive Growth Review
```
Client: Sneha Kapoor (Client ID: C004, Age 28, High Risk Appetite)
She wants to grow her portfolio aggressively over the next 10 years.
Check current holdings, research IT and Pharma sector growth outlook,
assess if her current risk level is aligned with her goals,
and suggest how to reposition the portfolio for maximum growth.
```

### Pre-Retirement Shift
```
Client: Vikram Sinha (Client ID: C005, Age 57, retiring in 5 years)
He currently holds 70% equity. Review his holdings, check the Banking sector outlook,
assess if his risk level is appropriate, and create a step-by-step plan
to gradually shift to a capital-preservation portfolio before retirement.
```

### Sector Rotation Strategy
```
Client: Rahul Sharma (Client ID: C001)
The client wants to rotate out of Banking and into Pharma and Gold.
Research both sector outlooks, check current portfolio exposure,
assess the risk impact of this rotation, and give a final buy/sell recommendation.
```

### Compliance Check
```
Client: Anita Desai (Client ID: C006, NRI client)
Check her current portfolio holdings, assess the risk level,
and confirm whether the portfolio structure is compliant with FEMA and RBI
regulations applicable to NRI investors. Flag any issues.
```

---

## How to Use

1. Open `main.py`
2. Replace the `client_input` string with any question above
3. Run:
   ```bash
   source venv/bin/activate && python main.py
   ```

---

## Current Provider
Configured in `config/settings.py` → `PROVIDER = "mistral"` (working)

| Provider  | Status              |
|-----------|---------------------|
| Mistral   | Active              |
| Groq      | Resets midnight UTC |
| Google    | New key needed      |
| OpenAI    | Billing required    |
