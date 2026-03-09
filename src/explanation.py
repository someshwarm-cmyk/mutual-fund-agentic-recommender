def generate_explanation(row, risk, horizon, investment_type, fund_type):

    fund_name = row["Scheme Name"]

    ret_1y = row.get("1Y Return (%)", "N/A")
    ret_3y = row.get("3Y Return (%)", "N/A")
    sharpe = row.get("Sharpe Ratio", "N/A")
    vol = row.get("Volatility", "N/A")

    explanation = f"""
{fund_name} is recommended because:

• It matches your **{risk} risk appetite**.
• Suitable for a **{horizon} investment horizon**.
• Aligns with your **{fund_type} fund preference**.

Performance indicators:

• 1 Year Return: {ret_1y}%
• 3 Year Return: {ret_3y}%
• Sharpe Ratio: {sharpe}
• Volatility: {vol}

Higher Sharpe ratio indicates better risk-adjusted performance,
making this fund suitable for your investment strategy.
"""

    return explanation