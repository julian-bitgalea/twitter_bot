import requests
import tweepy
import schedule
from pprint import pprint 
import random
import json
import argparse

# Get & parse config
from dotenv import dotenv_values
config = dotenv_values(".env")
consumer_key = config.get("TW_CONSUMER_KEY", "Wrong key name for consumer key. ")
consumer_secret = config.get("TW_CONSUMER_SECRET", "Wrong key name for consumer secret.")
access_token = config.get("TW_ACCESS_TOKEN", "Wrong key name for access token.")
access_token_secret = config.get("TW_ACCESS_TOKEN_SECRET", "Wrong key name for acces token secret.")
tw_bearer_token = config.get("TW_BEARER_TOKEN", "Wrong key name for bearer token.")


# Authenticate to Twitter
def authenticate_to_twitter(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
        print("Authentication Successful")
    except:
        print("Authentication Error")
    return api

api = authenticate_to_twitter(consumer_key, consumer_secret, access_token, access_token_secret)


tweet_list = ['1','11', '111','1111','11111','111111111111111','1111111111']


def get_btc_price(fiat_code):
    api_url = "https://api.bitso.com/v3/ticker/?book=btc_" + fiat_code
    response = requests.get(api_url)
    res_json = response.json()
    print("GOT RESPONSE :::::::::")
    print(json.dumps(res_json, indent=4, sort_keys=True))


get_btc_price('ars')


def tweet():
    print(tweet_list)
    tweet = random.choice(tweet_list)
    print("TWEETING:::::", tweet)
    tweet_list.remove(tweet)
    print(tweet_list)
    api.update_status(random.choice(tweet_list))


def main():
    #schedule.every(5).seconds.do(tweet)
    schedule.every(5).seconds.do(get_btc_price('usd'))
    while True: 
        try:
            schedule.run_pending()

        except tweepy.TweepyException as e:
            raise e

if __name__ == "__main__":
    main()