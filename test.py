import yfinance as yf

def get_earliest_data_date(ticker):
    """
    Retrieve the earliest date for which open price data is available for a given ticker.

    Parameters:
        ticker (str): The stock ticker symbol.

    Returns:
        str: The earliest date with open price data in 'YYYY-MM-DD' format.
    """
    # Fetch data
    stock_data = yf.Ticker(ticker)
    history = stock_data.history(period="max")

    # Check if data is available
    if history.empty:
        raise ValueError(f"No data available for ticker {ticker}.")

    # Find the earliest date with open data
    earliest_date = history.index.min()
    return earliest_date.strftime('%Y-%m-%d')

# Example usage
benchmark_ticker = "SPY"
earliest_date = get_earliest_data_date(benchmark_ticker)
print(f"Earliest date with open data for {benchmark_ticker}: {earliest_date}")
