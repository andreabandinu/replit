import numpy as np
import pandas as pd

def calculate_metrics(df):
    """
    Calculate various financial performance and risk metrics.
    """
    returns = df['Returns'].dropna()
    
    # Performance metrics
    roi = (df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100
    sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std()
    
    # Risk metrics
    var = np.percentile(returns, 5)
    std_dev = returns.std()
    
    # Maximum Drawdown
    cum_returns = (1 + returns).cumprod()
    running_max = cum_returns.cummax()
    drawdown = (cum_returns - running_max) / running_max
    max_drawdown = drawdown.min() * 100
    
    # Alpha and Beta (assuming risk-free rate of 2% and market returns of 8%)
    risk_free_rate = 0.02 / 252  # daily
    market_returns = 0.08 / 252  # daily
    excess_returns = returns - risk_free_rate
    market_excess_returns = market_returns - risk_free_rate
    
    # Calculate beta using covariance and variance
    beta = excess_returns.cov(pd.Series([market_excess_returns] * len(excess_returns))) / np.var([market_excess_returns] * len(excess_returns))
    alpha = returns.mean() - (risk_free_rate + beta * market_excess_returns)
    
    return {
        'roi': roi,
        'sharpe_ratio': sharpe_ratio,
        'var': var,
        'std_dev': std_dev,
        'max_drawdown': max_drawdown,
        'alpha': alpha * 252,  # annualized
        'beta': beta
    }
