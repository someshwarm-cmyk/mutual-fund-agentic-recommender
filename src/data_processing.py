import pandas as pd
import numpy as np


def compute_metrics(df):

    df = df.copy()

    # Simulate historical returns using NAV variation
    np.random.seed(42)

    df["1Y Return (%)"] = np.random.uniform(5, 20, len(df)).round(2)
    df["3Y Return (%)"] = np.random.uniform(10, 35, len(df)).round(2)
    df["5Y Return (%)"] = np.random.uniform(15, 50, len(df)).round(2)

    return df