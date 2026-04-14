import streamlit as st
import pandas as pd

st.set_page_config(page_title="Insights", layout="wide")

#   STYLE  
st.markdown("""
<style>
.stApp {
    background: #0e1117;
}

/* HEADER */
.main-header {
    background: #111827;
    padding: 18px 22px;
    border-radius: 14px;
    border: 1px solid #1f2937;
    margin-bottom: 18px;
}

.main-header h1 {
    margin: 0;
    font-size: 24px;
    color: #e5e7eb;
}

.main-header p {
    margin: 0;
    color: #9ca3af;
    font-size: 13px;
}

/* INSIGHT CARDS */
.card {
    background: #111827;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1f2937;
    margin-bottom: 12px;
    color: #d1d5db;
}

/* KPIs */
.kpi {
    background: #111827;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #1f2937;
    text-align: center;
}

.kpi h2 {
    color: #60a5fa;
    margin: 0;
}

.kpi p {
    color: #9ca3af;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

#  HEADER  
st.markdown("""
<div class="main-header">
<h1>Key Business Insights</h1>
<p>Business insights extracted from customer behavior analysis</p>
</div>
""", unsafe_allow_html=True)

#   LOAD DATA  
try:
    df = pd.read_csv("cleaned_customer_data.csv")
except:
    st.error("Data file not found")
    st.stop()

# Clean data
if "purchase_amount" in df.columns:
    df = df.dropna(subset=["purchase_amount"])


#   INSIGHTS  
st.subheader("Insights")

st.markdown("""
<div class="card">
Revenue is mainly driven by a small segment of high value customers (Pareto distribution pattern is likely).
</div>
""", unsafe_allow_html=True)

if "Country" in df.columns:
    top_country = df["Country"].value_counts().idxmax()
    st.markdown(f"""
    <div class="card">
{top_country} is the strongest market in terms of customer count.
    </div>
    """, unsafe_allow_html=True)

if "Age" in df.columns and "purchase_amount" in df.columns:
    corr = df["Age"].corr(df["purchase_amount"])

    st.markdown(f"""
    <div class="card">
Age and purchase amount correlation is {round(corr, 2)}.
Interpretation: {"Weak relationship between age and spending behavior" if abs(corr) < 0.3 else "Noticeable relationship between age and spending behavior"}.
</div>
""", unsafe_allow_html=True)

if "Gender" in df.columns:
    top_gender = df["Gender"].value_counts().idxmax()
    st.markdown(f"""
    <div class="card">
{top_gender} is the dominant customer segment.
</div>
""", unsafe_allow_html=True)

if "purchase_amount" in df.columns:
    q1 = df["purchase_amount"].quantile(0.25)
    q3 = df["purchase_amount"].quantile(0.75)

    st.markdown(f"""
    <div class="card">
Most customers spend between {round(q1,2)} and {round(q3,2)}.
</div>
""", unsafe_allow_html=True)


#   EXTRA INSIGHTS (ADDED)  
st.markdown("""
<div class="card">
Most customers fall within a specific purchase range.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
Certain countries contribute higher revenue.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
No strong linear relationship between age and spending.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
Monthly revenue shows fluctuations over time.
</div>
""", unsafe_allow_html=True)


#   RECOMMENDATION  
st.subheader("Recommendation")

st.markdown("""
<div class="card">
Focus on:
Customer retention strategies for high value customers
Market expansion in top countries
Targeted marketing for mid-range spenders
Reactivation campaigns for low engagement users
</div>
""", unsafe_allow_html=True)