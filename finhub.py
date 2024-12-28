import finnhub
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tqdm import tqdm
import yfinance as yf
import pandas as pd
import numpy as np
import time

from sp500_tickers import *

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
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += relativedelta(months=months)

    return dates

def get_splits(ticker, start_date, end_date):
    """
    Retrieve stock splits for a given stock and date range.

    Parameters:
        ticker (str): The stock ticker symbol.
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        DataFrame: A DataFrame containing the splits data indexed by date.
    """
    stock_data = yf.Ticker(ticker)
    splits = stock_data.splits
    splits = splits[(splits.index >= start_date) & (splits.index <= end_date)]
    return splits

def calculate_cumulative_relative_return(ticker, start_date, benchmark_ticker="SPY", years=1):
    """
    Calculate the cumulative return of a stock relative to a benchmark index over a period of time after a given start date,
    (accounting for stock splits?).

    Parameters:
        ticker (str): The stock ticker symbol.
        benchmark_ticker (str): The benchmark index ticker symbol.
        start_date (str): The start date in 'YYYY-MM-DD' format.
        years (int): Number of years after the start date to calculate cumulative relative return.

    Returns:
        float: The cumulative relative return over the specified period.
    """
    # Determine the end date based on the number of years
    start_date_obj = pd.to_datetime(start_date)
    end_date_obj = start_date_obj + pd.DateOffset(years=years)
    end_date = end_date_obj.strftime('%Y-%m-%d')

    # Download data from Yahoo Finance
    stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    benchmark_data = yf.download(benchmark_ticker, start=start_date, end=end_date, progress=False)

    # Ensure data is not empty
    if stock_data.empty or benchmark_data.empty:
        raise ValueError("No data found for the given ticker(s) and date range.")

    # Calculate cumulative returns
    stock_cumulative_return = (stock_data['Close'].iloc[-1].to_numpy()[0] / stock_data['Open'].iloc[0].to_numpy()[0]) - 1
    benchmark_cumulative_return = (benchmark_data['Close'].iloc[-1].to_numpy()[0] / benchmark_data['Open'].iloc[0].to_numpy()[0]) - 1

    # Calculate cumulative relative return
    cumulative_relative_return = stock_cumulative_return - benchmark_cumulative_return

    return cumulative_relative_return

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

def get_xy_data_for_tickers(ticker_data_dict, start_date='1993-01-29', end_date='2023-12-27'):
    x_data = []
    y_data = []
    quarter_dates_list = get_dates_list(start_date, end_date)
    for quarter_start_date in tqdm(quarter_dates_list):
        quarter_start_date = datetime.strptime(quarter_start_date, '%Y-%m-%d')
        for ticker in ticker_data_dict.keys():
            closest_date = None
            for date_str in ticker_data_dict[ticker].keys():
                date = datetime.strptime(date_str, '%Y-%m-%d')
                # Closest date on or before the start date:
                if date <= quarter_start_date:
                    if closest_date is None or date > closest_date:
                        closest_date = date
            if closest_date is not None:
                closest_date=closest_date.strftime('%Y-%m-%d')
            else:
                closest_date = None
            if closest_date:
                for retry_n in range(2):
                    x_data.append(list(ticker_data_dict[ticker][closest_date].values()))
                    try:
                        y_data.append(calculate_cumulative_relative_return(ticker, closest_date))
                    except ValueError:
                        print(f"No data available for {ticker} from yfinance, retry_n={retry_n}")
                        if(len(x_data)!=len(y_data)):
                            x_data.pop()
                            assert(len(x_data)==len(y_data))
            else:
                #print(f"No data available for {ticker} on or before {quarter_start_date}")
                continue
    assert(len(x_data) == len(y_data))
    return np.array(x_data), np.array(y_data)

all_tickers_data = get_all_tickers_data(sp500_list, feature_list)
x_data, y_data = get_xy_data_for_tickers(all_tickers_data)

#x_data=np.load("x_data.npy")
#y_data=np.load("y_data.npy")
np.save("x_data.npy", x_data)
np.save("y_data.npy", x_data)
print(x_data.shape)
print(y_data.shape)
