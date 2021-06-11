## Twitter Sentiment Analysis.

**Abstract**

The stock market is very dynamic and is considered to be one of the most sensitive field to rapid changes due to the underlying nature of the financial domain. There are various factors that influence stock sentiment, which include news (economic, political and industry related) and social media. These factors help influence stock sentiment as they impact stock market volatility and the overall trend.

The application addressed in this project analyze the impact of sentiment on the stock market. and able to forecasts stock market movement direction not only using financial market data, but also combining them with and extensive dataset that combines social media and news articles.

##### Data Collection

The dataset is entirly scraped from diffrent financial sources using the following API:

1. NEWSAPI              https://newsapi.org/
2. FINNHUB API       https://finnhub.io/
3. STOCK NEWS API https://stocknewsapi.com/

##### Metrics

- Accuracy
- ROC

##### Liberary

- Requests
- Selenium
- BeautifulSoup
- Json
- DateTime
- JobLib
- SYS
- DateTime
- Time
- OS
- Requests
- RE
- Itertools
- Langdetect
- NLTK
- Gensim
- Numpy
- Pandas
- Seaborn
- Matplotlib
- Ploty
- Wordcloud
- Tensorflow
- Keras
- Scikit-learn
- Statsmodels

#### Models

- TfidfVectorizer
- GloVe 

#### Interpretation

<img align="right" width="400" height="400" hspace="0" vspace="0" src="https://raw.githubusercontent.com/akladyous/stock-market-sentiment-analysis/main/img/roc.jpg"><img align="left" width="400" height="400" hspace="0" vspace="20" src="https://raw.githubusercontent.com/akladyous/stock-market-sentiment-analysis/main/img/cm.png">







The method we used in our project to do sentiement analysis and price forcasting includes 2 magior modeling approaches:

- Sentiment Analysis Prediction
  - the two major methods we used to do sentiment analysis includes Recurrent Neural Network (RNN) model constructed with Embedding layer and LSTM bidirectional layer where we intialized with the embedding matrix learned from Gensim Word2Vec pretrained Model.
- Stock Market Price Prediction
  - the second model is focused on statistical approach using SARIMAX model for a short-term time series forecasting and predicting the stock market trend.

#### Conclusion

- Since the our dataset is completely scrapped from various financial news sources, we end up with an unbalanced dataset where the postive classe represent 85%  of our data, however our the model did pretty good with 92.8% of Accuracy as well as and "ROC" 89% for both "True Positive Rate" & "False Positive Rate".
- similarly the second dataset we used on predicting the time series and stock market price are not stionary and rappresent an exponential trend,  however SARIMAX model are able to predict the future values of the stock price for the upcomming 6 period (30 minutes).

#### Future Work

- Improve web scraping technique using different API
- Use SQL database to improve our model performance.
- Create a real-time Dashboard for predicting market sentiment and price forecasting
