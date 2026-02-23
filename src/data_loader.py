import requests
import pandas as pd

AMFI_URL = "https://www.amfiindia.com/spages/NAVAll.txt"


def fetch_amfi_data():
    try:
        response = requests.get(AMFI_URL, timeout=10)

        if response.status_code != 200:
            return None

        return parse_nav_text(response.text)

    except Exception:
        return None


def parse_nav_text(text):

    lines = text.splitlines()

    data = []
    current_category = "Other"

    for line in lines:

        # Detect Category Sections
        if "Open Ended Schemes" in line:
            lower = line.lower()

            if "equity" in lower:
                current_category = "Equity"
            elif "debt" in lower:
                current_category = "Debt"
            elif "gold" in lower:
                current_category = "Gold"
            elif "hybrid" in lower:
                current_category = "Hybrid"
            else:
                current_category = "Other"

            continue

        # Parse Scheme Rows
        if ";" in line:
            parts = line.split(";")

            if len(parts) >= 6:
                try:
                    scheme_code = parts[0].strip()
                    scheme_name = parts[3].strip()  # ✅ CORRECT INDEX
                    nav = float(parts[4].strip())
                    date = parts[5].strip()

                    data.append([
                        scheme_code,
                        scheme_name,
                        nav,
                        date,
                        current_category
                    ])

                except:
                    continue

    df = pd.DataFrame(data, columns=[
        "Scheme Code",
        "Scheme Name",
        "NAV",
        "Date",
        "Category"
    ])

    return df


def parse_uploaded_file(uploaded_file):
    text = uploaded_file.read().decode("utf-8")
    return parse_nav_text(text)