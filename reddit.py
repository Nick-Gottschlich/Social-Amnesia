# standard python imports
from time import sleep
import os
from pathlib import Path
from datetime import datetime
from tkinter import messagebox

# pip imports
import praw
import arrow

USER_AGENT = 'Social Amensia: v0.1.0 (by /u/JavaOffScript)'

EDIT_OVERWRITE = 'Wiped by Social Amnesia'

prawConfigFile = Path(f'{os.path.expanduser("~")}/.config/praw.ini')

# The reddit state object
#   Handles the actual praw object that manipulate the reddit account
#   as well as any configuration options about how to act.
redditState = {}

# Logs into reddit using PRAW, gives user an error on failure
def setRedditLogin(username, password, clientID, clientSecret, loginConfirmText, init):
    if init:
        try:
            reddit = praw.Reddit('user', user_agent=USER_AGENT)
            reddit.user.me()
        except:
            # praw.ini is broken, delete it
            os.remove(prawConfigFile)
            return
    else:
        reddit = praw.Reddit(
            client_id=clientID,
            client_secret=clientSecret,
            user_agent=USER_AGENT,
            username=username,
            password=password
        )

        if prawConfigFile.is_file():
            os.remove(prawConfigFile)

        prawConfigString = f'''[user]
client_id={clientID}
client_secret={clientSecret}
password={password}
username={username}'''

        with open(prawConfigFile, 'a') as out:
            out.write(prawConfigString)

    redditUsername = str(reddit.user.me())

    loginConfirmText.set(f'Logged in as {redditUsername}')

    # initialize state
    redditState['user'] = reddit.redditor(redditUsername)
    redditState['recentlyPostedCutoff'] = arrow.now().replace(hours=0)
    redditState['maxScore'] = 0
    redditState['testRun'] = 0
    redditState['gildedSkip'] = 0

# Sets the time of comments or submissions to save, stores it in redditState
#  and updates the UI to show what its currently set to.
#   ____ToSave: the input received from the UI
#   currentTimeToSave: what is stored for the user in the UI
def setTimeToSave(hoursToSave, daysToSave, weeksToSave, yearsToSave, currentTimeToSave):
    totalHours = int(hoursToSave) + (int(daysToSave) * 24) + \
        (int(weeksToSave) * 168) + (int(yearsToSave) * 8736)

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
        currentTimeToSave.set(
            f'Currently set to save: [{yearsText} {weeksText} {daysText} {hoursText}] of items')


# Sets the maximum score level, any posts above this store will be skipped over
#  updates the UI to show what its currently set to.
#   maxScore: the input received from the UI
#   currentMaxScore: what is stored for the user in the UI
def setMaxScore(maxScore, currentMaxScore):
    if (maxScore == ''):
        maxScore = 0
    elif (maxScore == 'Unlimited'):
        redditState['maxScore'] = 9999999999
    else:
        maxScore = int(maxScore)
        redditState['maxScore'] = maxScore

    currentMaxScore.set(f'Currently set to: {str(maxScore)} upvotes')


# Set whether to skip gilded comments or not (stored in redditState)
#   gildedSkipBool - 0 to delete gilded comments, 1 to skip gilded comments
def setGildedSkip(gildedSkipBool):
    if (gildedSkipBool.get()):
        redditState['gildedSkip'] = gildedSkipBool.get()


# Deletes the items according to user configurations.
#   commentBool: true if deleting comments, false if deleting submissions
#   currentlyDeletingText: Describes the item that is currently being deleted.
#   deletionProgressBar: updates as the items are looped through
#   numDeletedItemsText: updates as X out of Y comments are looped through
#   root: the reference to the actual tkinter GUI window
def deleteItems(root, commentBool, currentlyDeletingText, deletionProgressBar, numDeletedItemsText):
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
            for char in itemSnippet:
                # tkinter can't handle certain unicode characters,
                #  so we strip them
                if (ord(char) > 65535):
                    itemSnippet = itemSnippet.replace(char, '')
        else:
            itemString = 'Submission'
            itemSnippet = item.title[0:15]
            if len(item.title) > 15:
                itemSnippet = itemSnippet + '...'
            for char in itemSnippet:
                # tkinter can't handle certain unicode characters,
                #  so we strip them
                if (ord(char) > 65535):
                    itemSnippet = itemSnippet.replace(char, '')

        timeCreated = arrow.get(item.created_utc)

        if (timeCreated > redditState['recentlyPostedCutoff']):
            currentlyDeletingText.set(
                f'{itemString} `{itemSnippet}` more recent than cutoff, skipping.')
        elif (item.score > redditState['maxScore']):
            currentlyDeletingText.set(
                f'{itemString} `{itemSnippet}` is higher than max score, skipping.')
        elif (item.gilded and redditState['gildedSkip']):
            currentlyDeletingText.set(
                f'{itemString} `{itemSnippet}` is gilded, skipping.')
        else:
            if (redditState['testRun'] == 0):
                # Need the try/except here as it will crash on
                #  link submissions otherwise
                try:
                    item.edit(EDIT_OVERWRITE)
                except:
                    ayy = 'lmao'

                item.delete()

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


# Set whether to run a test run or not (stored in redditState)
# testRunBool - 0 for real run, 1 for test run
def setTestRun(testRunBool):
    redditState['testRun'] = testRunBool.get()


# neccesary global bool for the scheduler
alreadyRanBool = False

# reddit scheduler
#   root: tkinkter window
#   schedulerBool: true if set to run, false otherwise
#   hourOfDay: int 0-23, sets hour of day to run on
#   stringVar, progressVar - empty Vars needed to run the deleteItems function
def setRedditScheduler(root, schedulerBool, hourOfDay, stringVar, progressVar):
    global alreadyRanBool
    if not schedulerBool.get():
        alreadyRanBool = False
        return

    currentTime = datetime.now().time().hour

    if (currentTime == hourOfDay and not alreadyRanBool):
        messagebox.showinfo(
            'Scheduler', 'Social Amnesia is now erasing your past on reddit.')

        deleteItems(root, True, stringVar, progressVar, stringVar)
        deleteItems(root, False, stringVar, progressVar, stringVar)

        alreadyRanBool = True
    if (currentTime < 23):
        if (currentTime == hourOfDay + 1):
            alreadyRanBool = False
    else:
        if (currentTime == 0):
            alreadyRanBool = False

    root.after(1000, lambda: setRedditScheduler(
        root, schedulerBool, hourOfDay, stringVar, progressVar))
