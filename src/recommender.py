import pandas as pd


def recommend_funds(df, risk, horizon, investment_type, fund_type, top_n):

    df = df.copy()

    # -----------------------------
    # Risk Filtering
    # -----------------------------

    if risk == "low":
        df = df[df["Volatility"] < 8]

    elif risk == "medium":
        df = df[(df["Volatility"] >= 6) & (df["Volatility"] <= 12)]

    else:
        df = df[df["Volatility"] > 8]

    # -----------------------------
    # Fund Type Filtering
    # -----------------------------

    if fund_type != "All":

        df = df[df["Fund Type"] == fund_type]

    # -----------------------------
    # SWP Preference
    # -----------------------------

    if investment_type == "swp":

        df = df[df["Fund Type"].isin(["Debt", "Hybrid"])]

    # -----------------------------
    # AI Score Calculation
    # -----------------------------

    df["Score"] = (
        df["1Y Return (%)"] * 0.20
        + df["3Y Return (%)"] * 0.25
        + df["5Y Return (%)"] * 0.25
        + df["10Y Return (%)"] * 0.15
        + df["Sharpe Ratio"] * 0.15
    )

    df = df.sort_values("Score", ascending=False)

    recommendations = df.head(top_n)

    profile = f"{risk} risk | {horizon} horizon | {investment_type} | {fund_type}"

    return recommendations, profile