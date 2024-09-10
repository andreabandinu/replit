import numpy as np
import pandas as pd
from scipy.stats import norm
import yfinance as yf

def calculate_metrics(df, market_ticker='^GSPC'):
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
    
    # Alpha and Beta calculation using S&P 500 as market index
    try:
        # Fetch market data
        market_data = yf.download(market_ticker, start=df.index[0], end=df.index[-1])
        market_returns = market_data['Close'].pct_change().dropna()

        # Align dates
        aligned_returns = returns.align(market_returns, join='inner')
        stock_returns = aligned_returns[0]
        market_returns = aligned_returns[1]

        # Calculate excess returns
        risk_free_rate = 0.02 / 252  # Assuming 2% annual risk-free rate
        excess_returns = stock_returns - risk_free_rate
        market_excess_returns = market_returns - risk_free_rate

        # Calculate beta
        beta = excess_returns.cov(market_excess_returns) / market_excess_returns.var()

        # Calculate alpha
        alpha = (stock_returns.mean() - risk_free_rate) - (beta * (market_returns.mean() - risk_free_rate))

        # Annualize alpha
        alpha_annualized = alpha * 252

    except Exception as e:
        print(f"Error calculating Alpha and Beta: {e}")
        alpha_annualized = np.nan
        beta = np.nan
    
    # Monte Carlo VaR, ES, and CVaR
    mc_var, mc_es, mc_cvar = monte_carlo_risk_metrics(returns)
    
    return {
        'roi': roi,
        'sharpe_ratio': sharpe_ratio,
        'var': var,
        'std_dev': std_dev,
        'max_drawdown': max_drawdown,
        'alpha': alpha_annualized,
        'beta': beta,
        'mc_var': mc_var,
        'mc_es': mc_es,
        'mc_cvar': mc_cvar
    }

def monte_carlo_risk_metrics(returns, num_simulations=10000, confidence_level=0.95):
    """
    Perform Monte Carlo simulation to calculate Value at Risk (VaR), Expected Shortfall (ES),
    and Conditional Value at Risk (CVaR).
    Returns VaR, ES, and CVaR as percentages of the initial investment.
    """
    mean_return = returns.mean()
    std_dev = returns.std()
    
    # Generate random returns
    simulated_returns = np.random.normal(mean_return, std_dev, size=(len(returns), num_simulations))
    
    # Calculate cumulative returns
    cumulative_returns = np.cumprod(1 + simulated_returns, axis=0)
    
    # Calculate portfolio value at the end of the simulation period
    final_values = cumulative_returns[-1]
    
    # Sort the final values
    sorted_final_values = np.sort(final_values)
    
    # Calculate VaR
    var_index = int(num_simulations * (1 - confidence_level))
    var = (1 - sorted_final_values[var_index]) * 100  # Convert to percentage
    
    # Calculate ES
    es = (1 - np.mean(sorted_final_values[:var_index])) * 100  # Convert to percentage
    
    # Calculate CVaR (mean of returns below VaR)
    cvar = (1 - np.mean(sorted_final_values[:var_index])) * 100  # Convert to percentage
    
    return var, es, cvar
