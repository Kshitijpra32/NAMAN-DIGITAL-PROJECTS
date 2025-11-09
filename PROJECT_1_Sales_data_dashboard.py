#IMPORT MODULES
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt


# TITLE
st.title("📊 Sales Data Dashboard (Python + Streamlit)")
st.write("Analyze sales trends & patterns with sample generated data.")


# SAMPLE DATA GENERATION
st.subheader("Generate Sample Sales Data")

num_rows = st.slider("Select number of sample rows", min_value=50, max_value=1000, value=300)

np.random.seed(42)
data = pd.DataFrame({
    "InvoiceDate": pd.date_range(start="2024-01-01", periods=num_rows, freq="D"),
    "Region": np.random.choice(["North", "South", "East", "West"], num_rows),
    "Product": np.random.choice(["Laptop", "Headphones", "Mobile", "Camera"], num_rows),
    "Sales": np.random.randint(2000, 50000, num_rows)
})

# Display data table
st.subheader("📁 Sales Dataset Preview")
st.dataframe(data, use_container_width=True)


# FILTERS
st.subheader("Filter Records")
region_filter = st.multiselect("Filter by Region", options=data["Region"].unique(), default=data["Region"].unique())
product_filter = st.multiselect("Filter by Product", options=data["Product"].unique(), default=data["Product"].unique())

filtered_data = data[(data["Region"].isin(region_filter)) & (data["Product"].isin(product_filter))]
st.write(f"Total Rows after filter: {len(filtered_data)}")
st.dataframe(filtered_data, use_container_width=True)


# SALES TREND (Altair chart)
st.subheader("📈 Sales Trend Over Time (Improved View)")
sales_trend = filtered_data.groupby("InvoiceDate")["Sales"].sum().reset_index()
line_chart = alt.Chart(sales_trend).mark_line(point=True).encode(
    x="InvoiceDate:T",
    y="Sales:Q",
    tooltip=["InvoiceDate", "Sales"]
).interactive()

st.altair_chart(line_chart, use_container_width=True)


# SALES BY REGION (BAR CHART)
st.subheader("📊 Sales by Region")
region_sales = filtered_data.groupby("Region")["Sales"].sum()
fig2, ax2 = plt.subplots()
ax2.bar(region_sales.index, region_sales.values)
ax2.set_xlabel("Region")
ax2.set_ylabel("Total Sales")
st.pyplot(fig2)


# SALES BY PRODUCT (BAR CHART)
st.subheader("📦 Sales by Product")
product_sales = filtered_data.groupby("Product")["Sales"].sum()
fig3, ax3 = plt.subplots()
ax3.bar(product_sales.index, product_sales.values)
ax3.set_xlabel("Product")
ax3.set_ylabel("Total Sales")
st.pyplot(fig3)
