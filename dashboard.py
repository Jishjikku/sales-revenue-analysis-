import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales & Revenue Dashboard", page_icon="📊", layout="wide")

st.title("📊 Sales & Revenue Analysis Dashboard")
st.caption("Interactive analysis of sales, revenue, products, regions, and profit.")

@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

df = load_data()

st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
categories = st.sidebar.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
products = st.sidebar.multiselect("Product", sorted(df["Product"].unique()), default=sorted(df["Product"].unique()))

filtered = df[
    df["Region"].isin(regions)
    & df["Category"].isin(categories)
    & df["Product"].isin(products)
]

total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
total_quantity = filtered["Quantity"].sum()
orders = filtered["Order_ID"].nunique()
avg_order = total_sales / orders if orders else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"₹{total_sales:,.0f}")
c2.metric("Total Profit", f"₹{total_profit:,.0f}")
c3.metric("Units Sold", f"{total_quantity:,}")
c4.metric("Average Order Value", f"₹{avg_order:,.0f}")

st.divider()

left, right = st.columns(2)

monthly = filtered.groupby("Month", as_index=False)["Sales"].sum()
fig_month = px.line(monthly, x="Month", y="Sales", markers=True, title="Monthly Sales Trend")
left.plotly_chart(fig_month, use_container_width=True)

product_sales = filtered.groupby("Product", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
fig_product = px.bar(product_sales, x="Product", y="Sales", title="Sales by Product")
right.plotly_chart(fig_product, use_container_width=True)

left2, right2 = st.columns(2)

region_sales = filtered.groupby("Region", as_index=False)["Sales"].sum()
fig_region = px.pie(region_sales, names="Region", values="Sales", title="Sales by Region")
left2.plotly_chart(fig_region, use_container_width=True)

category_profit = filtered.groupby("Category", as_index=False)["Profit"].sum()
fig_profit = px.bar(category_profit, x="Category", y="Profit", title="Profit by Category")
right2.plotly_chart(fig_profit, use_container_width=True)

st.subheader("Top-Performing Products")
top = filtered.groupby("Product", as_index=False).agg(
    Sales=("Sales", "sum"),
    Quantity=("Quantity", "sum"),
    Profit=("Profit", "sum")
).sort_values("Sales", ascending=False)
st.dataframe(top, use_container_width=True, hide_index=True)

st.subheader("Filtered Sales Data")
st.dataframe(filtered.sort_values("Date", ascending=False), use_container_width=True, hide_index=True)
