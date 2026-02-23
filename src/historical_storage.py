import os
import pandas as pd
from datetime import datetime


HISTORY_FILE = "data/nav_history.csv"


def update_nav_history(current_df):
    """
    Appends today's NAV data into historical storage.
    """

    today = datetime.today().strftime("%Y-%m-%d")

    current_df = current_df.copy()
    current_df["Date"] = today

    # If file does not exist, create it
    if not os.path.exists(HISTORY_FILE):
        current_df.to_csv(HISTORY_FILE, index=False)
        return

    history_df = pd.read_csv(HISTORY_FILE)

    # Remove today's data if already exists (avoid duplicates)
    history_df = history_df[history_df["Date"] != today]

    updated_df = pd.concat([history_df, current_df], ignore_index=True)

    updated_df.to_csv(HISTORY_FILE, index=False)