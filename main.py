import streamlit as st
import pandas as pd
import numpy as np
from data_generator import generate_stock_data
from financial_metrics import calculate_metrics
from visualizations import plot_line_chart, plot_heatmap, plot_histogram
from portfolio_optimization import get_optimal_portfolio

# Set page config
st.set_page_config(page_title="Financial Performance Dashboard", layout="wide")

# Title and description
st.title("Financial Performance and Risk Metrics Dashboard")
st.write("This dashboard displays key financial performance and risk metrics using real stock data.")

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
    st.rerun()

# Generate real stock data
df = generate_stock_data(st.session_state.ticker, start_date, end_date)

# Calculate metrics
metrics = calculate_metrics(df)

# Display metrics
st.header("Performance Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("ROI", f"{metrics['roi']:.2f}%")
col2.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
col3.metric("Alpha", f"{metrics['alpha']:.4f}")
col4.metric("Beta", f"{metrics['beta']:.2f}")

st.header("Risk Metrics")
col5, col6, col7 = st.columns(3)
col5.metric("Historical VaR (95%)", f"{metrics['var']:.2f}%")
col6.metric("Standard Deviation", f"{metrics['std_dev']:.2f}")
col7.metric("Maximum Drawdown", f"{metrics['max_drawdown']:.2f}%")

st.header("Advanced Risk Metrics (Monte Carlo)")
col8, col9, col10 = st.columns(3)
col8.metric("Monte Carlo VaR (95%)", f"{metrics['mc_var']:.2f}%")
col9.metric("Monte Carlo Expected Shortfall", f"{metrics['mc_es']:.2f}%")
col10.metric("Conditional Value at Risk (CVaR)", f"{metrics['mc_cvar']:.2f}%")

# Portfolio Optimization
st.header("Portfolio Optimization")
optimal_portfolio = get_optimal_portfolio(df)

col11, col12, col13 = st.columns(3)
col11.metric("Optimal Portfolio Return", f"{optimal_portfolio['return']:.2f}%")
col12.metric("Optimal Portfolio Volatility", f"{optimal_portfolio['volatility']:.2f}%")
col13.metric("Optimal Portfolio Sharpe Ratio", f"{optimal_portfolio['sharpe_ratio']:.2f}")

st.write("Optimal Portfolio Weights:")
st.write(pd.Series(optimal_portfolio['weights'], index=[st.session_state.ticker], name="Weight"))

# Visualizations
st.header("Price and Returns")
fig_line = plot_line_chart(df)
st.plotly_chart(fig_line, use_container_width=True)

col14, col15 = st.columns(2)

with col14:
    st.header("Correlation Heatmap")
    fig_heatmap = plot_heatmap(df)
    st.plotly_chart(fig_heatmap, use_container_width=True)

with col15:
    st.header("Returns Distribution")
    fig_hist = plot_histogram(df)
    st.plotly_chart(fig_hist, use_container_width=True)

# Add a note about the data and advanced risk models
st.caption("Note: This dashboard uses real stock data fetched using the yfinance library. The Monte Carlo simulation for VaR, Expected Shortfall, and Conditional Value at Risk (CVaR) provides a robust estimation of potential losses under various market scenarios. The portfolio optimization feature demonstrates the optimal portfolio allocation based on the efficient frontier approach.")
