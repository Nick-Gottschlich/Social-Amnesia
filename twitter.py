import tweepy

# for dev purposes
from secrets import twitterConsumerKey, twitterConsumerSecret, twitterAccessToken, twitterAccessTokenSecret

# twitter state object
#  Handles configuration options set by the user
twitterState = {}

def setTwitterLogin(consumerKey, consumerSecret, accessToken, accessTokenSecret, loginConfirmText):
    # ============ REAL =============
    # auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    # auth.set_access_token(accessToken, accessTokenSecret)
    # ============= REAL ============

    # =========== DEV TESTING =============
    auth = tweepy.OAuthHandler(twitterConsumerKey, twitterConsumerSecret)
    auth.set_access_token(twitterAccessToken, twitterAccessTokenSecret)
    # ============== DEV TESTING ==============

    api = tweepy.API(auth)

    twitterUsername = api.me().screen_name

    loginConfirmText.set(f'Logged in to twitter as {twitterUsername}')

    # ========== this block gets all of the users tweets ============

    # userTweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    # newTweets = api.user_timeline(count=200)

    # save most recent tweets
    # userTweets.extend(newTweets)

    # save the id of the oldest tweet less one
    # oldest = userTweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    # while len(newTweets) > 0:
    #     print(f'getting tweets before ${oldest}')

    #     # all requests use the max_id param to prevent duplicates
    #     newTweets = api.user_timeline(count=200, max_id=oldest)

    #     # save most recent tweets
    #     userTweets.extend(newTweets)

    #     # update the id of the oldest tweet less one
    #     oldest = userTweets[-1].id - 1

    #     print(f'...${len(userTweets)} tweets downloaded so far')

    # for tweet in userTweets:
    #     print(tweet.text)

    # ========== this block gets all of the users tweets ============
