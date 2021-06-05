import re
import sys
import numpy as np
import pandas as pd
import nltk
from nltk.probability import FreqDist
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, RegexpTokenizer
# nltk.download('vader_lexicon')
# nltk.download('stopwords')

class NLP_stat:

    @staticmethod
    def text_tonkenize(data):
        # make lower case
        data = data.apply(lambda txt: txt.lower() if type(txt)==str else txt)
        # stop words
        stop_words=stopwords.words('english')
        data = data.apply(lambda txt: ' '.join([word for word in txt.split() if word not in stop_words]))
        # word tokenize
        word_tokenizer = RegexpTokenizer('[a-zA-Z]+')
        data = data.apply(lambda txt: word_tokenizer.tokenize(txt))
        data = data.apply(lambda txt: ' '.join(txt))
        # Word Lemmatizer
        lemmatizer = WordNetLemmatizer()
        data = data.apply(lambda txt: lemmatizer.lemmatize(txt))  
        # join word in sentences
        data = data.apply(lambda txt: ' '.join(txt) if type(txt)==list else txt)
        # escape characters
        escape_chars = re.compile(r"[\t\n\r\f\v-]")
        data = data.apply(lambda txt: escape_chars.sub('', txt) if type(txt)==str else txt)
        # single characters
        single_chars = re.compile(r"(^\w{1})(?=\s)|(?<=\s)[\w]{1}(?=\s)")
        data = data.apply(lambda txt: single_chars.sub('', txt))
        return data

    @staticmethod
    def polarity_score(data):
        """
                Return a float for sentiment strength based on the input text.
                Positive values are positive valence, negative value are negative valence.

        ref:    https://www.nltk.org/api/nltk.sentiment.html
                https://www.nltk.org/howto/sentiment.html
        """
        def check_polarity(x):
            if type(x)!=np.nan and x > 0.05:
                return "positive"
            elif type(x)!=np.nan and x < -0.05:
                return "negative"
            elif type(x)!=np.nan and x >= -0.05 and x <= 0.05:
                return "neutral"
            else:
                return np.nan

        sid = SentimentIntensityAnalyzer()
        df_scores = pd.DataFrame()
        df_scores['text']       = data.values.tolist()
        df_scores['scores']     = df_scores['text'].apply(lambda x: sid.polarity_scores(x) if type(x)==str else x)
        df_scores['neg']   = df_scores['scores'].apply(lambda x: x['neg'] if type(x)==dict else x )
        df_scores['neu']    = df_scores['scores'].apply(lambda x: x['neu'] if type(x)==dict else x )
        df_scores['pos']   = df_scores['scores'].apply(lambda x: x['pos'] if type(x)==dict else x )
        df_scores['comp']   = df_scores['scores'].apply(lambda x: x['compound'] if type(x)==dict else x )
        df_scores['sent']  = df_scores['comp'].apply(lambda x: check_polarity(x))
        df_scores.drop(labels = ['scores'], axis=1, inplace=True)
        return df_scores

    @staticmethod
    def get_unique_words(data):
        unique_words = set()
        for idx, row in data.iteritems():
            if isinstance(row, str):
                for word in row.split():
                    unique_words.update([word])
        return list(unique_words)

    @staticmethod
    def WordsCount(data):
        return data.map(lambda words: len(words.split())).to_list()
    
    @staticmethod
    def get_word_list(data):
        words_list = list()
        for idx, row in data.iteritems():
            if isinstance(row, str):
                for word in row.split():
                    words_list.append(word)
        return words_list

    @staticmethod
    def freq_dist(data):
        freq_df = pd.DataFrame( FreqDist(data.split()).items(), columns=['word', 'frequency'] )
        return freq_df

    @staticmethod
    def get_freq_dist(data):
        data_text = None
        if type(data) == str:
            data_text = data.split()
        elif type(data) == list:
            data_text = data
        else:
            return None
        freq_df = pd.DataFrame(FreqDist(data_text).items(), columns=['word', 'frequency'] )
        return freq_df

