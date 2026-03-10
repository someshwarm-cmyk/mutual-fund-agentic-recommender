import streamlit as st
import pandas as pd

from src.data_loader import fetch_amfi_data
from src.data_processing import compute_metrics
from src.recommender import recommend_funds
from src.explanation import generate_explanation

from src.sip_simulator import (
    calculate_sip_growth,
    generate_sip_table,
    calculate_swp_growth,
    calculate_lumpsum_growth
)

from src.document_engine import (
    extract_amc,
    get_amc_document_link,
    get_scheme_document_search_link,
    get_amfi_scheme_link,
)

# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="AI Mutual Fund Advisor",
    layout="wide"
)

st.title("🤖 AI Mutual Fund Advisory Platform")

# -------------------------------------------------
# SIDEBAR - INVESTOR PROFILE
# -------------------------------------------------

st.sidebar.title("Investor Profile")

risk = st.sidebar.selectbox(
    "Risk Appetite",
    ["low", "medium", "high"]
)

horizon = st.sidebar.selectbox(
    "Investment Horizon",
    ["short", "medium", "long"]
)

investment_type = st.sidebar.selectbox(
    "Investment Type",
    ["sip", "lumpsum", "swp"]
)

fund_type = st.sidebar.selectbox(
    "Preferred Fund Type",
    ["All", "Equity", "Debt", "Gold", "Hybrid", "Others"]
)

top_n = st.sidebar.slider(
    "Number of Recommendations",
    3,
    10,
    5
)

# -------------------------------------------------
# FETCH DATA
# -------------------------------------------------

df = fetch_amfi_data()

if df is None or df.empty:

    st.error("AMFI data not available")

else:

    df = compute_metrics(df)

    # -------------------------------------------------
    # RECOMMENDATION ENGINE
    # -------------------------------------------------

    if st.button("Generate Recommendation"):

        recs, profile = recommend_funds(
            df,
            risk,
            horizon,
            investment_type,
            fund_type,
            top_n,
        )

        st.subheader(f"Investor Profile: {profile}")

        st.dataframe(
            recs[
                [
                    "Scheme Name",
                    "Fund Type",
                    "1Y Return (%)",
                    "3Y Return (%)",
                    "5Y Return (%)",
                    "10Y Return (%)",
                    "Sharpe Ratio",
                    "Volatility",
                    "Score"
                ]
            ]
        )

        # -------------------------------------------------
        # EXPLAINABLE AI SECTION
        # -------------------------------------------------

        st.markdown("## Explainable AI Insights")

        for _, row in recs.iterrows():

            fund_name = row["Scheme Name"]

            st.markdown(f"### {fund_name}")

            explanation = generate_explanation(
                row,
                risk,
                horizon,
                investment_type,
                fund_type
            )

            st.write(explanation)

            # -------------------------------------------------
            # DOCUMENT LINKS
            # -------------------------------------------------

            amc = extract_amc(fund_name)
            amc_link = get_amc_document_link(amc)

            if amc_link:
                st.markdown(f"[AMC Document Page]({amc_link})")

            search_link = get_scheme_document_search_link(fund_name)
            st.markdown(f"[Search Scheme Documents]({search_link})")

            scheme_code = row.get("Scheme Code")
            amfi_link = get_amfi_scheme_link(scheme_code)

            if amfi_link:
                st.markdown(f"[AMFI Scheme Page]({amfi_link})")

            st.divider()

# -------------------------------------------------
# SIP WEALTH SIMULATOR
# -------------------------------------------------

if investment_type == "sip":

    st.header("💰 SIP Wealth Simulator")

    sip_amount = st.number_input(
        "Monthly SIP (₹)",
        500,
        100000,
        5000
    )

    sip_years = st.slider(
        "Investment Years",
        1,
        40,
        15
    )

    sip_return = st.slider(
        "Expected Return (%)",
        1,
        20,
        12
    )

    if st.button("Simulate SIP"):

        r = sip_return / 100

        fv = calculate_sip_growth(
            sip_amount,
            sip_years,
            r
        )

        st.success(f"Future Value: ₹{fv:,.0f}")

        sip_df = generate_sip_table(
            sip_amount,
            sip_years,
            r
        )

        st.line_chart(
            sip_df.set_index("Month")["Portfolio Value"]
        )

# -------------------------------------------------
# LUMPSUM SIMULATOR
# -------------------------------------------------

if investment_type == "lumpsum":

    st.header("💵 Lumpsum Investment Simulator")

    principal = st.number_input(
        "Investment Amount (₹)",
        10000,
        10000000,
        100000
    )

    years = st.slider(
        "Investment Years",
        1,
        40,
        10
    )

    return_rate = st.slider(
        "Expected Return (%)",
        1,
        20,
        12
    )

    if st.button("Simulate Lumpsum"):

        r = return_rate / 100

        final_value, lump_df = calculate_lumpsum_growth(
            principal,
            years,
            r
        )

        st.success(f"Future Value: ₹{final_value:,.0f}")

        st.line_chart(
            lump_df.set_index("Month")["Portfolio Value"]
        )

# -------------------------------------------------
# SWP RETIREMENT SIMULATOR
# -------------------------------------------------

if investment_type == "swp":

    st.header("📤 Retirement SWP Simulator")

    corpus = st.number_input(
        "Initial Corpus (₹)",
        100000,
        100000000,
        5000000
    )

    withdrawal = st.number_input(
        "Monthly Withdrawal (₹)",
        5000,
        500000,
        30000
    )

    years = st.slider(
        "Retirement Years",
        1,
        40,
        20
    )

    swp_return = st.slider(
        "Return During Retirement (%)",
        1,
        15,
        8
    )

    if st.button("Simulate SWP"):

        r = swp_return / 100

        remaining, balances = calculate_swp_growth(
            corpus,
            withdrawal,
            years,
            r,
        )

        st.success(f"Remaining Corpus: ₹{remaining:,.0f}")

        swp_df = pd.DataFrame({
            "Month": range(1, len(balances) + 1),
            "Portfolio Value": balances
        })

        st.line_chart(
            swp_df.set_index("Month")["Portfolio Value"]
        )
