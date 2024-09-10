import numpy as np
import pandas as pd
from scipy.optimize import minimize

def portfolio_return(weights, returns):
    return np.sum(returns.mean() * weights) * 252

def portfolio_volatility(weights, returns):
    return np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))

def sharpe_ratio(weights, returns, risk_free_rate=0.02):
    return (portfolio_return(weights, returns) - risk_free_rate) / portfolio_volatility(weights, returns)

def negative_sharpe_ratio(weights, returns, risk_free_rate=0.02):
    return -sharpe_ratio(weights, returns, risk_free_rate)

def optimize_portfolio(returns, risk_free_rate=0.02):
    num_assets = returns.shape[1]
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    initial_weights = np.array([1/num_assets] * num_assets)
    
    optimized = minimize(negative_sharpe_ratio, initial_weights, args=(returns, risk_free_rate),
                         method='SLSQP', bounds=bounds, constraints=constraints)
    
    return optimized.x

def get_optimal_portfolio(df):
    returns = df['Returns'].dropna()
    optimal_weights = optimize_portfolio(returns.to_frame())
    
    optimal_return = portfolio_return(optimal_weights, returns.to_frame())
    optimal_volatility = portfolio_volatility(optimal_weights, returns.to_frame())
    optimal_sharpe = sharpe_ratio(optimal_weights, returns.to_frame())
    
    return {
        'weights': optimal_weights,
        'return': optimal_return,
        'volatility': optimal_volatility,
        'sharpe_ratio': optimal_sharpe
    }
