import pandas as pd
import numpy as np

def calculate_sip_growth(monthly_investment, years, annual_return):

    months = years * 12
    monthly_rate = annual_return / 12

    if monthly_rate == 0:
        return monthly_investment * months

    future_value = monthly_investment * (
        ((1 + monthly_rate) ** months - 1) / monthly_rate
    ) * (1 + monthly_rate)

    return round(future_value, 2)


def generate_sip_table(monthly_investment, years, annual_return):

    data = []
    total_invested = 0
    current_value = 0

    monthly_rate = annual_return / 12

    for month in range(1, years * 12 + 1):

        total_invested += monthly_investment
        current_value = (current_value + monthly_investment) * (1 + monthly_rate)

        data.append({
            "Month": month,
            "Total Invested": total_invested,
            "Portfolio Value": round(current_value, 2)
        })

    return pd.DataFrame(data)