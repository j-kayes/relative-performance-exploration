import finnhub
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tqdm import tqdm
import yfinance as yf
import pandas as pd
import numpy as np
import time
import logging

from sp500_tickers import *

def calculate_returns(tickers, spread=0.00, benchmark_ticker='SPY', start_date='2020-01-01', end_date='2021-01-01'):
    # Download data for the specified tickers and date range
    tickers.append("SPY")  # Add the benchmark ticker to the list
    data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')
    returns = {}
    for ticker in tickers:
        try:
            # Get the open price at the start date and close price at the end date
            open_price = data[ticker]['Open'].iloc[0] * (1 + spread)
            close_price = data[ticker]['Close'].iloc[-1] * (1 - spread)

            # Calculate the return
            if(ticker is not benchmark_ticker):
                returns[ticker] = (close_price / open_price) - 1
            else:
                benchmark_return = (close_price / open_price) - 1
        except IndexError:
            print(f"No data available for {ticker} in the specified date range.")
            returns[ticker] = None

    # Calculate the average return assuming equal share between all stocks/tickers
    valid_returns = [ret for ret in returns.values() if ret is not None]
    average_return = sum(valid_returns) / len(valid_returns) if valid_returns else None

    return benchmark_return, returns, average_return

def get_dates_list(start_date, end_date, months=3):
    """
    Generate a list of dates between `start_date` and `end_date` spaced by `n` months.

    Parameters:
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.
        months (int): Number of months to space between dates.

    Returns:
        list: A list of date strings in 'YYYY-MM-DD' format.
    """
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    dates = []
    current_date = start_date

    while current_date <= end_date:
        dates.append(current_date)
        current_date += relativedelta(months=months)

    return dates

def initialise_stock_dict(ticker_list, metrics_list, start_date='1993-03-01', end_date='2024-12-24'):
    date_dict = {}
    for ticker in tqdm(ticker_list):
        date_dict[ticker] = {}
        for metric in metrics_list:
            date_dict[ticker][metric] = {}
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            # Create a dictionary with each date as a key
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                if(date_str in date_str[ticker]):
                    date_dict[ticker][current_date.strftime('%Y-%m-%d')].append() 
                current_date += timedelta(days=1)

    return date_dict

def get_common_keys(data_dict):
    # Initialize the set with keys from the first date
    all_dates = list(data_dict.keys())
    common_keys = set(data_dict[all_dates[0]].keys())

    # Iterate through the remaining dates and perform intersection
    for date in all_dates[1:]:
        common_keys.intersection_update(data_dict[date].keys())
    return common_keys

# Setup client
finnhub_client = finnhub.Client(api_key="ctlfnq1r01qv7qq264lgctlfnq1r01qv7qq264m0")
feature_list = ['assetTurnoverTTM', 'bookValue', 'cashRatio', 'currentRatio',
       'ebitPerShare', 'eps', 'ev', 'fcfMargin', 'fcfPerShareTTM',
       'grossMargin', 'inventoryTurnoverTTM', 'longtermDebtTotalAsset',
       'longtermDebtTotalCapital', 'longtermDebtTotalEquity',
       'netDebtToTotalCapital', 'netDebtToTotalEquity', 'netMargin',
       'operatingMargin', 'payoutRatioTTM', 'pb', 'peTTM', 'pfcfTTM',
       'pretaxMargin', 'psTTM', 'quickRatio', 'receivablesTurnoverTTM',
       'roaTTM', 'roeTTM', 'roicTTM', 'rotcTTM', 'salesPerShare', 'sgaToSale',
       'totalDebtToEquity', 'totalDebtToTotalAsset', 'totalDebtToTotalCapital',
       'totalRatio', 'ptbv', 'tangibleBookValue']

def get_ticker_data(ticker, feature_list):
    quarterly_data_dict = {}
    time.sleep(1.0)
    finhub_dict = finnhub_client.company_basic_financials(ticker, 'all')
    if(len(finhub_dict['series'])==0):
        print("No data for {}".format(ticker))
        return None
    for metric in feature_list:
        if(metric in finhub_dict['series']['quarterly']):
            for entry in finhub_dict['series']['quarterly'][metric]:
                x_date = (datetime.strptime(entry['period'], "%Y-%m-%d").date() + timedelta(days=1)).strftime('%Y-%m-%d')
                if x_date not in quarterly_data_dict:
                    quarterly_data_dict[x_date] = {metric: entry['v']}
                else:
                    quarterly_data_dict[x_date][metric] = entry['v']

    for date in quarterly_data_dict.keys():
        for feature in feature_list:
            if feature not in quarterly_data_dict[date]:
                quarterly_data_dict[date][feature] = np.nan
        assert(len(quarterly_data_dict[date]) == len(feature_list))
    return quarterly_data_dict

