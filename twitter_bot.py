import requests


#Get & parse config
from dotenv import dotenv_values
config = dotenv_values(".env") 

consumer_key = config.get("TW_CONSUMER_KEY", "Wrong key name")
consumer_secret = config.get("TW_CONSUMER_SECRET", "Wrong key name")
access_token = config.get("TW_ACCESS_TOKEN", "Wrong key name")
access_token_secret = config.get("TW_ACCESS_TOKEN_SECRET", "Wrong key name")
tw_bearer_token = config.get("TW_BEARER_TOKEN", "Wrong key name")

print(consumer_key, consumer_secret, access_token, access_token_secret)

import tweepy

client = tweepy.Client(bearer_token=tw_bearer_token)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication Successful")
except:
    print("Authentication Error")

api = tweepy.API(auth)

public_tweets = api.home_timeline()

for tweet in public_tweets:
    print(tweet.text)


