import streamlit as st
import pandas as pd

from src.data_loader import fetch_amfi_data
from src.data_processing import compute_metrics
from src.recommender import recommend_funds
from src.historical_storage import update_nav_history

# =========================
# PAGE CONFIG (FIRST ALWAYS)
# =========================

st.set_page_config(
    page_title="Agentic Mutual Fund Recommender",
    layout="wide"
)

# =========================
# FETCH NAV DATA (ONLY ONCE)
# =========================

df = fetch_amfi_data()

if df is not None and not df.empty:
    try:
        update_nav_history(df)
    except Exception as e:
        st.warning("Historical storage update failed.")

# =========================
# SIDEBAR
# =========================

st.sidebar.title("Investor Preferences")

risk = st.sidebar.selectbox("Risk Appetite", ["low", "medium", "high"])
horizon = st.sidebar.selectbox("Investment Horizon", ["short", "medium", "long"])
investment_type = st.sidebar.selectbox("Investment Type", ["sip", "lumpsum"])
fund_type = st.sidebar.selectbox(
    "Preferred Fund Type",
    ["All", "Equity", "Debt", "Gold", "Hybrid"]
)
top_n = st.sidebar.slider("Number of Recommendations", 3, 15, 5)

# =========================
# MAIN TITLE
# =========================

st.title("📊 Agentic AI Mutual Fund Recommender")
st.write("Live NAV powered by AMFI")

# =========================
# ERROR HANDLING
# =========================

if df is None or df.empty:
    st.error("AMFI server busy. Please try again later.")
else:

    # Optional: compute extra metrics (if still needed)
    df = compute_metrics(df)

    if st.button("Generate Recommendation"):

        recommendations, profile = recommend_funds(
            df,
            risk,
            horizon,
            investment_type,
            fund_type,
            top_n,
        )

        st.markdown(f"## 🧠 Investor Profile: **{profile}**")

        if recommendations.empty:
            st.warning("No funds found for selected category.")
        else:

            # =========================
            # TABLE DISPLAY
            # =========================

            st.subheader("📈 Top Recommended Funds")

            display_columns = [
                "Scheme Name",
                "Category",
                "NAV",
                "Score"
            ]

            # Add return columns only if they exist
            for col in [
                "1Y Return (%)",
                "3Y Return (%)",
                "5Y Return (%)",
                "Annualized Return",
                "Volatility",
                "Sharpe Ratio"
            ]:
                if col in recommendations.columns:
                    display_columns.append(col)

            st.dataframe(
                recommendations[display_columns],
                use_container_width=True,
            )

            # =========================
            # EXPLAINABLE AI SECTION
            # =========================

            st.markdown("## 🔍 Why These Funds Were Recommended")

            for _, row in recommendations.iterrows():

                st.markdown(f"### {row['Scheme Name']}")

                explanation = f"""
                • Risk alignment matched your **{risk}** profile  
                • Investment horizon considered: **{horizon} term**  
                • Investment type: **{investment_type.upper()}**  
                • Final Score: **{round(row['Score'], 3)}**
                """

                if "Sharpe Ratio" in row:
                    explanation += f"\n• Risk-adjusted performance (Sharpe): **{round(row['Sharpe Ratio'], 3)}**"

                if "Volatility" in row:
                    explanation += f"\n• Annualized Volatility: **{round(row['Volatility'], 3)}**"

                st.write(explanation)
                st.divider()

from src.sip_simulator import calculate_sip_growth, generate_sip_table

st.markdown("## 📈 SIP Growth Simulator")

col1, col2, col3 = st.columns(3)

with col1:
    sip_amount = st.number_input("Monthly SIP Amount (₹)", min_value=500, value=5000)

with col2:
    sip_years = st.slider("Investment Duration (Years)", 1, 30, 5)

with col3:
    expected_return = st.slider("Expected Annual Return (%)", 1, 25, 12)

if st.button("Simulate SIP Growth"):

    annual_return_decimal = expected_return / 100

    future_value = calculate_sip_growth(
        sip_amount,
        sip_years,
        annual_return_decimal
    )

    total_invested = sip_amount * sip_years * 12
    wealth_gain = future_value - total_invested

    st.success(f"Future Value: ₹{future_value:,.0f}")
    st.info(f"Total Invested: ₹{total_invested:,.0f}")
    st.info(f"Wealth Gained: ₹{wealth_gain:,.0f}")

    # Growth chart
    sip_df = generate_sip_table(
        sip_amount,
        sip_years,
        annual_return_decimal
    )

    st.line_chart(sip_df.set_index("Month")[["Total Invested", "Portfolio Value"]])                