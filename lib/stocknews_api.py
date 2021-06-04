import pickle
import requests
import json
import sys
from datetime import datetime
from sys import stdout
from time import sleep
from datetime_util import DateTime_Validator
from scrapy import Scrapy

class StockNewsAPI(DateTime_Validator):
    def __init__(self, token, start_date, end_date):
        super().__init__(start_date, end_date)
        self.token = token
        self.start_date_us_fmt = self.convert_2_us_fmt(start_date)
        self.end_date_us_fmt = self.convert_2_us_fmt(end_date)

    def get_news(self, tickers, **kwargs):
        self._symbols = tickers
        self._news = []
        self.date_range = self.get_date_range(step=4, date_format="US")
        self._date_list_ = []
        self._params = {"tickers": tickers,
                "type": "article",
                "token": self.token,
                "fallback": "true",
                "country": "USA",
                "items": 50,
                "sortby": "rank"
                # "date": None,
                # "page": 1,
                # "industry":"Exchange+Traded",
                #"exchange": "NASDAQ"
                }
        self._params.update(kwargs)

        for idx in range(len(self.date_range)-1):
            self._date_list_.append(f"{self.date_range[idx].replace('-','')}-{self.date_range[idx+1].replace('-','')}")

        for idx, time_span in enumerate(self._date_list_):
            
            self._params['date'] = time_span
            url = "https://stocknewsapi.com/api/v1?"
            html_page = Scrapy.get_url(url, self._params)
            all_articles = json.loads(html_page.text)
            if ('data' in all_articles) and (len(all_articles['data']) !=0):
                for article in all_articles['data']:
                    self._news.append(article)
            # sys.stdout.write(f"\r[ {round((idx+1)/len(self._date_list_)*100)}% ] {html_page.url}")
            # sys.stdout.flush()
            sleep(.1)
        return self._news        
