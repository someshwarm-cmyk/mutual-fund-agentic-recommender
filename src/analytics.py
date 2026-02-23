import pandas as pd
import numpy as np


def calculate_annualized_return(nav_series):

    nav_series = nav_series.sort_index()

    daily_returns = nav_series.pct_change().dropna()

    if len(daily_returns) == 0:
        return 0

    mean_daily_return = daily_returns.mean()

    annualized_return = (1 + mean_daily_return) ** 252 - 1

    return annualized_return

def calculate_volatility(nav_series):

    daily_returns = nav_series.pct_change().dropna()

    if len(daily_returns) == 0:
        return 0

    return daily_returns.std() * np.sqrt(252)

def calculate_sharpe_ratio(nav_series, risk_free_rate=0.06):

    annual_return = calculate_annualized_return(nav_series)
    volatility = calculate_volatility(nav_series)

    if volatility == 0:
        return 0

    return (annual_return - risk_free_rate) / volatility