import pandas as pd
import numpy as np
import yfinance as yf

def generate_dummy_data(ticker, start_date, end_date):
    """
    Generate dummy financial data that mimics real stock data.
    """
    # Use yfinance to get real data structure
    real_data = yf.download(ticker, start=start_date, end=end_date)
    
    # Generate dummy price data
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    np.random.seed(42)  # for reproducibility
    prices = np.random.randint(100, 200, size=len(dates)) + np.cumsum(np.random.randn(len(dates))) * 2
    
    # Create a DataFrame with dummy data
    df = pd.DataFrame({
        'Open': prices,
        'High': prices * (1 + abs(np.random.randn(len(dates)) * 0.02)),
        'Low': prices * (1 - abs(np.random.randn(len(dates)) * 0.02)),
        'Close': prices * (1 + np.random.randn(len(dates)) * 0.01),
        'Volume': np.random.randint(1000000, 10000000, size=len(dates))
    }, index=dates)
    
    # Calculate daily returns
    df['Returns'] = df['Close'].pct_change()
    
    return df

if __name__ == "__main__":
    # Example usage
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2023-06-30"
    dummy_data = generate_dummy_data(ticker, start_date, end_date)
    print(dummy_data.head())