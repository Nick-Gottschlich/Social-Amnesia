"""
Quick program to auto tweet and favorite as rapidly as possible to fill out a twitter acct
"""

import tweepy
from datetime import datetime

# TODO: Use `os.env`?
from secrets import twitterConsumerKey, twitterConsumerSecret, twitterAccessToken, twitterAccessTokenSecret
import random


auth = tweepy.OAuthHandler(twitterConsumerKey, twitterConsumerSecret)
auth.set_access_token(twitterAccessToken, twitterAccessTokenSecret)
api = tweepy.API(auth, wait_on_rate_limit=True)

    emoji = random.choice('😂❤️♻️😍♥️😭😊😒💕😘')
    print(emoji)
    testTweets = tweepy.Cursor(api.search, q=emoji).items(20)

    for tweet in testTweets:
        try:
            api.create_favorite(tweet.id)
            print("FAVORITING: ", tweet.text)
        except Exception as e:
            print(e)

    while True:
        try:
            api.update_status(datetime.now())
            print('tweet tweet: ', datetime.now())
        except Exception as e:
            print(e)
            break
