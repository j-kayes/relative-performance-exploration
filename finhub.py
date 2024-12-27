import finnhub
from datetime import datetime, timedelta
from tqdm import tqdm
import yfinance as yf
import pandas as pd
import numpy as np

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

def calculate_cumulative_relative_return(ticker, benchmark_ticker, start_date, years=1):
    """
    Calculate the cumulative return of a stock relative to a benchmark index over a period of time after a given start date,
    accounting for stock splits.

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
    print(benchmark_data)
    print(stock_data)

    # Ensure data is not empty
    if stock_data.empty or benchmark_data.empty:
        raise ValueError("No data found for the given ticker(s) and date range.")

    # Calculate cumulative returns
    print(stock_data['Close'].iloc[-1].to_numpy()[0])
    print(stock_data['Open'].iloc[0].to_numpy()[0])
    print(benchmark_data['Close'].iloc[-1].to_numpy()[0])
    print(benchmark_data['Open'].iloc[0].to_numpy()[0])
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

def get_ticker_x_values(ticker_list, metrics_list, start_date='1993-03-01', end_date='2024-12-24'):
    ticker_date_x_dict = {}
    for ticker in tqdm(ticker_list):
        ticker_date_x_dict[ticker] = {}
        for metric in metrics_list:
            ticker_date_x_dict[ticker][metric] = {}
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            # Create a dictionary with each date as a key
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                if(date_str in date_str[ticker]):
                    ticker_date_x_dict[ticker][current_date.strftime('%Y-%m-%d')].append() 
                current_date += timedelta(days=1)

    return date_dict


# Setup client
finnhub_client = finnhub.Client(api_key="ctlfnq1r01qv7qq264lgctlfnq1r01qv7qq264m0")




''''
in_all = {}
aapl_quarterly_data_dict = {}
aapl_finhub_dict = finnhub_client.company_basic_financials('AAPL', 'all')
for metric in aapl_finhub_dict['series']['quarterly']:
    entries = []
    for entry in aapl_finhub_dict['series']['quarterly'][metric]:
        x_date = (datetime.strptime(entry['period'], "%Y-%m-%d").date() + timedelta(days=1)).strftime('%Y-%m-%d')
        if(x_date not in aapl_quarterly_data_dict):
            aapl_quarterly_data_dict[x_date] = {metric: entry['v']}
        else:
            aapl_quarterly_data_dict[x_date][metric] = entry['v']

test_df = pd.DataFrame()
test_dict = {}
for date in aapl_quarterly_data_dict.keys():
    for metric in aapl_quarterly_data_dict[date].keys():
        if(metric not in test_dict):
            test_df[metric] = aapl_quarterly_data_dict[date][metric]
        else:
            test_df[metric].add(aapl_quarterly_data_dict[date][metric], axis='rows')
        
test_df.to_excel('test.xlsx')
print(aapl_qutest_dfarterly_data_dict)
''''''

print(calculate_cumulative_relative_return('AAPL', 'SPY', '1995-01-01', years=1))

sp500_tickers = [
    'MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AMD', 'AES', 'AFL', 'AGIL',
    'APD', 'AIRB', 'AKAM', 'ALB', 'ARE', 'ALXN', 'AMAT', 'APTV', 'ADM', 'ANSS',
    'ANTM', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME',
    'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD',
    'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL',
    'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET',
    'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN',
    'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP',
    'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN',
    'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON',
    'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH',
    'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC',
    'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR',
    'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA',
    'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI',
    'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME',
    'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD',
    'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL',
    'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET',
    'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN',
    'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP',
    'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN',
    'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON',
    'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH',
    'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC',
    'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR',
    'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA',
    'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI',
    'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME',
    'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD',
    'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL',
    'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET',
    'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN',
    'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP',
    'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN',
    'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON',
    'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH',
    'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC',
    'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR',
    'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANET', 'AON', 'APA',
    'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI',
    'ANET', 'AON', 'APA', 'AAPL', 'AMZN', 'AMCR', 'AMD', 'AMP', 'ABC', 'AME',
    'AMGN'
    ]
'''