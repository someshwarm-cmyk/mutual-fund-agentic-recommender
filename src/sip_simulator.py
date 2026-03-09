import pandas as pd


def calculate_sip_growth(sip_amount, years, annual_return):

    months = years * 12
    monthly_rate = annual_return / 12

    value = 0

    for i in range(months):
        value = (value + sip_amount) * (1 + monthly_rate)

    return value


def generate_sip_table(sip_amount, years, annual_return):

    months = years * 12
    monthly_rate = annual_return / 12

    value = 0
    data = []

    for m in range(1, months + 1):

        value = (value + sip_amount) * (1 + monthly_rate)

        data.append({
            "Month": m,
            "Portfolio Value": value
        })

    return pd.DataFrame(data)


def calculate_swp_growth(initial_corpus, withdrawal, years, annual_return):

    months = years * 12
    monthly_rate = annual_return / 12

    corpus = initial_corpus
    balances = []

    for m in range(months):

        corpus = corpus * (1 + monthly_rate)
        corpus -= withdrawal

        if corpus < 0:
            corpus = 0

        balances.append(corpus)

    return corpus, balances