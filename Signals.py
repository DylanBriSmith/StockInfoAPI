import json
import pandas as pd
import matplotlib.pyplot as pyplot
from datetime import datetime

pyplot.style.use('seaborn')
import yfinance as yf
import requests
#below is the YahooFinance api connection
#use your given api key for functioning
url = "https://yfapi.net/v6/finance/quote"
querystring = {"symbols": ""}
headers = {
    'x-api-key': "18z3t0FpI33wWFrNEmb2x2rjFmJIUf9a3MlFQlqL"
}


# response = requests.request("GET", url, headers=headers, params=querystring)


class Signals:
    """Wellcome!  This is my first API attempt.  Im not sure this is really an API.  Use it for whatever you'd like!  
        This was originally created so I could write my dads trading strategy into somewhat of a bot for him.  I ended up getting quite far and had my drive wiped by my stupid actions. 
        So I came back with this, a fraction of what once was but something to put on Github I suppose.

        I have no idea what the difference between ''' and the other(i cannot write it or i get errors everywhere)
    Returns:
        Black Magic: <-
    """
    '''
    :param ticker: Any Ticker you would like
    :param interval: 1m, 5m, 15m, 1d 1wk, 1mo
    :param range: 1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, 10y, ytd, max
    '''
    def __init__(self, ticker, interval, range):
        """

        Args:
            ticker (String): Any Ticker you would like
            interval (String): 1m, 5m, 15m, 1d 1wk, 1mo
            range (String): 1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, 10y, ytd, max
        """
        '''
        :param ticker: Any Ticker you would like
        :param interval: 1m, 5m, 15m, 1d 1wk, 1mo
        :param range: 1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, 10y, ytd, max
        '''
        self.ticker = ticker
        self.found_ticker = yf.Ticker(ticker)
        self.closing_prices_list = []
        self.opening_prices_list = []
        self.interval = interval
        self.range = range

    def all_data(self):
        '''
        :return: a dict of all data from yfinance of your ticker
        '''
        print(self.foundticker.info)

    def market_cap(self):
        '''
        :return: The marketcap of the ticker.  from yfinance
        '''
        print('$' + str(self.foundticker.info['marketCap']))

    def yahoo_finance_all(self):
        '''

        :return: a dict of all the data from a response call from the yahoo finance api
        '''
        querystring = {"symbols": self.ticker}
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)

    def closes(self):
        '''
        :return: a Pandas Series of all the closing prices of the ticker in the specified range given at instance
        '''
        ticker = self.ticker.upper()
        querystring = {"symbols": self.ticker,
                       "interval": f"{self.interval}",
                       "range": f"{self.range}"
                       }
        url = f"https://yfapi.net/v8/finance/chart/{ticker}"
        response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.text)
        data = json.loads(response.text)
        # data is a dict
        # the below line is all trial and error to access the closing prices
        for value in data['chart']['result'][0]['indicators']['quote'][0]['close']:
            self.closing_prices_list.append(value)
        return self.closing_prices_list

    def opens(self):
        '''

        :return: a Pandas Series of all the opening prices of the ticker in the specified range given at instance
        '''
        ticker = self.ticker.upper()
        querystring = {"symbols": self.ticker,
                       "interval": f"{self.interval}",
                       "range": f"{self.range}"
                       }
        url = f"https://yfapi.net/v8/finance/chart/{ticker}"
        response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.text)
        data = json.loads(response.text)
        # data is a dict
        # the below line is all trial and error to access the closing prices
        for value in data['chart']['result'][0]['indicators']['quote'][0]['open']:
            self.opening_prices_list.append(value)
        return self.opening_prices_list

    def moving_average(self, type, period):
        '''

        :param type: "close", "open"
        :param period: period is the value of days, for example
           1 is a 1 day moving average(or whatever interval you chose)
        :return: A pandas Series of a rolling mean applied to the price list of your choice
        '''
        if type == "open":
            output = pd.Series(data = self.opens(), dtype=float).rolling(period).mean()

        elif type == "close":
            output = pd.Series(data=self.closes(), dtype=float).rolling(period).mean()
        return output


test = Signals("msft", "1d", "3mo")
watcha = test.moving_average("close", 5)
print(watcha.to_list())