
import streamlit as st
import pandas as pd
import plotly.express as px

# Configure dashboard
st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/retail_sales.csv")

    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    return df


df = load_data()

# Dashboard heading
st.title("Retail Sales & Pricing Analytics")
st.caption("Retail performance analysis | 2023–2024")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

categories = st.sidebar.multiselect(
    "Product Category",
    options=df["Product Category"].unique(),
    default=df["Product Category"].unique()
)

# Filter dataset
filtered_df = df[
    df["Product Category"].isin(categories)
]

# KPI calculations
total_revenue = filtered_df["Total Amount"].sum()
total_transactions = len(filtered_df)
total_units = filtered_df["Quantity"].sum()
average_transaction = filtered_df["Total Amount"].mean()

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Transactions", f"{total_transactions:,}")
col3.metric("Units Sold", f"{total_units:,}")
col4.metric("Average Sale", f"${average_transaction:,.2f}")

st.divider()

# Revenue by category
st.subheader("Revenue by Product Category")

category_sales = (
    filtered_df.groupby("Product Category")["Total Amount"]
    .sum()
    .reset_index()
)

fig = px.bar(
    category_sales,
    x="Product Category",
    y="Total Amount",
    title="Revenue by Category",
    labels={
        "Total Amount": "Revenue ($)",
        "Product Category": "Category"
    },
    text_auto=",.0f"
)

st.plotly_chart(fig, use_container_width=True)
