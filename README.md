# 📊 Agentic AI Mutual Fund Recommender

An intelligent mutual fund recommendation system powered by live AMFI NAV data, historical analytics, risk-adjusted scoring, and SIP growth simulation.

Built using:
- Python
- Streamlit
- Pandas
- NumPy

---
## App Link
https://mutual-fund-agentic-recommender.streamlit.app/

## 🚀 Live Features

✅ Live NAV data from AMFI  
✅ Automatic historical NAV storage  
✅ Risk-based fund recommendation  
✅ Category filtering (Equity, Debt, Gold, Hybrid)  
✅ Sharpe Ratio-based scoring  
✅ Risk alignment scoring  
✅ SIP Growth Simulator  
✅ Explainable AI reasoning  

---

## 📁 Project Structure
mutual-fund-agentic-recommender/
│
├── data/
│ └── nav_history.csv
│
├── src/
│ ├── data_loader.py
│ ├── data_processing.py
│ ├── historical_storage.py
│ ├── recommender.py
│ ├── sip_simulator.py
│
├── app.py
├── requirements.txt
└── README.md

---

## ⚙️ How It Works

### 1️⃣ Live Data Fetching
The system fetches real-time NAV data from AMFI:

- Parses raw text file
- Extracts scheme code, scheme name, NAV, date
- Automatically classifies funds into categories

---

### 2️⃣ Historical Storage Engine

Every time the app runs:

- Today’s NAV is appended to `nav_history.csv`
- Duplicate entries for the same day are removed
- NAV is converted to numeric
- Invalid rows are discarded

This allows time-series performance analysis.

---

### 3️⃣ Time-Series Analytics Engine

Using historical NAV:

- Daily returns are computed
- Annualized return is calculated
- Annualized volatility is computed
- Sharpe Ratio is calculated:

```
Sharpe = (Annual Return - Risk Free Rate) / Volatility
```

Funds with insufficient history are skipped.

---

### 4️⃣ Risk Alignment Model

Each fund is assigned a risk score based on keywords:

| Fund Type | Risk Score |
|-----------|------------|
| Small Cap | 1.0 |
| Mid Cap   | 0.85 |
| Large Cap | 0.6 |
| Liquid    | 0.1 |
| Others    | 0.5 |

User risk mapping:

| User Input | Risk Value |
|------------|-----------|
| Low        | 0.2 |
| Medium     | 0.6 |
| High       | 1.0 |

Risk Alignment Formula:

```
1 - abs(Fund_Risk - User_Risk)
```

---

### 5️⃣ Final Recommendation Score

Funds are ranked using:

```
Score = 0.6 × Sharpe Ratio + 0.4 × Risk Alignment
```

Top N funds are returned.

---

### 6️⃣ SIP Growth Simulator

Uses compound interest formula:

```
Future Value = SIP × [((1+r)^n - 1)/r] × (1+r)
```

Displays:
- Total Invested
- Future Value
- Wealth Gained
- Growth chart

---

## 🧠 Explainable AI Layer

For every recommended fund:

- Risk match explanation
- Investment horizon consideration
- Risk-adjusted performance shown
- Final score transparency

---

## 🔧 Installation

``
git clone https://github.com/your-username/mutual-fund-agentic-recommender.git
cd mutual-fund-agentic-recommender
pip install -r requirements.txt
streamlit run app.py``

## 🎯 Use Cases

Retail Investors

Financial Advisors

FinTech Learning Projects

Portfolio Analytics Demonstration

## 📌 Future Improvements

Rolling 1Y CAGR

Max Drawdown

Beta vs Index

Portfolio allocation optimizer

AI-based allocation suggestions

Deployment on Streamlit Cloud

## 👨‍💻 Author

Someshwar M
Data Analytics



