"""
Quick program to auto tweet and favorite as rapidly as possible to fill out a twitter acct
"""

import tweepy
from datetime import datetime

# TODO: Use `os.env`?
from secrets import twitterConsumerKey, twitterConsumerSecret, twitterAccessToken, twitterAccessTokenSecret

auth = tweepy.OAuthHandler(twitterConsumerKey, twitterConsumerSecret)
auth.set_access_token(twitterAccessToken, twitterAccessTokenSecret)
api = tweepy.API(auth)

while True:
    # this emoji is used so much there will always be new tweets to favorite
    testTweets = tweepy.Cursor(api.search, q='😂').items(10)

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
