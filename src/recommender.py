import pandas as pd
import numpy as np
import os

HISTORY_FILE = "data/nav_history.csv"


def get_keyword_risk(name: str) -> float:
    name = name.lower()

    if "small cap" in name:
        return 1.0
    elif "mid cap" in name:
        return 0.85
    elif "large cap" in name:
        return 0.6
    elif "psu" in name:
        return 0.3
    elif "liquid" in name:
        return 0.1
    elif "etf" in name:
        return 0.6
    else:
        return 0.5


def compute_time_series_metrics():

    if not os.path.exists(HISTORY_FILE):
        return pd.DataFrame()

    history = pd.read_csv(HISTORY_FILE)

    if history.empty:
        return pd.DataFrame()

    history["Date"] = pd.to_datetime(history["Date"])
    history = history.sort_values(["Scheme Name", "Date"])

    results = []

    for scheme, group in history.groupby("Scheme Name"):

        group = group.sort_values("Date")
        nav_series = group["NAV"]

        daily_returns = nav_series.pct_change().dropna()

        if len(daily_returns) < 20:
            continue

        mean_daily = daily_returns.mean()
        annual_return = (1 + mean_daily) ** 252 - 1

        volatility = daily_returns.std() * np.sqrt(252)

        if volatility == 0:
            sharpe = 0
        else:
            sharpe = (annual_return - 0.06) / volatility

        results.append({
            "Scheme Name": scheme,
            "Annualized Return": round(annual_return, 4),
            "Volatility": round(volatility, 4),
            "Sharpe Ratio": round(sharpe, 4)
        })

    return pd.DataFrame(results)

def recommend_funds(df, risk, horizon, investment_type, fund_type, top_n):

    df = df.copy()

    if fund_type != "All":
        df = df[df["Category"] == fund_type]

    if df.empty:
        return df, "No Matching Funds"

    # Compute dynamic metrics
    metrics_df = compute_time_series_metrics()

    if not metrics_df.empty:
        df = df.merge(metrics_df, on="Scheme Name", how="left")

    # Ensure analytics columns always exist
    if "Sharpe Ratio" not in df.columns:
        df["Sharpe Ratio"] = 0

    if "Annualized Return" not in df.columns:
        df["Annualized Return"] = 0

    if "Volatility" not in df.columns:
        df["Volatility"] = 0

    df["Sharpe Ratio"] = df["Sharpe Ratio"].fillna(0)

    # Risk mapping
    user_risk_map = {"low": 0.2, "medium": 0.6, "high": 1.0}
    user_risk = user_risk_map.get(risk, 0.5)

    df["Fund_Risk"] = df["Scheme Name"].apply(get_keyword_risk)
    df["Risk_Alignment"] = 1 - abs(df["Fund_Risk"] - user_risk)

    # Risk-adjusted scoring
    df["Score"] = (
        0.6 * df["Sharpe Ratio"] +
        0.4 * df["Risk_Alignment"]
    )

    df = df.sort_values(by="Score", ascending=False)

    profile = {
        "low": "Conservative",
        "medium": "Balanced",
        "high": "Aggressive"
    }.get(risk, "Balanced")

    return df.head(top_n), profile