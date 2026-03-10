def generate_explanation(row, risk, horizon, investment_type, fund_type):

    fund = row["Scheme Name"]
    sharpe = row["Sharpe Ratio"]
    volatility = row["Volatility"]
    score = row["Score"]

    explanation = f"""
- **Investment Type:** {investment_type.upper()}
- **Risk Profile:** Suitable for a {risk} risk investor
- **Investment Horizon:** {horizon} term investment
- **Sharpe Ratio:** {sharpe:.2f} indicating strong risk-adjusted returns
- **Volatility:** {volatility:.2f} showing the level of risk fluctuation
- **Overall Score:** {score:.2f} based on return, volatility, and Sharpe ratio
- **Recommendation Reason:** This fund aligns well with the selected investment strategy and investor profile.
"""

    return explanation
