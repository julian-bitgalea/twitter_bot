#!/usr/bin/env python3
# coding: utf-8

__version__ = "0.1"

import argparse
import json
import random
import sys
import time

import requests
import schedule
import tweepy
# Get & parse config
from dotenv import dotenv_values

from array import array
import logging
import locale
import requests

import glob

LOG_LEVEL = logging.DEBUG

config = dotenv_values(".env")
consumer_key = config.get("TW_CONSUMER_KEY", "Wrong key name for consumer key. ")
consumer_secret = config.get("TW_CONSUMER_SECRET", "Wrong key name for consumer secret.")
access_token = config.get("TW_ACCESS_TOKEN", "Wrong key name for access token.")
access_token_secret = config.get("TW_ACCESS_TOKEN_SECRET", "Wrong key name for acces token secret.")
tw_bearer_token = config.get("TW_BEARER_TOKEN", "Wrong key name for bearer token.")

# util loggin function
def _get_logger(name=__name__, handler=logging.StreamHandler(sys.stdout)):
    logger = logging.getLogger(name)
    try:
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    except locale.Error as e:
        logger.debug("Ignoring error %s when setting locale", e)
    try:
        logger.setLevel(LOG_LEVEL)
    except NameError:
        logger.setLevel(logging.INFO)
    if not len(logger.handlers):
        handler = handler
        formater = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
        handler.setFormatter(formater)
        logger.addHandler(handler)
    return logger

# TODO Create TwitterClient class
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

# TODO figure out a way to dynamically generate this list
tweet_list = ['1', '11', '111', '1111', '11111', '111111111111111', '1111111111']

def get_btc_price(fiat_code):
    api_url = "https://api.bitso.com/v3/ticker/?book=btc_" + fiat_code
    response = requests.get(api_url)
    res_json = response.json()
    print(f"GOT RESPONSE FOR {fiat_code} ::::::::: {json.dumps(res_json, indent=4, sort_keys=True)}")

def tweet():
    print(tweet_list)
    tweet = random.choice(tweet_list)
    print("TWEETING:::::", tweet)
    tweet_list.remove(tweet)
    print(tweet_list)
    api.update_status(random.choice(tweet_list))


def main(**kwargs):
    logger = _get_logger(name=__file__)
    start = time.time()
    logger.info("Script execution STARTED")
    # schedule.every(5).seconds.do(tweet)
    print(kwargs['fiat_codes'])
    codes = kwargs['fiat_codes']

    for c in codes:
        print(c)
        print(f'scheduling {c} to be gotten')
        schedule.every(5).seconds.do(get_btc_price, c)

    while True:
        try:
            schedule.run_pending()

        except tweepy.TweepyException as e:
            raise e


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Input fiat currency codes to init bot:",
        epilog=f"Example: --fiat_codes ars usd mxn ",
    )
    parser.add_argument(
        "--fiat_codes",
        help='The fiat currency code(s) for BTC valuation ',
        nargs="+",
        required=True,
    )

    args = parser.parse_args()
    for arg in vars(args):
        print(arg, "=", getattr(args, arg))
    count = 1

    for f in args.fiat_codes:
        print(count, ":", f)
        count = count + 1
    return vars(args)


# if __name__ == "__main__":
#     main()

if __name__ == "__main__":
    sys.exit(main(**_parse_args()))
