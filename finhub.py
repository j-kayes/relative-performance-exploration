import finnhub
from datetime import datetime, timedelta
from tqdm import tqdm

# todo: currenty takes too long:
def initialise_stock_dict(ticker_list, metrics_list, start_date='1989-09-29', end_date='2024-12-24'):
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
                date_dict[ticker][metric][current_date.strftime('%Y-%m-%d')] = None  # You can change the value as needed
                current_date += timedelta(days=1)

    return date_dict

# Setup client
finnhub_client = finnhub.Client(api_key="ctlfnq1r01qv7qq264lgctlfnq1r01qv7qq264m0")

aapl_quarterly_data_dict = {}
aapl_finhub_dict = finnhub_client.company_basic_financials('AAPL', 'all')

for metric in aapl_finhub_dict['series']['quarterly']:
    entries = []
    for entry in aapl_finhub_dict['series']['quarterly'][metric]:
        entries.append((entry['period'], entry['v']))
    aapl_quarterly_data_dict[metric] = entries

    print(aapl_quarterly_data_dict.keys())

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
