from time import sleep
import sys
import requests
from bs4 import BeautifulSoup as BS
from numpy import nan
from joblib import dump, load

class Scrapy(object):
    @staticmethod
    def get_url(url, params={}, verify=True, timeout=15, handle_exceptions=False):
        if not url.startswith(("http://", "https://")):
            return None
        url_redirect = None
        response = None
        #https://www.whatismybrowser.com/detect/what-is-my-user-agent
        
        url_redirect = Scrapy.check_redirect(url, params)
        
        if url_redirect :
            # check if response status code is ok:
            session = requests.session()
            # session.stream = True
            session.cookies.clear()
            headers= {
                    'User-Agent' : 'Mozilla/5.0',
                    'Connection' : 'keep-alive',
                    'Accept-Encoding': 'gzip, compress, deflate, br',
                    # 'Cache-Control': 'no-cache',
                    # "Pragma": "no-cache"
                    }
            session.headers = headers
            
            try:
                response = session.get(url_redirect,
                                    params=params,
                                    verify=True,
                                    timeout=timeout,
                                    headers=headers,
                                    allow_redirects=True)
            except Exception as error:
                session.close()
                if handle_exceptions:
                    print(response.raise_for_status())
            else:
                session.close()
                if Scrapy.check_html(response):
                    return response
                else:
                    session.close()
                    return None
        else:
            return response

    def check_redirect(url, params={}, handle_exceptions=False):
        """
        return real url path
        """
        response = None
        try:
            session = requests.session()
            headers= {
                    'User-Agent' : 'Mozilla/5.0',
                    'Connection' : 'keep-alive',
                    'Accept-Encoding': 'gzip, compress, deflate, br',
                    'Cache-Control': 'no-cache',
                    "Pragma": "no-cache"
                    }
            session.headers = headers
            session = requests.session()
            session.stream = True
            session.cookies.clear()
            response = session.get(url, params=params, verify=True, headers=headers, allow_redirects=True)
            session.close()
        except:
            if handle_exceptions:
                print(response.raise_for_status())
                return False
        else:
            if Scrapy.check_html(response):
                return response.url
            else:
                return False

    @staticmethod
    def check_html(html_page):
        if isinstance(html_page, requests.Response):
            if html_page and html_page.status_code == 200:
                return True
            else:
                return False

    @staticmethod
    def url2text(html_page):
        """
        Scrap articles from html page content
        """
        article = None
        if Scrapy.check_html(html_page):
            soup = BS(html_page.content, 'html.parser')
            p_tags = soup.find_all('p')
            article_tags = [x.text for x in p_tags]
            if len(article_tags) >=1:
                article = ' '.join(article_tags)
            else:
                article = None
        else:
            article = nan
        return article

    @staticmethod
    def scrap(url_list):
        if isinstance(url_list, list):
            articles = []
            missing_articles = []
            total_urls = len(url_list)
            content = None
            for idx, url, in enumerate(url_list):
                if not Scrapy.url_blacklist(url):
                    html_page = Scrapy.get_url(url, timeout=5)
                    if Scrapy.check_html(html_page):
                        sys.stdout.write(f"{idx+1}/{total_urls} {round(idx/total_urls*100)}% {html_page.url}\r")
                        content = Scrapy.url2text(html_page)
                        if content:
                            articles.append(content)
                        else:
                            articles.append(nan)
                            # missing_articles.append(url)
                    else:
                        # missing_articles.append(url)
                        articles.append(nan)
                    sys.stdout.flush()
                    sleep(1)
                else:
                    articles.append(nan)
                    # missing_articles.append(url)
        else:
            raise ValueError("input should be a list of url's")
        return articles #, missing_articles
    
    @staticmethod
    def url_blacklist(url):
        status = False
        blacklist = ['nasdaq', 'seekingalpha']
        for website in blacklist:
            if url.find(website) == -1:
                status = False
            else:
                status = True
        return status

    @staticmethod
    def web_scrap(url_list):
        """
        Scrap url's from given list of url's using "Selenium"
        """
        # "Accept-Language":"en-US,en;q=0.9"
        # "Accept-Encoding":"gzip, deflate, br"
        # "User-Agent":"Java-http-client/"
        from selenium import webdriver
        driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
        driver.implicitly_wait(10)
        article = None
        articles = []
        missing_articles = []
        total_urls = len(url_list)
        for idx, url, in enumerate(url_list):
            sys.stdout.write(f"{idx+1}/{total_urls} {round(idx/total_urls*100)}% {url}\r")

            driver.get(url)
            temp= []
            for _article in driver.find_element_by_xpath("/html/body").find_elements_by_css_selector("p"):
                temp.append(_article.text)
            articles.append(''.join(temp))
            sys.stdout.flush()
        driver.close()
        return articles

# from joblib import load
# import pandas as pd
# from scrapy import Scrapy

# scrap = Scrapy()
# finnhub_key=load('./finnhub/finnhub_key.pkl')
# df_news = pd.read_csv('./data/finnhub_news.csv')
# articles = scrap.scrap(df_news['url'].to_list()[3:])
