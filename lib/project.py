import pandas as pd
import numpy as np
from joblib import load, dump
from datetime_util import timestamp2datetime
from stocknews_api import StockNewsAPI
from finnhub_api import Finnhub
from news_api import News_api
from scrapy import Scrapy
from nlp import NLP_stat
# from model import Model

class Project(object):
    def __new__(cls, *args, **kwargs):
        __instance = super(Project, cls).__new__(cls)
        __apis = frozenset(['newsapi', 'finnhub', 'stocknews'])
        if kwargs:
            if (
                sorted(__apis) == sorted([__k.lower() for __k in kwargs.keys()])
                and
                all([type(__v)==bool for __v in kwargs.values()])
                ):
                return __instance
            else:
                raise Exception("Invalid module names!")
        else:
            return __instance

    def __init__(self, start_date, end_date, symbol, auto_run=False, **kwargs):
        self.start_date = start_date
        self.end_date = end_date
        self.symbol = symbol
        self._auto_tun = auto_run
        self._newsapi = True
        self._finnhub = True
        self._stocknews = True
        if kwargs:
            for k,v in kwargs.items():
                setattr(self, ('_'+k), v)
        self._token = {}
        self._newsapi_news = []
        self._newsapi_df = pd.DataFrame()
        self._finnhub_news = []
        self._finnhub_df = pd.DataFrame()
        self._stocknews_news = []
        self._stocknews_df = pd.DataFrame()
        self._news_df = pd.DataFrame()
        self._score_df = pd.DataFrame()
        self._df = pd.DataFrame()
        self._articles = None
        self._file_name = './data/news_df.csv'
        self._accuracy = None
        self._y_predicted = None
        self._pred_df= None

    def run(self):
        if self._auto_tun:
            self.data_collection()
            self.cleaning_data()
            self.scrap_url()
            self.preprocessing()
            # self.modeling()
            return self._df


    def data_collection(self):
        self._token["newsapi_key"] = load("./newsapi/newsapi_key1.pkl")
        self._token["finnhub_key"] = load('./finnhub/finnhub_key.pkl')
        self._token["stocknews_key"] = load("./stocknewsapi/stocknewsapi_key.pkl")

        # collecting data using newsapi API
        if self._newsapi :
            sources = ['abc-news', 'business-insider', 'financial-post', 'google-news', 'reuters',
                        'nbc-news', 'techcrunch', 'wired', 'the-wall-street-journal']
            newsapi_inst = News_api(self._token["newsapi_key"], self.start_date, self.end_date)
            self._newsapi_news = newsapi_inst.get_news([self.symbol], sources=None)
        # collecting data using finnhub API
        if self._finnhub:
            finnhub_inst = Finnhub(self._token["finnhub_key"], self.start_date, self.end_date, self.symbol)
            self._finnhub_news = finnhub_inst.company_news()
        # collecting data using stocknews API
        if self._stocknews:
            stocknews_inst = StockNewsAPI(self._token["stocknews_key"], self.start_date, self.end_date)
            self._stocknews_news = stocknews_inst.get_news(self.symbol, items=50, pages=1)
        if not self._auto_tun:
            return self._newsapi_news, self._finnhub_news, self._stocknews_news

    def cleaning_data(self):
        # news_api news
        if self._newsapi :
            self._newsapi_df = pd.DataFrame(self._newsapi_news)
            self._newsapi_df.dropna(inplace=True)
            cols_to_drop = ['author', 'title', 'description', 'urlToImage', 'urlToImage','content']
            self._newsapi_df.drop(labels=cols_to_drop, axis=1, inplace=True)
            self._newsapi_df.rename(columns={"publishedAt":"date"}, inplace=True)
            self._newsapi_df['date'] = pd.to_datetime(self._newsapi_df['date'], infer_datetime_format=True)
            self._newsapi_df['source'] = self._newsapi_df['source']\
            .apply(lambda s: s['name'] if s['name']!=None else s['id'] if s['id']!=None else s)
        if self._finnhub:
            # finnhub_api news
            self._finnhub_df = pd.DataFrame(self._finnhub_news)
            self._finnhub_df.dropna(inplace=True)
            cols_to_drop = ['category', 'headline', 'id', 'image', 'related', 'summary']
            self._finnhub_df.drop(labels=cols_to_drop, axis=1, inplace=True)
            self._finnhub_df.rename(columns={'datetime':'date'}, inplace=True)
            self._finnhub_df['date'] = self._finnhub_df['date'].map(lambda x: timestamp2datetime(x))
            self._finnhub_df['date'] = pd.to_datetime(self._finnhub_df['date'], format='%Y-%m-%d %H:%M:%S')

        if self._stocknews:
            # stocknewsapi news
            self._stocknews_df = pd.DataFrame(self._stocknews_news)
            cols_to_drop = self._stocknews_df.columns.difference(['news_url', 'source_name','date'])
            self._stocknews_df.drop(cols_to_drop, axis=1, inplace=True)
            self._stocknews_df.columns=['url', 'source', 'date']
            self._stocknews_df['date'] = self._stocknews_df['date'].str.replace("\s-[0-9]{4}$", '', regex=True)
            self._stocknews_df['date'] = pd.to_datetime(self._stocknews_df['date'], format="%a, %d %b %Y %H:%M:%S")

        self._news_df = pd.concat([self._newsapi_df, self._finnhub_df, self._stocknews_df],
                                axis=0, ignore_index=True, sort=True)
        if not self._auto_tun:
            return self._news_df

    def scrap_url(self):
        self._articles = Scrapy.scrap(self._news_df['url'].to_list())
        self._news_df['articles'] = self._articles
        if not self._auto_tun:
            return self._news_df

    def preprocessing(self):
        self._news_df.dropna(inplace=True)
        self._news_df.drop(self._news_df.loc[(self._news_df['articles'].isna())].index, inplace=True)
        self._news_df['articles'] = NLP_stat.text_tonkenize(self._news_df['articles'])
        self._score_df = NLP_stat.polarity_score(self._news_df['articles'])
        self._df = pd.concat([self._news_df.reset_index(drop=True), self._score_df.reset_index(drop=True)],
                            axis=1, ignore_index=False, sort=False)
        self._df.drop(labels=['articles','neg','neu', 'pos', 'comp'], axis=1, inplace=True)
        self._df.rename(columns={'text':'articles'}, inplace=True)
        if not self._auto_tun:
            return self._df

