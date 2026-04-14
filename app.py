import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Customer Dashboard", layout="wide")

st.markdown("""
<style>

.stApp {
    background: #0e1117;
}


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


section[data-testid="stSidebar"] {
    background: #0b1220;
    border-right: 1px solid #1f2937;
}

section[data-testid="stSidebar"] * {
    color: #d1d5db !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #93c5fd !important;
}

/*  KPI CARDS  */
[data-testid="stMetric"] {
    background: #111827;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1f2937;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}

[data-testid="stMetricValue"] {
    color: #93c5fd !important;
    font-weight: 700;
}

[data-testid="stMetricLabel"] {
    color: #9ca3af !important;
}

/*  TEXT  */
h1, h2, h3 {
    color: #e5e7eb !important;
}

p, label {
    color: #9ca3af !important;
}

/* DATAFRAME  */
[data-testid="stDataFrame"] {
    background-color: #111827 !important;
    border-radius: 10px;
    border: 1px solid #1f2937;
}

/* INPUTS  */
div[data-baseweb="select"] > div {
    background-color: #111827 !important;
    border: 1px solid #1f2937 !important;
    border-radius: 10px !important;
}

/* tags */
span[data-baseweb="tag"] {
    background-color: #374151 !important;
    color: #e5e7eb !important;
}

/*  BUTTONS  */
.stButton > button {
    background: #1f2937;
    color: #e5e7eb;
    border: 1px solid #374151;
    border-radius: 10px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #374151;
}

/* SLIDER */
.stSlider > div div div div {
    background-color: #60a5fa !important;
}

/* CHARTS */
[data-testid="stPlotlyChart"] {
    background-color: #111827;
    padding: 12px;
    border-radius: 12px;
    border: 1px solid #1f2937;
}

/* Plotly text fix */
.js-plotly-plot text {
    fill: #e5e7eb !important;
}

/* Grid softer */
.js-plotly-plot .gridlayer path {
    stroke: #1f2937 !important;
}

</style>
""", unsafe_allow_html=True) 
st.title("Customer Dashboard")



# Load Data

try:
    df_raw = pd.read_csv("messy_customer_data.csv")
    df_clean = pd.read_csv("cleaned_customer_data.csv")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()


# Sidebar Filters 

st.sidebar.title("Filters Panel")
st.sidebar.markdown("Use filters below to explore the data")

df_filtered = df_clean.copy()


# Country Filter

if "Country" in df_filtered.columns:
    st.sidebar.subheader("Country")

    country = st.sidebar.multiselect(
        "Select Country",
        options=sorted(df_filtered["Country"].dropna().unique()),
        default=sorted(df_filtered["Country"].dropna().unique())
    )

    df_filtered = df_filtered[df_filtered["Country"].isin(country)]


# Gender Filter

if "Gender" in df_filtered.columns:
    st.sidebar.subheader("Gender")

    gender = st.sidebar.multiselect(
        "Select Gender",
        options=sorted(df_filtered["Gender"].dropna().unique()),
        default=sorted(df_filtered["Gender"].dropna().unique())
    )

    df_filtered = df_filtered[df_filtered["Gender"].isin(gender)]

# Age Filter

if "Age" in df_filtered.columns:
    st.sidebar.subheader("Age Range")

    min_age = int(df_filtered["Age"].min())
    max_age = int(df_filtered["Age"].max())

    age_range = st.sidebar.slider(
        "Select Age Range",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age)
    )

    df_filtered = df_filtered[
        (df_filtered["Age"] >= age_range[0]) &
        (df_filtered["Age"] <= age_range[1])
    ]


# Purchase Filter

if "purchase_amount" in df_filtered.columns:
    st.sidebar.subheader("Purchase Amount")

    min_p = float(df_filtered["purchase_amount"].min())
    max_p = float(df_filtered["purchase_amount"].max())

    purchase_range = st.sidebar.slider(
        "Select Purchase Range",
        min_value=min_p,
        max_value=max_p,
        value=(min_p, max_p)
    )

    df_filtered = df_filtered[
        (df_filtered["purchase_amount"] >= purchase_range[0]) &
        (df_filtered["purchase_amount"] <= purchase_range[1])
    ]


