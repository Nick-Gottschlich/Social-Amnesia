# standard python imports
from time import sleep

# pip imports
import praw
import arrow

# auto import and set a login for development purposes
# from secrets import REDDIT_USERNAME, REDDIT_PASSWORD, CLIENT_ID, CLIENT_SECRET

USER_AGENT = 'Social Scrubber: v0.0.1 (by /u/JavaOffScript)'

EDIT_OVERWRITE = 'Scrubbed by Social Scrubber'

# The reddit state object
#   Handles the actual praw object that manipulate the reddit account
#   as well as any configuration options about how to act.
redditState = {}

# Logs into reddit using PRAW, gives user an error on failure
def setRedditLogin(username, password, clientID, clientSecret, loginConfirmText):
    # ============= REAL =================
    reddit = praw.Reddit(
        client_id=clientID,
        client_secret=clientSecret,
        user_agent=USER_AGENT,
        username=username,
        password=password
    )
    # ============= REAL =================

    # ================= FOR TESTING ===================
    # username = REDDIT_USERNAME
    # reddit = praw.Reddit(
    #     client_id=CLIENT_ID,
    #     client_secret=CLIENT_SECRET,
    #     user_agent=USER_AGENT,
    #     username=REDDIT_USERNAME,
    #     password=REDDIT_PASSWORD
    # )
    #================= FOR TESTING ===================

    # confirm successful login
    if (reddit.user.me() == username):
        loginConfirmText.set(f'Logged in as {username}')

        # initialize state
        redditState['user'] = reddit.redditor(username)
        redditState['recentlyPostedCutoff'] = arrow.now().replace(hours=0)
        redditState['maxScore'] = 0
        redditState['testRun'] = 0

# Sets the time of comments or submissions to save, stores it in redditState
#  and updates the UI to show what its currently set to.
# ____ToSave: the input received from the UI
# currentTimeToSave: what is stored for the user in the UI
def setTimeToSave(hoursToSave, daysToSave, weeksToSave, yearsToSave, currentTimeToSave):
    totalHours = int(hoursToSave) + (int(daysToSave) * 24) + (int(weeksToSave) * 168) + (int(yearsToSave) * 8736)

    redditState['recentlyPostedCutoff'] = arrow.now().replace(
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
        currentTimeToSave.set(f'Currently set to save: [{yearsText} {weeksText} {daysText} {hoursText}] of items')


# Sets the maximum score level, any posts above this store will be skipped over
#  updates the UI to show what its currently set to.
# maxScore: the input received from the UI
# currentMaxScore: what is stored for the user in the UI
def setMaxScore(maxScore, currentMaxScore):
    if (maxScore == ''):
        maxScore = 0
    elif (maxScore == 'Unlimited'):
        redditState['maxScore'] = 9999999999
    else:
        maxScore = int(maxScore)
        redditState['maxScore'] = maxScore

    currentMaxScore.set(f'Currently set to: {str(maxScore)} upvotes')


# Deletes the items according to user configurations.
# commentBool: true if deleting comments, false if deleting submissions
# currentlyDeletingText: Describes the item that is currently being deleted.
# deletionProgressBar: updates as the items are looped through
# numDeletedItemsText: updates as X out of Y comments are looped through
# root: the reference to the actual tkinter GUI window
def deleteItems(commentBool, currentlyDeletingText, deletionProgressBar, numDeletedItemsText, root):
    if commentBool:
        totalItems = sum(
            1 for item in redditState['user'].comments.new(limit=None))
        itemArray = redditState['user'].comments.new(limit=None)
    else:
        totalItems = sum(
            1 for item in redditState['user'].submissions.new(limit=None))
        itemArray = redditState['user'].submissions.new(limit=None)

    numDeletedItemsText.set(f'0/{str(totalItems)} items processed so far')

    count = 1
    for item in itemArray:
        if commentBool:
            itemString = 'Comment'
            itemSnippet = item.body[0:15]
            if len(item.body) > 15:
                itemSnippet = itemSnippet + '...'
        else:
            itemString = 'Submission'
            itemSnippet = item.title[0:15]
            if len(item.title) > 15:
                itemSnippet = itemSnippet + '...'

        timeCreated = arrow.get(item.created_utc)

        print(redditState)

        if (timeCreated > redditState['recentlyPostedCutoff']):
            currentlyDeletingText.set(
                f'{itemString} `{itemSnippet}` more recent than cutoff, skipping.')
        elif (item.score > redditState['maxScore']):
            currentlyDeletingText.set(
                f'{itemString} `{itemSnippet}` is higher than max score, skipping.')
        else:
            if (redditState['testRun'] == 0):
                # ==== comment back in once things get real ====
                item.clear_vote()
                Need the try/except here as it will crash on
                 link submissions otherwise
                try:
                    item.edit(EDIT_OVERWRITE)
                except:
                    ayy = 'lmao'
                item.delete()
                # ==== comment out for dev purposes ====
                currentlyDeletingText.set(
                    f'Deleting {itemString} `{itemSnippet}`')
            else:
                currentlyDeletingText.set(
                    f'TEST RUN: Would delete {itemString} `{itemSnippet}`')

        numDeletedItemsText.set(
            f'{str(count)}/{str(totalItems)} items processed.')
        deletionProgressBar['value'] = round(
            (count / totalItems) * 100, 1)
        
        root.update()
        
        count += 1
        
        # Sleep for one second so the user can follow along with the progress
        sleep(1)


# Set whether to run a test run or not (stored in redditState)
# testRunBool - 0 for real run, 1 for test run
def setTestRun(testRunBool):
    redditState['testRun'] = testRunBool.get()
