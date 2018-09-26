import os
from datetime import datetime
from pathlib import Path
import arrow
import praw
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import shelve

import sys
sys.path.insert(0, "../utils")

from utils import helpers

USER_AGENT = 'Social Amnesia: v0.2.0 (by /u/JavaOffScript)'
EDIT_OVERWRITE = 'Wiped by Social Amnesia'

praw_config_file_path = Path(f'{os.path.expanduser("~")}/.config/praw.ini')

# neccesary global bool for the scheduler
alreadyRanBool = False

def initialize_reddit_user(login_confirm_text):
    try:
        reddit = praw.Reddit('user', user_agent=USER_AGENT)
        reddit.user.me()
        login_confirm_text.set(f'Logged in to Reddit as {str(reddit.user.me())}')
    except:
        # praw.ini is broken, delete it
        os.remove(praw_config_file_path)


def initialize_reddit_settings():
    reddit_state['user'] = reddit.redditor(str(reddit.user.me()))
    reddit_state['time_to_save'] = arrow.now().replace(hours=0)
    reddit_state['max_score'] = 0
    reddit_state['test_run'] = 1
    reddit_state['gilded_skip'] = 0
    reddit_state['whitelisted_comments'] = {}
    reddit_state['whitelisted_posts'] = {}
    reddit_state.sync


def set_reddit_login(username, password, client_id, client_secret, login_confirm_text):
    """
    Logs into reddit using PRAW, gives user an error on failure
    :param username: input received from the UI
    :param password: input received from the UI
    :param client_id: input received from the UI
    :param client_secret: input received from the UI
    :param login_confirm_text: confirmation text - shown to the user in the UI
    :param init: boolean, true if this is the run performed on startup, false otherwise
    :return: none
    """
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

    initialize_reddit_settings()


def set_reddit_time_to_save(hours_to_save, days_to_save, weeks_to_save, years_to_save, current_time_to_save, reddit_state):
    """
    See set_time_to_save function in utils/helpers.py
    """
    reddit_state['hours'] =  hours_to_save
    reddit_state['days'] = days_to_save
    reddit_state['weeks'] = weeks_to_save
    reddit_state['years'] = years_to_save

    reddit_state['time_to_save'] = helpers.set_time_to_save(hours_to_save, days_to_save, weeks_to_save, years_to_save, current_time_to_save)
    reddit_state.sync


def set_reddit_max_score(max_score, current_max_score, reddit_state):
    """
    See set_max_score function in utils/helpers.py
    """
    reddit_state['max_score'] = helpers.set_max_score(max_score, current_max_score, 'upvotes')
    reddit_state.sync


def set_reddit_gilded_skip(gilded_skip_bool):
    """
    Set whether to skip gilded comments or not
    :param gildedSkipBool: false to delete gilded comments, true to skip gilded comments
    :return: none
    """
    skip_gild = gilded_skip_bool.get()
    if skip_gild:
        reddit_state['gilded_skip'] = skip_gild
        reddit_state.sync


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

    for item in item_array:
        if comment_bool:
            identifying_text = 'comments'
            item_string = 'Comment'
            item_snippet = helpers.format_snippet(item.body, 50)
        else:
            identifying_text = 'posts'
            item_string = 'Submission'
            item_snippet = helpers.format_snippet(item.title, 50)

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
        elif reddit_state[f'whitelisted_{identifying_text}'][item.id]:
            currently_deleting_text.set(
                f'{item_string} `{item_snippet}` is whitelisted, skipping.`'
            )
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
    Set whether to run a test run or not (stored in state)
    :param test_run_bool: 0 for real run, 1 for test run
    :return: none
    """
    reddit_state['test_run'] = test_run_bool.get()
    reddit_state.sync


def set_reddit_scheduler(root, scheduler_bool, hour_of_day, string_var, progress_var):
    """
    The scheduler that users can use to have social amnesia wipe comments at a set point in time, repeatedly.
    :param root: tkinkter window
    :param scheduler_bool: true if set to run, false otherwise
    :param hour_of_day: int 0-23, sets hour of day to run on
    :param string_var, progress_var - empty Vars needed to run the delete_reddit_items function
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


def set_reddit_whitelist(root, comment_bool):
    """
    Creates a window to let users select which comments or posts
        to whitelist
    :param root: the reference to the actual tkinter GUI window
    :param comment_bool: true for comments, false for posts
    :return: none
    """
    #TODO: update this to get whether checkbox is selected or unselected instead of blindly flipping from true to false
    def flip_whitelist_dict(id, identifying_text):
        whitelist_dict = reddit_state[f'whitelisted_{identifying_text}']
        whitelist_dict[id] = not whitelist_dict[id]
        reddit_state[f'whitelisted_{identifying_text}'] = whitelist_dict
        reddit_state.sync

    def onFrameConfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    if comment_bool:
        identifying_text = 'comments'
        item_array = reddit_state['user'].comments.new(limit=None)
    else:
        identifying_text = 'posts'
        item_array = reddit_state['user'].submissions.new(limit=None)

    whitelist_window = tk.Toplevel(root)

    canvas = tk.Canvas(whitelist_window, width=750, height=1000)
    frame = tk.Frame(canvas)

    scrollbar = tk.Scrollbar(whitelist_window, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    canvas.create_window((4,4), window=frame, anchor="nw")

    whitelist_title_label = tk.Label(
        frame, text=f'Pick {identifying_text} to save', font=('arial', 30))

    frame.bind("<Configure>", lambda event,
              canvas=canvas: onFrameConfigure(canvas))

    whitelist_title_label.grid(
        row=0, column=0, columnspan=2, sticky=(tk.N, tk.E, tk.W, tk.S))
    ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
        row=1, columnspan=2, sticky=(tk.E, tk.W), pady=5)
        

    counter = 2
    for item in item_array:
        if (item.id not in reddit_state[f'whitelisted_{identifying_text}']):
            # I wish I could tell you why I need to copy the dictionary of whitelisted items, and then modify it, and then
            #   reassign it back to the persistant shelf. I don't know why this is needed, but it works.
            whitelist_dict = reddit_state[f'whitelisted_{identifying_text}']
            whitelist_dict[item.id] = False
            reddit_state[f'whitelisted_{identifying_text}'] = whitelist_dict
            reddit_state.sync

        whitelist_checkbutton = tk.Checkbutton(frame, command=lambda 
            id=item.id: flip_whitelist_dict(id, identifying_text))

        if (reddit_state[f'whitelisted_{identifying_text}'][item.id]):
            whitelist_checkbutton.select()
        else:
            whitelist_checkbutton.deselect()

        whitelist_checkbutton.grid(row=counter, column=0)
        tk.Label(frame, 
            text=helpers.format_snippet(item.body if comment_bool else item.title, 100)).grid(row=counter,
                column=1)
        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            row=counter+1, columnspan=2, sticky=(tk.E, tk.W), pady=5)

        counter = counter + 2
    
    print(reddit_state[f'whitelisted_{identifying_text}'])