# Info

st.sidebar.markdown("---")
st.sidebar.info("Filters update all charts automatically")


# Raw Data

st.header("Raw Data")
st.dataframe(df_raw.head(), width="stretch")
st.write("Dataset Shape:", df_raw.shape)


# Cleaned Data

st.header("Cleaned Data")
st.dataframe(df_clean.head(), width="stretch")
st.write("Shape After Cleaning:", df_clean.shape)


# KPIs

st.header("KPIs")

if "purchase_amount" in df_filtered.columns:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Customers", df_filtered.shape[0])

    with col2:
        st.metric("Total Revenue", round(df_filtered["purchase_amount"].sum(), 2))

    with col3:
        st.metric("Average Purchase", round(df_filtered["purchase_amount"].mean(), 2))
else:
    st.metric("Total Customers", df_filtered.shape[0])
# Clean filtered data

if "purchase_amount" in df_filtered.columns:
    df_filtered = df_filtered.dropna(subset=["purchase_amount"])


# Charts

st.header("Charts")

# Customers by Country
if "Country" in df_filtered.columns:
    country_counts = df_filtered["Country"].value_counts().reset_index()
    country_counts.columns = ["Country", "Count"]

    fig1 = px.bar(country_counts, x="Country", y="Count", title="Customers by Country")
    st.plotly_chart(fig1, width="stretch")

# Purchase Distribution
if "purchase_amount" in df_filtered.columns:
    fig2 = px.histogram(df_filtered, x="purchase_amount", nbins=30, title="Purchase Distribution")
    st.plotly_chart(fig2, width="stretch")

# Age vs Purchase
if "Age" in df_filtered.columns and "purchase_amount" in df_filtered.columns:

    fig4 = px.scatter(
        df_filtered,
        x='Age',
        y='purchase_amount',
        title='Age vs Purchase Amount',
        color='Gender',
        opacity=0.7,
        size='purchase_amount',
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig4.update_layout(
        title_x=0,
        plot_bgcolor='white'
    )

    fig4.update_traces(marker=dict(line=dict(width=0.5, color='DarkSlateGray')))

    st.plotly_chart(fig4, width="stretch")

# Purchase by Gender
if "Gender" in df_filtered.columns and "purchase_amount" in df_filtered.columns:
    fig4 = px.box(df_filtered, x="Gender", y="purchase_amount", title="Purchase by Gender")
    st.plotly_chart(fig4, width="stretch")

# Monthly Trend
if "Signup_Date" in df_filtered.columns and "purchase_amount" in df_filtered.columns:

    df_filtered["Signup_Date"] = pd.to_datetime(df_filtered["Signup_Date"], errors="coerce")
    df_filtered["YearMonth"] = df_filtered["Signup_Date"].dt.to_period("M")

    monthly = df_filtered.groupby("YearMonth")["purchase_amount"].sum().reset_index()
    monthly["YearMonth"] = monthly["YearMonth"].astype(str)

    if not monthly.empty:
        fig5 = px.line(monthly, x="YearMonth", y="purchase_amount", title="Monthly Revenue Trend")
        st.plotly_chart(fig5, width="stretch")

# Correlation Heatmap 
numeric_df = df_filtered.select_dtypes(include=['number'])
corr = numeric_df.corr()

if not corr.empty:

    fig_corr = px.imshow(
        corr,
        text_auto=".2f",
        title='Correlation Heatmap',
        color_continuous_scale='Blues',
        zmin=-1,
        zmax=1
    )

    fig_corr.update_layout(
        title_x=0,
        plot_bgcolor='white'
    )

    st.plotly_chart(fig_corr, use_container_width=True)