def get_all_tickers_data(tickers, feature_list):
    all_tickers_data = {}
    for ticker in tqdm(tickers):
        all_tickers_data[ticker] = get_ticker_data(ticker, feature_list)
    return all_tickers_data

def check_yfinance_connection():
    try:
        response = requests.get("https://finance.yahoo.com", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def calculate_cumulative_relative_return(tickers, start_date, years, data, benchmark_ticker="SPY"):
    """
    Calculate the cumulative return of multiple stocks relative to a benchmark index over a period of time after a given start date.

    Parameters:
        tickers (list): List of stock ticker symbols.
        benchmark_ticker (str): The benchmark index ticker symbol.
        start_date (str): The start date in 'YYYY-MM-DD' format.
        years (int): Number of years after the start date to calculate cumulative relative return.
        data (DataFrame): Pre-downloaded data for the tickers and benchmark.

    Returns:
        dict: A dictionary with the cumulative relative return for each ticker.
    """
    end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=365 * years)).strftime('%Y-%m-%d')

    # Ensure data is not empty
    if data.empty:
        raise ValueError("No data found for the given ticker(s) and date range.")

    cumulative_relative_returns = {}
    for ticker in tickers:
        try:
            # Calculate cumulative returns
            stock_cumulative_return = (data[ticker]['Close'].iloc[-1] / data[ticker]['Open'].iloc[0]) - 1
            benchmark_cumulative_return = (data[benchmark_ticker]['Close'].iloc[-1] / data[benchmark_ticker]['Open'].iloc[0]) - 1

            # Calculate cumulative relative return
            cumulative_relative_return = stock_cumulative_return - benchmark_cumulative_return
            cumulative_relative_returns[ticker] = cumulative_relative_return
        except IndexError:
            print(f"No data available for {ticker} in the specified date range.")
            cumulative_relative_returns[ticker] = None

    return cumulative_relative_returns

def get_xy_data_for_tickers(ticker_data_dict, quarter_start_date='1993-03-01', end_date='2018-01-01', max_retries=1, retry_delay=1):
    x_data = []
    y_data = []
    dates_list = get_dates_list(quarter_start_date, end_date, months=3)
    tickers = list(ticker_data_dict.keys())
    benchmark_ticker = "SPY"

    for quarter_date in tqdm(dates_list):
        quarter_date_str = quarter_date.strftime('%Y-%m-%d')
        end_date_str = (quarter_date + timedelta(days=365)).strftime('%Y-%m-%d')

        for retry_n in range(max_retries):
            if check_yfinance_connection():
                try:
                    # Download data for all tickers at once
                    data = yf.download(tickers + [benchmark_ticker], start=quarter_date_str, end=end_date_str, group_by='ticker')
                    for ticker in tickers:
                        closest_date = None
                        for date_str in ticker_data_dict[ticker].keys():
                            date = datetime.strptime(date_str, '%Y-%m-%d')
                            # Closest date on or before the start date:
                            if date <= quarter_date:
                                if closest_date is None or date > closest_date:
                                    closest_date = date
                        if closest_date is not None:
                            closest_date_str = closest_date.strftime('%Y-%m-%d')
                            if closest_date_str in ticker_data_dict[ticker]:
                                x_data.append(list(ticker_data_dict[ticker][closest_date_str].values()))
                                cumulative_relative_returns = calculate_cumulative_relative_return([ticker], closest_date_str, 1, data, benchmark_ticker)
                                y_data.append(cumulative_relative_returns[ticker])
                    break  # Exit the retry loop if successful
                except ValueError:
                    print(f"No data available for tickers from yfinance, retry_n={retry_n}")
                    if len(x_data) != len(y_data):
                        x_data.pop()
                        assert len(x_data) == len(y_data)
                    if retry_n < max_retries - 1:
                        print(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                    else:
                        print(f"Failed to get data for tickers after {max_retries} retries.")
            else:
                print("No connection to yfinance. Waiting for connection to be restored...")
                time.sleep(retry_delay)

    assert len(x_data) == len(y_data)
    return np.array(x_data), np.array(y_data)

#logging.basicConfig(level=logging.DEBUG)
all_tickers_data = np.load("sp500.npy", allow_pickle=True).item() #get_all_tickers_data(sp500_list, feature_list)
np.save("sp500.npy", all_tickers_data, allow_pickle=True)
#x_data, y_data = get_xy_data_for_tickers(all_tickers_data)

x_data = np.load("x_data.npy")
y_data = np.load("y_data.npy")



print(x_data)
print(y_data)

#x_data = np.save("x_data.npy", x_data)
#y_data = np.save("y_data.npy", y_data)



#print(calculate_returns(["AAPL", "GOOG", "XOM"]))