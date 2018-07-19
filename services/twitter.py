from datetime import datetime
from tkinter import messagebox

import arrow
import tweepy

# for dev purposes
# from secrets import twitterConsumerKey, twitterConsumerSecret, twitterAccessToken, twitterAccessTokenSecret

# twitter state object
# Handles configuration options set by the user
twitterState = {}


def setTwitterLogin(consumerKey, consumerSecret, accessToken, accessTokenSecret, loginConfirmText):
    # ============ REAL =============
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    # ============= REAL ============

    # =========== DEV TESTING =============
    # auth = tweepy.OAuthHandler(twitterConsumerKey, twitterConsumerSecret)
    # auth.set_access_token(twitterAccessToken, twitterAccessTokenSecret)
    # ============== DEV TESTING ==============

    api = tweepy.API(auth)

    twitterUsername = api.me().screen_name

    loginConfirmText.set(f'Logged in to twitter as {twitterUsername}')

    # initialize state
    twitterState['api'] = api
    twitterState['timeToSave'] = arrow.utcnow().replace(hours=0)
    twitterState['maxFavorites'] = 0
    twitterState['maxRetweets'] = 0
    twitterState['testRun'] = 0


def setTwitterTimeToSave(hoursToSave, daysToSave, weeksToSave, yearsToSave, currentTimeToSave):
    totalHours = int(hoursToSave) + (int(daysToSave) * 24) + \
                 (int(weeksToSave) * 168) + (int(yearsToSave) * 8736)

    twitterState['timeToSave'] = arrow.now().replace(
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


def setTwitterMaxRetweets(maxRetweets, currentMaxRetweets):
    if (maxRetweets == ''):
        maxRetweets = 0
    elif (maxRetweets == 'Unlimited'):
        twitterState['maxRetweets'] = 9999999999
    else:
        maxRetweets = int(maxRetweets)
        twitterState['maxRetweets'] = maxRetweets

    currentMaxRetweets.set(f'Currently set to: {str(maxRetweets)} Retweets')


def deleteTwitterTweets(root, currentlyDeletingText, deletionProgressBar, numDeletedItemsText):
    userTweets = []

    # make initial request for most recent tweets 
    #  (200 is the maximum allowed count)
    newTweets = twitterState['api'].user_timeline(count=200)

    # save most recent tweets
    userTweets.extend(newTweets)

    # save the id of the oldest tweet less one
    oldest = userTweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(newTweets) > 0:
        # all requests use the max_id param to prevent duplicates
        newTweets = twitterState['api'].user_timeline(count=200, max_id=oldest)

        # save most recent tweets
        userTweets.extend(newTweets)

        # update the id of the oldest tweet less one
        oldest = userTweets[-1].id - 1

    totalTweets = len(userTweets)

    numDeletedItemsText.set(f'0/{str(totalTweets)} items processed so far')

    count = 1
    for tweet in userTweets:
        tweetSnippet = tweet.text[0:50]
        if len(tweet.text) > 50:
            tweetSnippet = tweetSnippet + '...'
        for char in tweetSnippet:
            # tkinter can't handle certain unicode characters,
            #  so we strip them
            if (ord(char) > 65535):
                tweetSnippet = tweetSnippet.replace(char, '')

        timeCreated = arrow.Arrow.fromdatetime(tweet.created_at)

        if (timeCreated > twitterState['timeToSave']):
            currentlyDeletingText.set(f'Tweet: `{tweetSnippet}` is more recent than cutoff, skipping.')
        elif (tweet.favorite_count >= twitterState['maxFavorites']):
            currentlyDeletingText.set(
                f'Tweet: `{tweetSnippet}` has more favorites than max favorites, skipping.')
        elif (tweet.retweet_count >= twitterState['maxRetweets'] and not tweet.retweeted):
            currentlyDeletingText.set(
                f'Tweet: `{tweetSnippet}` has more retweets than max retweets, skipping.')
        else:
            if (twitterState['testRun'] == 0):

                currentlyDeletingText.set(f'Deleting tweet: `{tweetSnippet}`')

                twitterState['api'].destroy_status(tweet.id)
            else:
                currentlyDeletingText.set(f'-TEST RUN- Would delete tweet: `{tweetSnippet}`')

        numDeletedItemsText.set(f'{str(count)}/{str(totalTweets)} items processed.')
        deletionProgressBar['value'] = round((count / totalTweets) * 100, 1)

        root.update()

        count += 1


def delete_twitter_favorites(root, currentlyDeletingText, deletionProgressBar, numDeletedItemsText):
    userFavorites = []

    # make initial request for most recent favorites
    #  (200 is the maximum allowed count)
    newFavorites = twitterState['api'].favorites(count=200)

    # save most recent favorite
    userFavorites.extend(newFavorites)

    # save the id of the oldest favorite less one
    oldest = userFavorites[-1].id - 1

    # # keep grabbing favorites until there are no favorites left to grab
    while len(newFavorites) > 0:
        # all requests use the max_id param to prevent duplicates
        newFavorites = twitterState['api'].favorites(count=200, max_id=oldest)

        # save most recent tweets
        userFavorites.extend(newFavorites)

        # update the id of the oldest tweet less one
        oldest = userFavorites[-1].id - 1

    # for favorite in userFavorites:
    #     print(favorite.text)

    totalFavorites = len(userFavorites)

    numDeletedItemsText.set(f'0/{str(totalFavorites)} items processed so far')

    count = 1
    for favorite in userFavorites:
        favoriteSnippet = favorite.text[0:50]
        if len(favorite.text) > 50:
            favoriteSnippet = favoriteSnippet + '...'
        for char in favoriteSnippet:
            # tkinter can't handle certain unicode characters,
            #  so we strip them
            if (ord(char) > 65535):
                favoriteSnippet = favoriteSnippet.replace(char, '')

        currentlyDeletingText.set(f'Deleting favorite: `{favoriteSnippet}`')

        timeCreated = arrow.Arrow.fromdatetime(favorite.created_at)

        if (timeCreated > twitterState['timeToSave']):
            currentlyDeletingText.set(f'Favorite: `{favoriteSnippet}` is more recent than cutoff, skipping.')
        else:
            currentlyDeletingText.set(f'Deleting favorite: `{favoriteSnippet}`')
            twitterState['api'].destroy_favorite(favorite.id)

        numDeletedItemsText.set(
            f'{str(count)}/{str(totalFavorites)} items processed.')
        deletionProgressBar['value'] = round((count / totalFavorites) * 100, 1)

        root.update()

        count += 1


# Set whether to run a test run or not (stored in twitterState)
# testRunBool - 0 for real run, 1 for test run
def setTwitterTestRun(testRunBool):
    twitterState['testRun'] = testRunBool.get()


# neccesary global bool for the scheduler
alreadyRanBool = False


def setTwitterScheduler(root, schedulerBool, hourOfDay, stringVar, progressVar):
    global alreadyRanBool
    if not schedulerBool.get():
        alreadyRanBool = False
        return

    currentTime = datetime.now().time().hour

    if (currentTime == hourOfDay and not alreadyRanBool):
        messagebox.showinfo(
            'Scheduler', 'Social Amnesia is now erasing your past on twitter.')

        deleteTwitterTweets(root, stringVar, progressVar, stringVar)
        delete_twitter_favorites(root, stringVar, progressVar, stringVar)

        alreadyRanBool = True
    if (currentTime < 23):
        if (currentTime == hourOfDay + 1):
            alreadyRanBool = False
    else:
        if (currentTime == 0):
            alreadyRanBool = False

    root.after(1000, lambda: setTwitterScheduler(
        root, schedulerBool, hourOfDay, stringVar, progressVar))
