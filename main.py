import streamlit as st
import pandas as pd
import numpy as np
from data_generator import generate_dummy_data
from financial_metrics import calculate_metrics
from visualizations import plot_line_chart, plot_heatmap, plot_histogram

# Set page config
st.set_page_config(page_title="Financial Performance Dashboard", layout="wide")

# Title and description
st.title("Financial Performance and Risk Metrics Dashboard")
st.write("This dashboard displays key financial performance and risk metrics using dummy time series data.")

# Initialize session state
if 'ticker' not in st.session_state:
    st.session_state.ticker = "AAPL"

# Sidebar for user input
st.sidebar.header("Settings")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-05-31"))

# Update ticker in session state when changed
new_ticker = st.sidebar.selectbox("Select Asset", ["AAPL", "GOOGL", "MSFT", "AMZN"], key="ticker_select")
if new_ticker != st.session_state.ticker:
    st.session_state.ticker = new_ticker
    st.rerun()  # Updated from st.experimental_rerun()

# Generate dummy data
df = generate_dummy_data(st.session_state.ticker, start_date, end_date)

# Calculate metrics
metrics = calculate_metrics(df)

# Display metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("ROI", f"{metrics['roi']:.2f}%")
col2.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
col3.metric("Alpha", f"{metrics['alpha']:.2f}")
col4.metric("Beta", f"{metrics['beta']:.2f}")

col5, col6, col7 = st.columns(3)
col5.metric("Value at Risk (95%)", f"{metrics['var']:.2f}")
col6.metric("Standard Deviation", f"{metrics['std_dev']:.2f}")
col7.metric("Maximum Drawdown", f"{metrics['max_drawdown']:.2f}%")

# Visualizations
st.header("Price and Returns")
fig_line = plot_line_chart(df)
st.plotly_chart(fig_line, use_container_width=True)

col8, col9 = st.columns(2)

with col8:
    st.header("Correlation Heatmap")
    fig_heatmap = plot_heatmap(df)
    st.plotly_chart(fig_heatmap, use_container_width=True)

with col9:
    st.header("Returns Distribution")
    fig_hist = plot_histogram(df)
    st.plotly_chart(fig_hist, use_container_width=True)

# Add a note about the data
st.caption("Note: This dashboard uses dummy data generated for demonstration purposes.")
