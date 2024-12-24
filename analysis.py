import requests
import yfinance as yf

def get_quarterly_eps(api_key, ticker):
    """
    Fetch quarterly EPS data for a given stock ticker using Alpha Vantage API.

    Args:
        api_key (str): Your Alpha Vantage API key.
        ticker (str): The stock ticker symbol.

    Returns:
        dict: A dictionary with the ticker as the key and a list of tuples (date, EPS) as the value.
    """
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "EARNINGS",
        "symbol": ticker,
        "apikey": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        data = response.json()

        if "quarterlyEarnings" not in data:
            raise ValueError(f"Unexpected response format or missing data for ticker: {ticker}")

        quarterly_eps = [
            (entry["fiscalDateEnding"], float(entry["reportedEPS"]))
            for entry in data["quarterlyEarnings"]
            if entry["reportedEPS"] != "None"
        ]

        return {ticker: quarterly_eps}

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return {ticker: []}
    except ValueError as e:
        print(e)
        return {ticker: []}

def get_shares_outstanding(ticker, date):
    """
    Fetch the number of shares outstanding for a given stock ticker, filtering to find the closest date before or on the given date.

    Args:
        ticker (str): The stock ticker symbol.
        date (str): The target date (in 'YYYY-MM-DD' format).

    Returns:
        int or None: Shares outstanding closest to or before the given date.
    """
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="max")
        history.index = history.index.strftime('%Y-%m-%d')  # Format index as strings for comparison

        # Filter dates before or on the given date
        filtered_history = history[history.index <= date]

        if filtered_history.empty:
            print(f"No data available for {ticker} before or on {date}.")
            return None

        # Get the last available row before or on the given date
        closest_date = filtered_history.index[-1]
        shares_outstanding = stock.info.get("sharesOutstanding", None)

        if shares_outstanding is None:
            print(f"Shares outstanding data not available for {ticker}.")

        return shares_outstanding

    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return None

# Example usage
api_key = "WRRLA8ME71KXWTBB"
ticker = "AAPL"
#print(get_quarterly_eps(api_key, ticker))
print(get_shares_outstanding("AAPL", "2021-12-31"))
