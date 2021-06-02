import re
import sys
import numpy as np
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, RegexpTokenizer, WhitespaceTokenizer
# nltk.download('vader_lexicon')
# nltk.download('stopwords')

class NLP_stat:
    # def __init__(self, df_series):
    #     if not isinstance(df_series, pd.Series):
    #         raise TypeError ("Invalid data type: Pandas Series required")
    #     self._df_series = df_series

    @staticmethod
    def text_tonkenize(text_series):
        # make lower case
        text_series = text_series.apply(lambda txt: txt.lower() if type(txt)==str else txt)
        # stop words
        stop_words=stopwords.words('english')
        text_series = text_series.\
            apply(lambda txt: ' '.join([word for word in txt.split() if word not in stop_words]))
        # word tokenize
        word_tokenizer = RegexpTokenizer('[a-zA-Z]+')
        text_series = text_series.apply(lambda txt: word_tokenizer.tokenize(txt))
        text_series = text_series.apply(lambda txt: ' '.join(txt))
        # Word Lemmatizer
        lemmatizer = WordNetLemmatizer()
        text_series = text_series.apply(lambda txt: lemmatizer.lemmatize(txt))  
        # join word in sentences
        text_series = text_series.apply(lambda txt: ' '.join(txt) if type(txt)==list else txt)
        # escape characters
        escape_chars = re.compile(r"[\t\n\r\f\v-]")
        text_series = text_series.apply(lambda txt: escape_chars.sub('', txt) if type(txt)==str else txt)
        # single characters
        single_chars = re.compile(r"(^\w{1})(?=\s)|(?<=\s)[\w]{1}(?=\s)")
        text_series = text_series.apply(lambda txt: single_chars.sub('', txt))
        return text_series

    @staticmethod
    def polarity_score(text_series):
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
        df_scores['text']       = text_series.values.tolist()
        df_scores['scores']     = df_scores['text'].apply(lambda x: sid.polarity_scores(x) if type(x)==str else x)
        df_scores['neg']   = df_scores['scores'].apply(lambda x: x['neg'] if type(x)==dict else x )
        df_scores['neu']    = df_scores['scores'].apply(lambda x: x['neu'] if type(x)==dict else x )
        df_scores['pos']   = df_scores['scores'].apply(lambda x: x['pos'] if type(x)==dict else x )
        df_scores['compound']   = df_scores['scores'].apply(lambda x: x['compound'] if type(x)==dict else x )
        df_scores['sentiment']  = df_scores['compound'].apply(lambda x: check_polarity(x))
        df_scores.drop(labels = ['scores'], axis=1, inplace=True)
        return df_scores

    @property
    def get_unique_words(self):
        self._unique_words = set()
        for idx, row in self._df_series.iteritems():
            if isinstance(row, str):
                for word in row.split():
                    self._unique_words.update([word])
        return list(self._unique_words)

    @property
    def WordsCount(self):
        return self._df_series.map(lambda words: len(words.split())).to_list()
    
    @property
    def get_word_list(self):
        self._words_list = list()
        for idx, row in self._df_series.iteritems():
            if isinstance(row, str):
                for word in row.split():
                    self._words_list.append(word)
        return self._words_list

    @property
    def FrequencyDist(self):
        from collections import Counter
        self._words_list = self.get_word_list
        self._word_freq_dict = dict()
        self._word_freq_dict = Counter(self._words_list)
        return dict(sorted(self._word_freq_dict.items(), key=lambda v: v[1], reverse=True))

    @property
    def ProbFrequencyDist(self):
        self._probs = dict()
        self._word_freq_dict = dict()
        self._word_freq_dict = self.FrequencyDist
        for k in self._word_freq_dict.keys():
            self._probs[k] = self._word_freq_dict[k]/sum( self._word_freq_dict.values())
        return self._probs

    @staticmethod
    def Fine_Grained_selection(self, threshold):
        """ 
        return a list of words from the vocabulary of the text that are more than X (threshold) characters long.
        so that P(w) is true if and only if w is more than X (threshold) characters long

        {w | w ∈ V & P(w)}      the set of all w such that w is an element of V (the vocabulary) and w has property P"
        """
        self._threshold = threshold
        return [word for word in self.get_unique_words if len(word)>self._threshold]

    @property
    def Lexical_Diversity(self):
        self._lex_list = list()
        for idx, row in self._df_series.iteritems():
            if isinstance(row, str):
                try:
                    self._lex_list.append(np.round(len(row) / len(set(row)),2))
                except ZeroDivisionError:
                    self._lex_list.append(0)
        return self._lex_list