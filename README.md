## Stock Market Sentiment Analysis.

**Abstract**

The stock market is very dynamic and is considered to be one of the most sensitive field to rapid changes due to the underlying nature of the financial domain. There are various factors that influence stock sentiment, which include news (economic, political and industry related) and social media. These factors help influence stock sentiment as they impact stock market volatility and the overall trend.

The application addressed in this project analyze the impact of the sentiment on the stock market and it's able to forecast stock market movement direction not only using financial market data, but also combining them with and extensive dataset that combines social media and news articles.

#### Objective

- Identification of trends in the stock prices of a company by performing sentiment analysis.

- find out which news source is the most impactful on predicting the stock price.

- Build a classification model capable of predicting the stock price for the upcoming 30 minutes.

  

##### Data Collection

The dataset is entirely scraped from different financial sources using different APIs and concerns the news related to the stock Apple from 01/01/2019 to 04/30/2021.

The API's used are the following:

- NEWSAPI              https://newsapi.org/
- FINNHUB API       https://finnhub.io/
- STOCK NEWS API https://stocknewsapi.com/

<img src="https://raw.githubusercontent.com/akladyous/stock-market-sentiment-analysis/main/img/top10_news_source.png?raw=True" alt="img" style="zoom:67%;" />

#### Features Engineering

Since we are dealing with unlabeled datasets, we applied VADER pre-trained model to classify the scraped articles and extract new features needed for our model.



![img](https://raw.githubusercontent.com/akladyous/stock-market-sentiment-analysis/main/img/sentiment_distribution.png?raw=True)



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

#### Exploratory Data Analysis



![img](https://raw.githubusercontent.com/akladyous/stock-market-sentiment-analysis/main/img/news_sources_vs_sentiment.png?raw=True)



<br clear="left"/>

![img](https://raw.githubusercontent.com/akladyous/stock-market-sentiment-analysis/main/img/word_freq_distribution.png?raw=True)

<br clear="left"/>

<img src="https://raw.githubusercontent.com/akladyous/stock-market-sentiment-analysis/main/img/word_cloud.png?raw=True" style="zoom:50%;" />

<br clear="left"/>

#### Models

- TfidfVectorizer
- GloVe 

#### Interpretation

![img](https://raw.githubusercontent.com/akladyous/stock-market-sentiment-analysis/main/img/roc.jpg?raw=True)

<br clear="left"/>

The method we used in our project to do sentiement analysis and price forcasting includes 2 major modeling approaches:

- Sentiment Analysis Prediction
  - The two major methods we used to do sentiment analysis includes Recurrent Neural Network (RNN) model constructed with Embedding layer and LSTM bidirectional layer which we intialized with the embedding matrix learned from Gensim Word2Vec pretrained Model.
- Stock Market Price Prediction
  - The second model is focused on statistical approach using SARIMAX model for a short-term time series forecasting and predicting the stock market trend.

#### Conclusion

- Since the our dataset is completely scrapped from various financial news sources, we end up with an unbalanced dataset where the postive classe represent 85% of our data, however our model did pretty well with 92.8% of Accuracy as well as and "ROC" 89% for both "True Positive Rate" & "False Positive Rate".
- Similarly the second dataset we used on predicting the time series and stock market price are not stionary and rappresent an exponential trend,  however SARIMAX model are able to predict the future values of the stock price for the upcomming 6 period (30 minutes).

#### Future Work

- Improve web scraping technique using different API
- Use SQL database to improve our model performance.
- Create a real-time Dashboard for predicting market sentiment and price forecasting
