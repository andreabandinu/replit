import yfinance as yf

def generate_stock_data(ticker, start_date, end_date):
    """
    Fetch real stock data using yfinance library.
    """
    df = yf.download(ticker, start=start_date, end=end_date)
    df['Returns'] = df['Close'].pct_change()
    return df

if __name__ == "__main__":
    # Example usage
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2023-06-30"
    stock_data = generate_stock_data(ticker, start_date, end_date)
    print(stock_data.head())