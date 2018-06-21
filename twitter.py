import tweepy

import arrow

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

    # initialize state
    twitterState['user'] = api
    twitterState['recentlyPostedCutoff'] = arrow.now().replace(hours=0)
    twitterState['maxFavorites'] = 0
    twitterState['maxRetweets'] = 0
    twitterState['testRun'] = 0


def setTwitterTimeToSave(hoursToSave, daysToSave, weeksToSave, yearsToSave, currentTimeToSave):
    totalHours = int(hoursToSave) + (int(daysToSave) * 24) + \
        (int(weeksToSave) * 168) + (int(yearsToSave) * 8736)

    twitterState['recentlyPostedCutoff'] = arrow.now().replace(
        hours=-totalHours)
    
    def setText(time, text):
        if (time == '0'):
            return ''
        else:
            return time + text
    
    hoursText = setText(hoursToSave, 'hours')
    daysText = setText(daysToSave, 'days')
    weeksText = setText(weeksToSave, 'weeks')
    yearsText = setText(yearsToSave, 'years')

    if (hoursToSave == '0' and daysToSave == '0' and weeksToSave == '0' and yearsToSave == '0'):
        currentTimeToSave.set(f'Currently set to save: [nothing]')
    else:
        currentTimeToSave.set(
            f'Currently set to save: [{yearsText} {weeksText} {daysText} {hoursText}] of items')

def setTwitterMaxFavorites(maxFavorites, currentMaxFavorites):
    if (maxFavorites == ''):
        maxFavorites = 0
    elif (maxFavorites == 'Unlimited'):
        twitterState['maxFavorites'] = 9999999999
    else:
        maxFavorites = int(maxFavorites)
        twitterState['maxFavorites'] = maxFavorites

    currentMaxFavorites.set(f'Currently set to: {str(maxFavorites)} Favorites')


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
