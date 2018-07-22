import os
from datetime import datetime
from pathlib import Path
from tkinter import messagebox
import sys
sys.path.insert(0, "../utils")
from utils import helpers

import arrow
import praw

USER_AGENT = 'Social Amnesia: v0.2.0 (by /u/JavaOffScript)'
EDIT_OVERWRITE = 'Wiped by Social Amnesia'

praw_config_file_path = Path(f'{os.path.expanduser("~")}/.config/praw.ini')

# The reddit state object
# Handles the actual praw object that manipulates the reddit account
# as well as any configuration options about how to act.
reddit_state = {}

# neccesary global bool for the scheduler
alreadyRanBool = False

def set_reddit_login(username, password, client_id, client_secret, login_confirm_text, init):
    """
    Logs into reddit using PRAW, gives user an error on failure
    :param username: input received from the UI - reddit password
    :param password: input received from the UI - reddit username
    :param client_id: input received from the UI - reddit app client id
    :param client_secret: input received from the UI - reddit app client secret
    :param login_confirm_text: confirmation text - shown to the user in the UI
    :param init: boolean, true if this is the run performed on startup, false otherwise
    """
    if init:
        try:
            reddit = praw.Reddit('user', user_agent=USER_AGENT)
            reddit.user.me()
        except:
            # praw.ini is broken, delete it
            os.remove(praw_config_file_path)
            return
    else:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=USER_AGENT,
            username=username,
            password=password
        )

        if praw_config_file_path.is_file():
            os.remove(praw_config_file_path)

        praw_config_string = f'''[user]
client_id={client_id}
client_secret={client_secret}
password={password}
username={username}'''

        with open(praw_config_file_path, 'a') as out:
            out.write(praw_config_string)

    reddit_username = str(reddit.user.me())

    login_confirm_text.set(f'Logged in to Reddit as {reddit_username}')

    # initialize state
    reddit_state['user'] = reddit.redditor(reddit_username)
    reddit_state['time_to_save'] = arrow.now().replace(hours=0)
    reddit_state['max_score'] = 0
    reddit_state['test_run'] = 1
    reddit_state['gilded_skip'] = 0

def set_reddit_time_to_save(hours_to_save, days_to_save, weeks_to_save, years_to_save, current_time_to_save):
    reddit_state['time_to_save'] = helpers.set_time_to_save(hours_to_save, days_to_save,
                     weeks_to_save, years_to_save, current_time_to_save)


def set_reddix_max_score(max_score, current_max_score):
    """
    Sets the maximum score level, any posts above this store will be skipped over
    updates the UI to show what its currently set to.
    :param max_score: the input received from the UI - any comments greater than or equal to this will be saved
    :param current_max_score: text to display for the user in the UI - current max_score
    :return: none
    """
    if max_score == '':
        max_score = 0
    elif max_score == 'Unlimited':
        reddit_state['max_score'] = 9999999999
    else:
        max_score = int(max_score)
        reddit_state['max_score'] = max_score

    current_max_score.set(f'Currently set to: {str(max_score)} upvotes')


def set_reddit_gilded_skip(gilded_skip_bool):
    """
    Set whether to skip gilded comments or not
    :param gildedSkipBool: false to delete gilded comments, true to skip gilded comments
    :return: none
    """
    skip_gild = gilded_skip_bool.get()
    if skip_gild:
        reddit_state['gilded_skip'] = skip_gild


def delete_reddit_items(root, comment_bool, currently_deleting_text, deletion_progress_bar, num_deleted_items_text):
    """
    Deletes the items according to user configurations.
    :param root: the reference to the actual tkinter GUI window
    :param comment_bool: true if deleting comments, false if deleting submissions
    :param currently_deleting_text: Describes the item that is currently being deleted.
    :param deletion_progress_bar: updates as the items are looped through
    :param num_deleted_items_text: updates as X out of Y comments are looped through
    :return: none
    """
    if comment_bool:
        total_items = sum(1 for _ in reddit_state['user'].comments.new(limit=None))
        item_array = reddit_state['user'].comments.new(limit=None)
    else:
        total_items = sum(1 for _ in reddit_state['user'].submissions.new(limit=None))
        item_array = reddit_state['user'].submissions.new(limit=None)

    num_deleted_items_text.set(f'0/{str(total_items)} items processed so far')

    count = 1

    def format_snippet(text, snippet):
        """
        Helper function to format the snippets from reddit comments/submissions
        :param text: full text of item
        :param snippet: 50 char snippet of item
        :return: formatted snippet with '...' if needed
        """
        if len(text) > 50:
            snippet = snippet + '...'
        for char in snippet:
            # tkinter can't handle certain unicode characters,
            # so we strip them
            if ord(char) > 65535:
                snippet = snippet.replace(char, '')
        return snippet

    for item in item_array:
        if comment_bool:
            item_string = 'Comment'
            item_snippet = format_snippet(item.body, item.body[0:50])
        else:
            item_string = 'Submission'
            item_snippet = format_snippet(item.title, item.title[0:50])

        time_created = arrow.get(item.created_utc)

        if time_created > reddit_state['time_to_save']:
            currently_deleting_text.set(
                f'{item_string} `{item_snippet}` more recent than cutoff, skipping.')
        elif item.score > reddit_state['max_score']:
            currently_deleting_text.set(
                f'{item_string} `{item_snippet}` is higher than max score, skipping.')
        elif item.gilded and reddit_state['gilded_skip']:
            currently_deleting_text.set(
                f'{item_string} `{item_snippet}` is gilded, skipping.')
        else:
            if reddit_state['test_run'] == 0:
                # Need the try/except here as it will crash on
                #  link submissions otherwise
                try:
                    item.edit(EDIT_OVERWRITE)
                except:
                    pass

                item.delete()

                currently_deleting_text.set(
                    f'Deleting {item_string} `{item_snippet}`')
            else:
                currently_deleting_text.set(
                    f'TEST RUN: Would delete {item_string} `{item_snippet}`')

        num_deleted_items_text.set(
            f'{str(count)}/{str(total_items)} items processed.')
        deletion_progress_bar['value'] = round(
            (count / total_items) * 100, 1)

        root.update()
        count += 1


def set_reddit_test_run(test_run_bool):
    """
    Set whether to run a test run or not (stored in redditState)
    :param testRunBool: 0 for real run, 1 for test run
    :return: none
    """
    reddit_state['test_run'] = test_run_bool.get()


def set_reddit_scheduler(root, scheduler_bool, hour_of_day, string_var, progress_var):
    """
    The scheduler that users can use to have social amnesia wipe comments at a set point in time, repeatedly.
    :param root: tkinkter window
    :param schedulerBool: true if set to run, false otherwise
    :param hourOfDay: int 0-23, sets hour of day to run on
    :param stringVar, progressVar - empty Vars needed to run the deleteRedditItems function
    :return: none
    """
    global alreadyRanBool
    if not scheduler_bool.get():
        alreadyRanBool = False
        return

    current_time = datetime.now().time().hour

    if current_time == hour_of_day and not alreadyRanBool:
        messagebox.showinfo('Scheduler', 'Social Amnesia is now erasing your past on reddit.')

        delete_reddit_items(root, True, string_var, progress_var, string_var)
        delete_reddit_items(root, False, string_var, progress_var, string_var)

        alreadyRanBool = True
    if current_time < 23 and current_time == hour_of_day + 1:
        alreadyRanBool = False
    elif current_time == 0:
        alreadyRanBool = False

    root.after(1000, lambda: set_reddit_scheduler(
        root, scheduler_bool, hour_of_day, string_var, progress_var))
