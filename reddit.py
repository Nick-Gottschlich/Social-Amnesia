# standard python imports
from time import sleep

# pip imports
import praw
import arrow

# auto import and set a login for development purposes
from secrets import REDDIT_USERNAME, REDDIT_PASSWORD, CLIENT_ID, CLIENT_SECRET

USER_AGENT = 'Social Scrubber: v0.0.1 (by /u/JavaOffScript)'

# The reddit state object
#   Handles the actual praw object that manipulate the reddit account
#   as well as any configuration options about how to act.
redditState = {}

# Logs into reddit using PRAW, gives user an error on failure
def setRedditLogin(username, password, clientID, clientSecret, loginConfirmText):
    # ============= REAL =================
    # reddit = praw.Reddit(
    #     client_id=clientID,
    #     client_secret=clientSecret,
    #     user_agent=USER_AGENT,
    #     username=username,
    #     password=password
    # )
    # ============= REAL =================

    # ================= FOR TESTING ===================
    username = REDDIT_USERNAME
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD
    )
    #================= FOR TESTING ===================

    # confirm successful login
    if (reddit.user.me() == username):
        loginConfirmText.set(f'Logged in as {username}')

        redditState['user'] = reddit.redditor(username)
        redditState['recentlyPostedCutoff'] = arrow.now().replace(hours=0)
        redditState['maxScore'] = 0

# Sets the hours of comments or submissions to save, stores it in redditState
#  and updates the UI to show what its currently set to.
# hoursToSave: the input received from the UI
# currentHoursToSave: what is stored for the user in the UI
def setHoursToSave(hoursToSave, currentHoursToSave):
    if (hoursToSave == ''):
        hoursToSave = 0
    else:
        hoursToSave = int(hoursToSave)

    redditState['recentlyPostedCutoff'] = arrow.now().replace(
        hours=-hoursToSave)
    currentHoursToSave.set(f'Currently set to: {str(hoursToSave)} hours')


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
            itemSnippet = item.body[0:100]
        else:
            itemString = 'Submission'
            itemSnippet = item.title[0:100]

        timeCreated = arrow.get(item.created_utc)

        if (timeCreated > redditState['recentlyPostedCutoff']):
            currentlyDeletingText.set(
                f'{itemString} `{itemSnippet}` more recent than cutoff, skipping.')
        elif (item.score > redditState['maxScore']):
            currentlyDeletingText.set(
                f'{itemString} `{itemSnippet}` is higher than max score, skipping.')
        else:
            # ==== comment back in once things get real ====
            # item.delete()

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