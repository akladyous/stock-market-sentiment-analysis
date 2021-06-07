import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as BS
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


def url2text(url_list):
    p_tag = []
    articles_tags = []
    articles_text = []
    
    for idx, url in enumerate(url_list):
        #https://www.whatismybrowser.com/detect/what-is-my-user-agent
        session = requests.session()
        user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        try:
            html_page = requests.get(url, headers=user_agent, verify=True, timeout=15)
            html_page.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print (url) # e.response.text
        session.close()
        if html_page.status_code == 200:
            p_tags = BS(html_page.content, 'html.parser').find_all('p')
            articles_tags = [x.text for x in p_tags]
            articles_text.append(' '.join(articles_tags))
        else:
            articles_text.append(np.nan)
    return articles_text

def polarity_score(pd_series):
    """
    ref:    https://www.nltk.org/api/nltk.sentiment.html
            https://www.nltk.org/howto/sentiment.html
    """
    sid = SentimentIntensityAnalyzer()
    df_scores = pd.DataFrame()
    df_scores['text']     = pd_series.apply(lambda row: tokenize.sent_tokenize(row) if row==str else row)
    df_scores['scores']   = df_scores.text.apply(lambda x: sid.polarity_scores(x) if type(x)==str else x)
    df_scores['negative'] = df_scores.scores.apply(lambda x: x['neg'] if type(x)==dict else x )
    df_scores['neutral']  = df_scores.scores.apply(lambda x: x['neu'] if type(x)==dict else x )
    df_scores['positive'] = df_scores.scores.apply(lambda x: x['pos'] if type(x)==dict else x )
    df_scores['compound'] = df_scores.scores.apply(lambda x: x['compound'] if type(x)==dict else x )
    df_scores['sentiment']= df_scores.compound.apply(lambda x: 'positive' if x>0 else 'negative')
    df_scores.drop(labels=['scores'], axis=1, inplace=True)
    
    return df_scores