from datetime_util import DateTime_Validator
# from newsapi import NewsApiClient
from scrapy import Scrapy
import requests
import json

class News_api(DateTime_Validator):
    def __init__(self, token, start_date, end_date):
        super().__init__(start_date, end_date)
        self._token = token
        self.start_date = start_date
        self.end_date = end_date
        self._categories_list = None

    def get_source_list(self, category=None, language=None, country=None):
        """
        This endpoint returns the subset of news publishers that top headlines (/v2/top-headlines) are available from
        category    Find sources that display news of this category. Possible options: 
                    business - entertainment - general - health - science - sports - technology. Default: all categories.
        language    Possible options: (ar de en es fr he it nl no pt ru se ud zh) Default: all languages
        country     Default: all countries.
        """
        self._category = category
        self._language = language
        self._country = country
        news_api_inist = NewsApiClient(api_key=self._token)
        if category is not None:
            self._language = None 
        self._categories_list = news_api_inist.get_sources(self._category, self._language, self._country)
        
        #[source['id'] for source in self._categories_list['sources']]
        return self._categories_list.get('sources')

    def get_headlines(self, symbols, category):
        self._headlines_list = {k:[] for k in symbols}

        news_api_inist = NewsApiClient(api_key=self._token)
        for symbol in symbols:
            top_headlines = news_api_inist.get_top_headlines(q=symbol,category=category,language='en')
            self._headlines_list[symbol].append((top_headlines))
            return self._headlines_list

    def get_news(self, symbols, sources=None):
        self._symbols = symbols
        self._sources = sources
        self._news_list = [] # {k:[] for k in symbols}

        #news_api_inist = NewsApiClient(api_key=self._token)

        self._et_url = "https://newsapi.org/v2/everything?"
        self._et_params  = {'q': self._symbols,
                            'apiKey': self._token,
                            'from': self.start_date,
                            'to': self.end_date,
                            'sortBy': 'publishedAt',
                            'language': 'en',
                            'page': 1}
        if self._sources != None:
            for source in self._sources:
                self._et_params['source'] = source
                html_page = Scrapy.get_url(self._et_url, self._et_params)
                all_articles =  News_api._check_articles(html_page)
                if all_articles:
                    for article in all_articles.get('articles'):
                        if article and len(article) > 0:
                            self._news_list.append(article)
                else:
                    self._news_list = False
        else:
            html_page = Scrapy.get_url(self._et_url, self._et_params)
            all_articles = News_api._check_articles(html_page)
            if all_articles:
                self._news_list = all_articles
            else:
                self._news_list = False

        return self._news_list
    
    @staticmethod
    def _check_articles(html_page):
        if Scrapy.check_html(html_page):
            all_articles = json.loads(html_page.text)
            if isinstance(all_articles, dict):
                if  (
                    (all_articles.get('status', False) == 'ok')
                    and
                    (all_articles.get('totalResults', False) > 0)
                    ):
                    return all_articles['articles']
                else:
                    return False
        else:
            return False
