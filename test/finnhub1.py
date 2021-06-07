import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import json
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import os
from pathlib import Path
from decouple import config
import requests
from bs4 import BeautifulSoup as BS

class Finnhub(object):
    def __init__(self, token=None):
        self._max_api_calls = 60                                            # maximum number of api call on free account.
        self._time_sleep = 60                                               # num. of second between each api call.
        self._nb_request = 0                                                # num. of requests alread done
        self._check_token(token)
        self._token = token                                                 # api token
        self._news_db_name = 'finnhub_financial_news'                       # news dataset file name
        self._hist_db_name = 'finnhyb_financial_hist'                       # news dataset file name
        self._project_dir()

    @staticmethod
    def timestamp2datetime(value):
        """convert Epoch & Unix Timestamp  to datetime object"""
        return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
    @staticmethod
    def datetime2timestamp(value):
        """convert datetime object to Epoch & Unix TimeStamp"""
        return int(datetime.timestamp(datetime.fromisoformat(value)))
    
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
            
    @classmethod
    def _project_dir(cls):
        _directory_name = 'finnhub'
        _dir_path = os.getcwd() + '/public/p5/' + _directory_name + '/'
        if not os.path.exists(_directory_name):
            os.makedirs(_directory_name)
    
    def company_profile(self, symbol):
        """ return dictionary with company profile """
        self._base_url = "https://finnhub.io/api/v1/stock/profile2?"
        self._params  = {'symbol': symbol,'token':self._token}
        with requests.session() as req_sess:
            html_page = requests.get(self._base_url, params=self._params)
            req_sess.close()
        self._company_profile = json.loads(html_page.text)
        return self._company_profile
#---------------------------------------------------------------------------------------------------------
class Finnhub_news(Finnhub):
    def __init__(self, start_date, end_date, symbol, token):
        super().__init__(token)
        self.symbol = symbol                                                # stock symbol
        self.start_date = start_date
        self.end_date = end_date
        self._validate_date(start_date, end_date)
        self._start_date = datetime.strptime(start_date, "%Y-%m-%d")   # convert string date to datetime object
        self._end_date = datetime.strptime(end_date, "%Y-%m-%d")       # convert string date to datetime object
        self._delta_date = abs((self._end_date - self._start_date).days)    # calulate diff. between 2 dates    
        self._check_delta_dates()
    
    @staticmethod
    def _validate_date(*args):
        for arg in args:
            try:
                datetime.strptime(arg, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    def _check_delta_dates(self):
        if self._start_date > self._end_date:
            raise Exception("Start_Date is older than End_Date")
        if (self._start_date <= (datetime.now() - relativedelta(years=1))) :
            raise Exception("Start_Date shouldn't be older than 1 year")

    def get_news(self):
        self._base_url = 'https://finnhub.io/api/v1/company-news?'
        self._params  = {'symbol': self.symbol,'token':self._token, 'from':self.start_date, 'to':self.end_date}
        with requests.session() as req_sess:
            html_page = requests.get(self._base_url, params=self._params, timeout=15)
            req_sess.close()
        self._news = json.loads(html_page.text)
        return self._news

