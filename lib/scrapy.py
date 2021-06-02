from time import sleep
import sys
import requests
from bs4 import BeautifulSoup as BS
from numpy import nan
from selenium import webdriver

class Scrapy(object):
    @staticmethod
    def get_url(url, params={}, verify=True, timeout=15, handle_exceptions=False):
        #https://www.whatismybrowser.com/detect/what-is-my-user-agent
        session = requests.session()
        session.stream = True
        session.cookies.clear()
        result = None
        headers= {
                'User-Agent' : 'Mozilla/5.0',
                'Connection' : 'keep-alive',
                'Accept-Encoding': 'gzip, compress, deflate, br',
                'Cache-Control': 'no-cache',
                "Pragma": "no-cache"
                }
        session.headers = headers
        if not url.startswith(("http://", "https://")):
            return None

        try:
            result = session.get(url,
                                params=params,
                                verify=True,
                                timeout=timeout,
                                headers=headers,
                                allow_redirects=True)
        except Exception as error:
            if handle_exceptions:
                print('Error')
        else:
            session.close()
            return result
    @staticmethod
    def check_result(html_page):
        if isinstance(html_page, requests.Response):
            if html_page and html_page.status_code == 200:
                return True
            else:
                return False

    @staticmethod
    def url2text(html_page):
        articles = None
        # html_page = self.get_url(timeout=40)
        if Scrapy.check_result(html_page):
            p_tags = BS(html_page.content, 'html.parser').find_all('p')
            articles_tags = [x.text for x in p_tags]
            articles = (' '.join(articles_tags))
        else:
            missing_urls.append((idx, url))
            articles = nan
        return articles

    @staticmethod
    def scrap(url_list):
        articles = []
        missing_articles = []
        total_urls = len(url_list)
        for idx, url, in enumerate(url_list):
            sys.stdout.write(f"{idx+1}/{total_urls} {round(idx/total_urls*100)}% {url}\r")
            html_page = Scrapy.get_url(url, timeout=40)
            if Scrapy.check_result(html_page):
                p_tags = BS(html_page.content, 'html.parser').find_all('p')
                articles_tags = [x.text for x in p_tags]
                if len(articles_tags) >=1:
                    articles.append(' '.join(articles_tags))
                else:
                    articles.append(nan)
            else:
                missing_articles.append((idx, url))
                articles.append(nan)
            sys.stdout.flush()
            sleep(1)
        return articles, missing_articles

    @staticmethod
    def web_scrap(url_list):
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

# s=Scrapy()
# r = s.get_url('http://www.google.com', handle_exceptions=True)
# print(r)



# url="https://www.fool.com/investing/2020/05/05/apple-news-engagement-is-soaring-amidst-covid-19.aspx"
# urls=[
#     "https://www.cnbc.com/2020/05/04/apple-announces-new-13-inch-macbook-pro-with-magic-keyboard.html",
#     "https://www.fool.com/investing/2020/05/05/now-is-a-perfect-time-for-apple-to-buy-sonos.aspx",
#     "https://www.fool.com/investing/2020/05/05/has-apple-shot-itself-in-crucial-india-smartphone.aspx",
#     "https://www.fool.com/investing/2020/05/05/apple-news-engagement-is-soaring-amidst-covid-19.aspx"
#     ]
# s = Scrapy()
# # s1 = s.get_url(url)
# # print(s1.status_code)
# # s2 = s.url2text(s.get_url(url))
# ar = s.scrap(urls)
# print(print(len(ar)))
# print(ar[0])
