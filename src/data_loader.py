import pandas as pd
import requests
from io import StringIO


def fetch_amfi_data():

    url = "https://www.amfiindia.com/spages/NAVAll.txt"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.text

        df = pd.read_csv(
            StringIO(data),
            sep=";",
            header=None,
            names=[
                "Scheme Code",
                "ISIN Div Payout",
                "ISIN Div Reinvestment",
                "Scheme Name",
                "NAV",
                "Date",
            ],
        )

        df = df[df["Scheme Code"].notna()]

        df["NAV"] = pd.to_numeric(df["NAV"], errors="coerce")

        return df

    except Exception as e:
        print("Error fetching AMFI data:", e)
        return None