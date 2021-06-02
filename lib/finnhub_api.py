from datetime import datetime, date
import os
from decouple import config
import requests
import json
from datetime_util import DateTime_Validator, datetime2timestamp
from scrapy import Scrapy

class FinnHub_init(DateTime_Validator):
    def __init__(self, token, start_date, end_date):
        super().__init__(start_date, end_date)
        self.token = token
        self.start_date = start_date
        self.end_date = end_date

        self._max_api_calls = 60                                            # maximum number of api call on free account.
        self._time_sleep = 60                                               # num. of second between each api call.
        self._nb_request = 0                                                # num. of requests alread done
        self._check_token(token)
        self._token = token                                                 # api token
        self._news_db_name = 'finnhub_financial_news'                       # news dataset file name
        self._hist_db_name = 'finnhyb_financial_hist'                       # news dataset file name
    
    @property
    def get_token(self):
        return self._token
    @get_token.setter
    def set_token(self, token):
        self._token = token
    @classmethod
    def _check_token(cls, token):
        if not (isinstance(token, str)
                and
                (token.isalnum())
                and
                (len(token)==20)):
            raise Exception('Invalid API KEY.. pleae verify!')        
#---------------------------------------------------------------------------------------------------------
class Finnhub(FinnHub_init):
    def __init__(self, token, start_date, end_date, symbol):
        super().__init__(token, start_date, end_date)
        self.symbol = symbol
        self.news_list = []

    def company_news(self):
        self._cn_url = 'https://finnhub.io/api/v1/company-news?'
        self._cn_params  = {'symbol': self.symbol,'token':self._token, 'from':self.start_date, 'to':self.end_date}
        html_page = Scrapy.get_url(self._cn_url, self._cn_params)

        if Scrapy.check_result(html_page):
            all_articles = json.loads(html_page.text)
            if len(all_articles) > 0:
                self.news_list = all_articles
            else:
                self.news_list = False
        return self.news_list

    def major_press_releases(self): # premium
        self._mpr_url = 'https://finnhub.io/api/v1/press-releases?'
        self._mpr_params  = {'symbol': self.symbol,'token':self._token, 'from':self.start_date, 'to':self.end_date}
        with requests.session() as mpr_session:
            self._mpr_html = requests.get(self._mpr_url, params=self._mpr_params, timeout=15)
            mpr_session.close()
        self._mpr_news = json.loads(self._mpr_html.text)
        return self._mpr_news        

    def company_profile(self):
        """ return dictionary with company profile """
        self._base_url = "https://finnhub.io/api/v1/stock/profile2?"
        self._params  = {'symbol': self.symbol, 'token': self._token}
        with requests.session() as req_sess:
            html_page = requests.get(self._base_url, params=self._params)
            req_sess.close()
        self._company_profile = json.loads(html_page.text)
        return self._company_profile
    
    def stock_candles(self, timeframe):
        """
        get candlestick data (OHLCV) from stocks.

        timeframe:  Supported resolution includes 1, 5, 15, 30, 60, D, W, M.
                    Some timeframes might not be available depending on the exchange.
        """
        stock_url = ('https://finnhub.io/api/v1/stock/candle?')
        params =    {'symbol': self.symbol,
                    'resolution': timeframe,
                    'from': datetime2timestamp(self.start_date), 
                    'to': datetime2timestamp(self.end_date),        
                    'token': self._token
                    }
        session = requests.session()
        stock_hist = requests.get(stock_url, params=params, timeout=25)
        session.close()
        return stock_hist.json()

# from joblib import load
# import pandas as pd
# key = load('./finnhub/finnhub_key.pkl', 'rb')
# apple = Finnhub(key, "2021-05-28", "2021-05-29", "AAPL")
# apple_news = apple.company_news()
# print(len(apple_news))
# print(pd.DataFrame(apple_news))
