import unittest
from datetime import datetime, timedelta
from analysis import *

class TestPopulateStockData(unittest.TestCase):

    def setUp(self):
        """
        Set up the test by fetching EPS data and initializing the necessary variables.
        """
        self.ticker = "AAPL"
        self.start_date = "1996-01-01"
        self.eps_data = get_quarterly_eps(self.ticker)
        self.stock_data = populate_stock_data(self.ticker, self.start_date)

    def test_data_population(self):
        """
        Test that populate_stock_data correctly applies the most recent EPS value up to each date.
        """
        all_dates = sorted(self.stock_data[self.ticker].keys())
        for date in all_dates:
            current_date = datetime.strptime(date, "%Y-%m-%d")

            # Get the most recent EPS value as of the current_date - 1 day
            most_recent_eps = None
            for eps_date, eps_value in self.eps_data[self.ticker]:
                eps_date_parsed = datetime.strptime(eps_date, "%Y-%m-%d")
                if eps_date_parsed <= current_date - timedelta(days=1):
                    most_recent_eps = eps_value
                else:
                    break

            # Assert that the EPS value in stock_data matches the most recent EPS value
            self.assertEqual(self.stock_data[self.ticker][date], most_recent_eps,
                             f"EPS mismatch on {date}: expected {most_recent_eps}, found {self.stock_data[self.ticker][date]}")

    def test_eps_update_on_quarter_date(self):
        """
        Test that EPS values update correctly on the date of a new quarterly EPS report.
        """
        for i in range(len(self.eps_data[self.ticker]) - 1):
            current_eps_date = datetime.strptime(self.eps_data[self.ticker][i][0], "%Y-%m-%d")
            next_eps_date = datetime.strptime(self.eps_data[self.ticker][i + 1][0], "%Y-%m-%d")
            current_eps_value = self.eps_data[self.ticker][i][1]

            # For all dates between current_eps_date + 1 and next_eps_date, EPS should be the current EPS value
            date = current_eps_date + timedelta(days=1)
            while date < next_eps_date:
                date_str = date.strftime("%Y-%m-%d")
                if date_str in self.stock_data[self.ticker]:  # Ensure the date is within the populated range
                    self.assertEqual(self.stock_data[self.ticker][date_str], current_eps_value,
                                     f"EPS mismatch on {date_str}: expected {current_eps_value}, found {self.stock_data[self.ticker][date_str]}")
                date += timedelta(days=1)

    def test_empty_eps_data(self):
        """
        Test that the function handles cases where no EPS data is available.
        """
        empty_ticker = "INVALID_TICKER"
        empty_stock_data = populate_stock_data(empty_ticker, self.start_date)
        self.assertEqual(empty_stock_data, {}, "Expected empty stock_data for invalid ticker")

if __name__ == "__main__":
    unittest.main()
