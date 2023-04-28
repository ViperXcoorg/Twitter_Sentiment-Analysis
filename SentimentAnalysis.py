# importing required packages
import tweepy
import re
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
import keys

# Passing Required keys and token
auth_handler = tweepy.OAuthHandler(consumer_key=keys.api_key,consumer_secret=keys.api_key_secret)
auth_handler.set_access_token(keys.access_token,keys.access_token_secret)

# Accessing Api
api = tweepy.API(auth_handler)

# initializing search term
search_term = 'amazon prime'
# initializing Number of tweets for Analysis
tweet_amount = 500

# call twitter Cursor to fetch tweets
tweets = tweepy.Cursor(api.search_tweets, q=search_term, lang='en',tweet_mode="extended").items(tweet_amount)


json_data = [tweet._json for tweet in tweets]
# Normalizing the json data
df = pd.json_normalize(json_data)
# Removing duplicates from the data
df.drop_duplicates(subset='full_text',inplace=True)

# Function for Cleaning the Data
def clean_tweet(tweet):
    return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|([RT])', ' ', str(tweet).lower()).split())

# Analyzing the tweets using tweepy module
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Analyzing the polarity from tweets
def analyze_polarity(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return analysis.sentiment.polarity
    elif analysis.sentiment.polarity == 0:
        return analysis.sentiment.polarity
    else:
        return analysis.sentiment.polarity

# Storing tweets and sentiment in columns
df['clean_tweet'] = df['full_text'].apply(lambda x : re.sub(r'\brt\b','',clean_tweet(x)))
df["Sentiment"] = df["full_text"].apply(lambda x : analyze_sentiment(x))
df["Polarity"] = df["full_text"].apply(lambda x : analyze_polarity(x))
#polarity = SentimentIntensityAnalyzer().polarity_scores(row)

# Converting the tweets into CSV file
df[['full_text','clean_tweet','Polarity','Sentiment']].to_csv("SM.csv",index=False)

# Printing Number of Positive, Negative and Neutral tweets
print("Total number of Tweets after removing duplicates are : {}".format(len(df["full_text"])))
print("Polarity of Tweets is: {}".format(df['Polarity'].sum()))
print("Total Positive Tweets are : {}".format(len(df[df["Sentiment"]=="Positive"])))
print("Total Negative Tweets are : {}".format(len(df[df["Sentiment"]=="Negative"])))
print("Total Neutral Tweets are : {}".format(len(df[df["Sentiment"]=="Neutral"])))

# Analysing tweets using pie chart
a=len(df[df["Sentiment"]=="Positive"])
b=len(df[df["Sentiment"]=="Negative"])
c=len(df[df["Sentiment"]=="Neutral"])
d=np.array([a,b,c])
explode = (0.1, 0.0, 0.1)
plt.pie(d,shadow=True,explode=explode,labels=["Positive","Negative","Neutral"],autopct='%1.2f%%')
plt.show()