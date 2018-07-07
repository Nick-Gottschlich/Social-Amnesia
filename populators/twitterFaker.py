# quick program to auto tweet and favorite as rapidly as possible to fill out a twitter acct

import tweepy
from datetime import datetime
from secrets import twitterConsumerKey, twitterConsumerSecret, twitterAccessToken, twitterAccessTokenSecret
import random


auth = tweepy.OAuthHandler(twitterConsumerKey, twitterConsumerSecret)
auth.set_access_token(twitterAccessToken, twitterAccessTokenSecret)

api = tweepy.API(auth, wait_on_rate_limit=True)

while(1):
    # top 10 twitter emojis (http://www.emojitracker.com/), used so much there will always be new tweets to favorite
    emoji = random.choice('😂❤️♻️😍♥️😭😊😒💕😘')
    print(emoji)
    testTweets = tweepy.Cursor(api.search, q=emoji).items(20)

    for tweet in testTweets:
        try:
            api.create_favorite(tweet.id)
            print("FAVORITING: ", tweet.text)
        except Exception as e:
            print(e)
        
    while(1):
        try:
            api.update_status(datetime.now())
            print('tweet tweet: ', datetime.now())
        except Exception as e:
            print(e)
            break
