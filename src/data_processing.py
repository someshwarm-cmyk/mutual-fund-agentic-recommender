import pandas as pd
import numpy as np


def classify_fund_type(name):

    name = str(name).lower()

    if "equity" in name:
        return "Equity"

    elif "debt" in name or "bond" in name:
        return "Debt"

    elif "gold" in name:
        return "Gold"

    elif "hybrid" in name or "balanced" in name:
        return "Hybrid"

    else:
        return "Others"


def compute_metrics(df):

    df = df.copy()

    # -------------------------
    # Fund Type
    # -------------------------

    df["Fund Type"] = df["Scheme Name"].apply(classify_fund_type)

    # -------------------------
    # Generate realistic returns
    # -------------------------

    np.random.seed(42)

    df["1Y Return (%)"] = np.random.uniform(5, 25, len(df))
    df["3Y Return (%)"] = np.random.uniform(6, 20, len(df))
    df["5Y Return (%)"] = np.random.uniform(7, 18, len(df))
    df["10Y Return (%)"] = np.random.uniform(8, 16, len(df))

    # -------------------------
    # Volatility
    # -------------------------

    df["Volatility"] = np.random.uniform(4, 15, len(df))

    # -------------------------
    # Sharpe Ratio
    # -------------------------

    df["Sharpe Ratio"] = df["3Y Return (%)"] / df["Volatility"]

    return df