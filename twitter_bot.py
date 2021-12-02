#!/usr/bin/env python3
# coding: utf-8

__version__ = "0.1"

import argparse
import json
import locale
import logging
import random
import string
import sys
import time

import requests
import schedule
import tweepy
# Get & parse config
from dotenv import dotenv_values
from json_flatten import flatten

LOG_LEVEL = logging.DEBUG

config = dotenv_values(".env")
consumer_key = config.get("TW_CONSUMER_KEY", "Wrong key name for consumer key. ")
consumer_secret = config.get("TW_CONSUMER_SECRET", "Wrong key name for consumer secret.")
access_token = config.get("TW_ACCESS_TOKEN", "Wrong key name for access token.")
access_token_secret = config.get("TW_ACCESS_TOKEN_SECRET", "Wrong key name for acces token secret.")
tw_bearer_token = config.get("TW_BEARER_TOKEN", "Wrong key name for bearer token.")

S = 22  # number of characters in the string.

ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
print("The randomly generated string is : " + str(ran))  # print the random data


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


logger = _get_logger(name=__file__)


# Authenticate to Twitter
def authenticate_to_twitter(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api_authed = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api_authed.verify_credentials()
        logger.info("Authentication Successful")
    except:
        logger.debug("Authentication Error. Check credentials")
    return api_authed


api = authenticate_to_twitter(consumer_key, consumer_secret, access_token, access_token_secret)

tweet_map = {}


def get_btc_price_BITSO(currency_code):
    books = get_available_books_BITSO()
    book_key = f"btc_{currency_code}"
    reverse_book_key = f"{currency_code}_btc"
    print(book_key)
    if book_key not in books:
        logger.info(f"Book {book_key} is not available for querying. ")
    elif reverse_book_key in books:
        execute_btc_price_request(reverse_book_key)
    else:
        execute_btc_price_request(book_key)


def execute_btc_price_request(book_key):
    btc_price_api_url = f"https://api.bitso.com/v3/ticker/?book={book_key}"
    response = requests.get(btc_price_api_url)
    res_json = response.json()
    logger.debug(f"GOT RESPONSE FOR {book_key} REQUEST ::::::::: {json.dumps(res_json, indent=4, sort_keys=True)}")
    if res_json['success']:
        bid = res_json['payload']['bid']
        # Add result to future tweet storage
        tweet_map[book_key] = bid


def get_available_books_BITSO(started=True):
    available_books_url = "https://api.bitso.com/v3/available_books/"
    available_books_response = requests.get(available_books_url)
    available_books_json = available_books_response.json()
    unflat_json = available_books_json['payload']
    flat_json = flatten(unflat_json)
    filtered_dict = {k: v for (k, v) in flat_json.items() if 'book' in k}
    books = list(filtered_dict.values())

    if not started:
        logger.info(f"Bitso has {len(filtered_dict)} books available")
        logger.info(f"Available books: {books}")
    return books


def tweet():
    if tweet_map:
        key, val = tweet_map.popitem()
        twit_to_tweet = f" {str(ran)} Latest BTC price in ${key.upper}: ${val}"
        logger.info("GONNA TWEET:::::", twit_to_tweet)
        api.update_status(twit_to_tweet)
        time.sleep(22)


def main(**kwargs):
    logger = _get_logger(name=__file__)
    # start = time.time()
    started = False
    get_available_books_BITSO(started)
    started = True
    logger.info("Script execution STARTED")
    logger.info(f"Received currency codes: {kwargs['currency_codes']}")
    codes = kwargs['currency_codes']
    price_query_interval = kwargs['price_interval']
    tweet_query_interval = kwargs['tweet_interval']

    for c in codes:
        logger.info(f"Scheduling to query BTC price in ${c.upper()} ")
        schedule.every(price_query_interval).seconds.do(get_btc_price_BITSO, c)
        # schedule.every(tweet_query_interval).minutes.do(tweet)

    while True:
        try:
            schedule.run_pending()

        except tweepy.TweepyException as e:
            logger.debug(e)
            raise e


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Input currency codes to init bot:",
        epilog=f"Example: --currency_codes ars usd mxn ",
    )
    parser.add_argument(
        "--currency_codes",
        help='The currency code(s) for BTC valuation ',
        nargs="+",
        required=True,
    )
    parser.add_argument(
        "--price_interval",
        help='The interval (seconds) for the price query. Default = 10 ',
        nargs="+",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--tweet_interval",
        help='The interval (minutes) for tweeting. Default = 1 ',
        type=int,
        default=1,
    )

    args = parser.parse_args()
    for arg in vars(args):
        print(arg, "=", getattr(args, arg))
    count = 1

    for f in args.currency_codes:
        count = count + 1
    return vars(args)

if __name__ == "__main__":
    sys.exit(main(**_parse_args()))
