# importing required packages
import tweepy
import pandas as pd
import stylecloud
from IPython.display import Image
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

json_data = [r._json for r in tweets]
# Normalizing the Data
df = pd.json_normalize(json_data)
# Removing duplicates from the tweets
df.drop_duplicates(subset='full_text',inplace=True)

# Creating the csv file of total tweets
df.to_csv("complete_info.csv",index=False)
df['full_text'].to_csv("tweet.csv",index=False)

# Declaring style cloud
stylecloud.gen_stylecloud(file_path='tweet.csv',
                          icon_name='fab fa-twitter',
                          palette='colorbrewer.qualitative.Paired_3',
                          background_color='white',
                          gradient='horizontal',
                          stopwords=True,
                          custom_stopwords=["RT","THE","IS","THIS","HTTPS","CO","i", "me", "my", "myself", "we", "our",
                                            "ours", "ourselves", "you", "you're", "you've", "you'll", "you'd", "your",
                                            "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
                                            "she's", "her", "hers", "herself", "it", "it's", "its", "itself", "they",
                                            "them", "their", "theirs", "themselves", "what", "which", "who", "whom",
                                            "this", "that", "that'll", "these", "those", "am", "is", "are", "was", "were",
                                            "be", "been", "being", "have", "has", "had", "having", "do", "does", "with",
                                            "about", "against", "between", "into", "through", "during", "before", "after",
                                            'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
                                            'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
                                            'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
                                            'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's',
                                            "t", "can", "will", "just", "don", "don't", "should", "should've", "now", "d", "ll",
                                            'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn',
                                            "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't",
                                            'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't",
                                            'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won',
                                            "won't",'wouldn', "wouldn't"])

# Displaying WordCloud
Image('stylecloud.png')
