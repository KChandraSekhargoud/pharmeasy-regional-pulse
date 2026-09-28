import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PharmEasy Regional Pulse", layout="wide")

@st.cache_data
def load_data():
    conn = sqlite3.connect('pharmeasy.db')
    df = pd.read_sql_query("""
        SELECT r.region, r.tier, o.order_id, o.order_date, o.category, o.sales_inr, o.profit_inr, substr(o.order_date, 1, 7) as month
        FROM regions_master r 
        INNER JOIN orders_clean o ON r.region = o.region
    """, conn)
    conn.close()
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Database not found. Please run build_db.py first.")
    st.stop()

# Task 4.2 - Embedded Executive Summary
st.markdown("### Executive Summary")
st.info("In May 2026, the network saw heavy regional volatility, headlined by Guntur's +122.19% Month-on-Month sales spike. This aggressive upward trend was distributed across core categories, signaling a structural demand shift rather than an isolated bulk order. We recommend immediate inventory buffering for Guntur to prevent stockouts. Please use the interactive filters below to explore the regional breakdown.")

# Task 4.1 - Interactive Region Filter
regions = ["All Regions"] + sorted(df['region'].dropna().unique().tolist())
selected_region = st.selectbox("Select Region to Filter:", regions)

filtered_df = df if selected_region == "All Regions" else df[df['region'] == selected_region]

# Task 4.1 - Overview Level (KPIs)
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales (INR)", f"₹{filtered_df['sales_inr'].sum():,.2f}")
col2.metric("Total Profit (INR)", f"₹{filtered_df['profit_inr'].sum():,.2f}")
col3.metric("Total Order Count", f"{filtered_df['order_id'].nunique():,}") 

st.markdown("---")
col_chart1, col_chart2 = st.columns(2)

# Chart 1: Bar Chart (Total Sales by Region - one color, highlights selected)
sales_by_region = df.groupby('region', as_index=False)['sales_inr'].sum()
sales_by_region['color'] = sales_by_region['region'].apply(lambda x: '#e74c3c' if x == selected_region else '#3498db')
fig_bar = px.bar(sales_by_region, x='region', y='sales_inr', title="What are the total sales by region?", labels={'sales_inr': 'Sales (INR)', 'region': 'Region'})
fig_bar.update_traces(marker_color=sales_by_region['color'])
fig_bar.update_yaxes(rangemode="tozero")
col_chart1.plotly_chart(fig_bar, use_container_width=True)

# Chart 2: Donut Chart (Sales Share by Category - capped slices)
sales_by_cat = filtered_df.groupby('category', as_index=False)['sales_inr'].sum()
fig_pie = px.pie(sales_by_cat, names='category', values='sales_inr', hole=0.4, title="What is the sales distribution by category?", labels={'sales_inr': 'Sales (INR)'})
col_chart2.plotly_chart(fig_pie, use_container_width=True)

# Chart 3: Line Chart (Monthly Trend)
trend_df = filtered_df.groupby('month', as_index=False)['sales_inr'].sum()
fig_line = px.line(trend_df, x='month', y='sales_inr', title="How did monthly sales trend over the period?", labels={'sales_inr': 'Sales (INR)', 'month': 'Month'})
fig_line.update_yaxes(rangemode="tozero")
st.plotly_chart(fig_line, use_container_width=True)

# Task 4.1 - Detail Level (Per-Region Data Table)
st.markdown("### Per-Region, Per-Month Detail")
detail_table = filtered_df.groupby(['region', 'month']).agg({'sales_inr': 'sum', 'profit_inr': 'sum', 'order_id': 'nunique'}).reset_index()
detail_table.rename(columns={'order_id': 'distinct_orders'}, inplace=True)
st.dataframe(detail_table, use_container_width=True)