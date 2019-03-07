import os
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from tkinter import messagebox
import shelve
import webbrowser

from services import reddit, twitter

USER_HOME_PATH = os.path.expanduser('~')

config_path = Path(f'{os.path.expanduser("~")}/.config')
if not os.path.exists(config_path):
    os.makedirs(config_path)

reddit_state_file_path = Path(
    f'{os.path.expanduser("~")}/.config/reddit_state.db')
reddit_state = shelve.open(str(reddit_state_file_path))

twitter_state_file_path = Path(
    f'{os.path.expanduser("~")}/.config/twitter_state.db')
twitter_state = shelve.open(str(twitter_state_file_path))


def create_storage_folder():
    """
    Creates the folders that can be used to store states between application usage sections.
    :return: none
    """
    storage_folder_path = os.path.join(USER_HOME_PATH, '.SocialAmnesia')
    reddit_storage_folder_path = os.path.join(storage_folder_path, "reddit")

    if not os.path.exists(storage_folder_path):
        os.makedirs(storage_folder_path)
        os.makedirs(reddit_storage_folder_path)


def build_number_list(max_number):
    """
    Builds a list of numbers from 0 up to `max_number`.
    :param max_number: how many numbers to return
    :return: list
    """
    return [str(i) for i in range(max_number)]


def create_dropdown(master: tk.Frame, width: int, value_quantity: int,
                    element_state: str = 'readonly', current: int = 0):
    """
    Creates a set up dropdown
    :param master: parent element
    :param width: width of the element
    :param value_quantity: how many number to create in the dropdown list
    :param element_state: preferably set to 'readonly'
    :param current: current chosen value
    :return: Dropdown element
    """
    dropdown = ttk.Combobox(master, width=width)
    dropdown['values'] = build_number_list(value_quantity)
    dropdown['state'] = element_state
    dropdown.current(current)
    return dropdown


class MainApp(tk.Frame):
    def __init__(self, master: tk.Tk, **kw):
        self.master = master
        super().__init__(self.master, **kw)
        self.configure_gui()

        self.tabs = ttk.Notebook(self.master)
        self.login_frame = self.build_login_tab()
        self.reddit_frame = self.build_reddit_tab()
        self.twitter_frame = self.build_twitter_tab()
        self.create_tabs()

    def configure_gui(self):
        self.master.title('Social Amnesia')
        self.master.protocol('WM_DELETE_WINDOW', self.master.withdraw)
        self.master.createcommand(
            'tk::mac::ReopenApplication', self.master.deiconify)
        self.master.report_callback_exception = self.handle_callback_error

    def create_tabs(self):
        self.tabs.add(self.login_frame, text='Login to accounts')
        self.tabs.add(self.reddit_frame, text='Reddit')
        self.tabs.add(self.twitter_frame, text='Twitter')
        self.tabs.pack(expand=1, fill='both')

    def handle_callback_error(*args):
        """
        Informs the user of errors in a friendly manner
        :param args: list of errors
        :return: None
        """
        print(args)
        received_error = str(args[1])
        errors = {
            "<class 'prawcore.exceptions.ResponseException'>": 'Failed to login to reddit!',
            "<class 'tweepy.error.TweepError'>": 'Failed to login to twitter!',
            "<class 'KeyError'>": 'You are not logged in!',
            "<class 'IndexError'>": 'No tweets/favorites found!',
            "<class 'AttributeError'>": 'You are not logged in!'
        }
        if (received_error.find('KeyError') and received_error != '<class 'KeyError'>'):
            keyErrorString = 'Corrupted database. To fix this, search your machine for the file "reddit_state.db" and delete it, then restart Social Amnesia and log in to reddit again.'
            messagebox.showerror('Error', keyErrorString)
        messagebox.showerror('Error', errors.get(
            received_error, received_error))

    def build_login_tab(self):
        """
        Builds the tab that lets the user log into their social media accounts
        :return: Login frame
        """
        frame = tk.Frame(self.tabs)

        frame.grid()
        frame.columnconfigure(1, pad=20)

        self.build_reddit_login(frame)
        self.build_twitter_login(frame)

        helpUrl = r'https://github.com/Nick-Gottschlich/Social-Amnesia#how-to-set-up-your-reddit-account'

        def openHelpUrl(event):
            webbrowser.open_new(helpUrl)

        howToLink = tk.Label(
            frame, text='Where do I find these values?', fg="blue", cursor="hand2")
        howToLink.bind("<Button-1>", openHelpUrl)
        howToLink.grid(row=6, column=0, sticky='W')

        limitationsText = 'Due to API constraints, Social Amnesia can only index 1,000 items back on reddit, and 3,200 items back on twitter.'
        tk.Label(frame, text=limitationsText).grid(
            row=7, column=0, columnspan=4, sticky='W')

        return frame

    @staticmethod
    def build_twitter_login(frame: tk.Frame):
        """
        Create and place elements for twitter in the login frame
        :param frame: frame to set up, in this case the login tab
        :return: none
        """
        # Create elements
        title = tk.Label(frame, text='Twitter')
        title.config(font=('arial', 25))

        consumer_key_label = tk.Label(
            frame, text='Enter Twitter consumer key:')
        consumer_key_entry = tk.Entry(frame)

        consumer_secret_label = tk.Label(
            frame, text='Enter Twitter consumer secret:')
        consumer_secret_entry = tk.Entry(frame, show="*")

        access_token_label = tk.Label(
            frame, text='Enter Twitter access token:')
        access_token_entry = tk.Entry(frame)

        access_token_secret_label = tk.Label(
            frame, text='Enter Twitter access token secret:')
        access_token_secret_entry = tk.Entry(frame, show="*")

        login_confirm_text = tk.StringVar()
        login_confirm_text.set('Waiting for login')

        login_confirmed_label = tk.Label(
            frame, textvariable=login_confirm_text)

        login_button = tk.Button(
            frame, text='Login to Twitter',
            command=lambda: twitter.set_twitter_login(
                consumer_key_entry.get(),
                consumer_secret_entry.get(),
                access_token_entry.get(),
                access_token_secret_entry.get(),
                login_confirm_text, twitter_state)
        )

        # Place elements
        title.grid(row=0, column=2, columnspan=2, sticky='W')

        consumer_key_label.grid(row=1, column=2, sticky='W')
        consumer_key_entry.grid(row=1, column=3, sticky='W')

        consumer_secret_label.grid(row=2, column=2, sticky='W')
        consumer_secret_entry.grid(row=2, column=3, sticky='W')

        access_token_label.grid(row=3, column=2, sticky='W')
        access_token_entry.grid(row=3, column=3, sticky='W')

        access_token_secret_label.grid(row=4, column=2, sticky='W')
        access_token_secret_entry.grid(row=4, column=3, sticky='W')

        login_button.grid(row=5, column=2, sticky='W')
        login_confirmed_label.grid(row=5, column=3, sticky='W')

        if 'login_info' in twitter_state:
            login_dict = twitter_state['login_info']
            twitter.set_twitter_login(login_dict['consumer_key'], login_dict['consumer_secret'],
                                      login_dict['access_token'], login_dict['access_token_secret'], login_confirm_text, twitter_state)

    @staticmethod
    def build_reddit_login(frame: tk.Frame):
        """
        Create and place elements for reddit in the login frame
        :param frame: frame to set up, in this case the login tab
        :return: None
        """
        # Create elements
        title = tk.Label(frame, text='Reddit')
        title.config(font=('arial', 25))

        username_label = tk.Label(frame, text='Enter Reddit username:')
        username_entry = tk.Entry(frame)

        password_label = tk.Label(frame, text='Enter Reddit password:')
        password_entry = tk.Entry(frame, show="*")

        client_id_label = tk.Label(frame, text='Enter Reddit client ID:')
        client_id_entry = tk.Entry(frame)

        client_secret_label = tk.Label(
            frame, text='Enter Reddit client secret:')
        client_secret_entry = tk.Entry(frame, show="*")

        login_confirm_text = tk.StringVar()
        login_confirm_text.set('Waiting for Login')

        login_confirmed_label = tk.Label(
            frame, textvariable=login_confirm_text)

        login_button = tk.Button(
            frame, text='Login to Reddit',
            command=lambda: reddit.set_reddit_login(
                username_entry.get(),
                password_entry.get(),
                client_id_entry.get(),
                client_secret_entry.get(),
                login_confirm_text,
                reddit_state
            )
        )

        # Place elements
        title.grid(row=0, column=0, columnspan=2, sticky='W')

        username_label.grid(row=1, column=0, sticky='W')
        username_entry.grid(row=1, column=1, sticky='W')

        password_label.grid(row=2, column=0, sticky='W')
        password_entry.grid(row=2, column=1, sticky='W')

        client_id_label.grid(row=3, column=0, sticky='W')
        client_id_entry.grid(row=3, column=1, sticky='W')

        client_secret_label.grid(row=4, column=0, sticky='W')
        client_secret_entry.grid(row=4, column=1, sticky='W')

        login_button.grid(row=5, column=0, sticky='W')
        login_confirmed_label.grid(row=5, column=1, sticky='W')

        reddit.initialize_reddit_user(login_confirm_text, reddit_state)

    def build_reddit_tab(self):
        """
        Build the tab that will handle Reddit configuration and actions
        :return: Set up Reddit frame
        """
        global reddit_state

        frame = tk.Frame(self.tabs)

        configuration_frame = tk.Frame(frame)
        configuration_frame.grid(row=0, column=0, sticky='w')

        deletion_frame = tk.Frame(frame)
        deletion_frame.grid(row=1, column=0, sticky='w')

        scheduler_frame = tk.Frame(frame)
        scheduler_frame.grid(row=2, column=0, sticky='w')

        # Configuration section title
        configuration_label = tk.Label(
            configuration_frame, text='Configuration')
        configuration_label.config(font=('arial', 25))

        # Configuration to set total time of items to save
        current_time_to_save = tk.StringVar()
        if 'hours' in reddit_state:
            def get_text(time, text):
                return '' if time == '0' else time + text

            hours_text = get_text(reddit_state['hours'], 'hours')
            days_text = get_text(reddit_state['days'], 'days')
            weeks_text = get_text(reddit_state['weeks'], 'weeks')
            years_text = get_text(reddit_state['years'], 'years')

            current_time_to_save.set(
                f'Currently set to save: [{years_text} {weeks_text} {days_text} {hours_text}] of items')
        else:
            current_time_to_save.set('Currently set to save: [nothing]')
        time_keep_label = tk.Label(
            configuration_frame, text='Keep comments/submissions younger than: ')

        hours_dropdown = create_dropdown(configuration_frame, 2, 24)
        days_dropdown = create_dropdown(configuration_frame, 2, 7)
        weeks_dropdown = create_dropdown(configuration_frame, 2, 52)
        years_dropdown = create_dropdown(configuration_frame, 2, 15)

        hours_label = tk.Label(configuration_frame, text='hours')
        days_label = tk.Label(configuration_frame, text='days')
        weeks_label = tk.Label(configuration_frame, text='weeks')
        years_label = tk.Label(configuration_frame, text='years')

        time_currently_set_label = tk.Label(
            configuration_frame, textvariable=current_time_to_save)
        set_time_button = tk.Button(
            configuration_frame, text='Set Total Time To Keep',
            command=lambda: reddit.set_reddit_time_to_save(
                hours_dropdown.get(), days_dropdown.get(),
                weeks_dropdown.get(), years_dropdown.get(),
                current_time_to_save, reddit_state)
        )

        # Configuration to set saving items with a certain amount of upvotes
        current_max_score = tk.StringVar()
        if 'max_score' in reddit_state:
            if reddit_state['max_score'] == 9999999999:
                reddit.set_reddit_max_score(
                    'Unlimited', current_max_score, reddit_state)
            else:
                reddit.set_reddit_max_score(
                    reddit_state['max_score'], current_max_score, reddit_state)
        else:
            current_max_score.set('Currently set to: 0 upvotes')

        max_score_label = tk.Label(
            configuration_frame, text='Delete comments/submissions less than score:')
        max_score_entry_field = tk.Entry(configuration_frame, width=5)
        max_score_currently_set_label = tk.Label(
            configuration_frame, textvariable=current_max_score)

        set_max_score_button = tk.Button(
            configuration_frame, text='Set Max Score',
            command=lambda: reddit.set_reddit_max_score(
                max_score_entry_field.get(), current_max_score, reddit_state)
        )
        set_max_score_unlimited_button = tk.Button(
            configuration_frame, text='Set Unlimited',
            command=lambda: reddit.set_reddit_max_score(
                'Unlimited', current_max_score, reddit_state)
        )

        # Configuration to let user skip over gilded comments
        gilded_skip_bool = tk.IntVar()
        # Skip gilded posts by default
        if 'gilded_skip' in reddit_state:
            if reddit_state['gilded_skip'] == 0:
                gilded_skip_bool.set(0)
            else:
                gilded_skip_bool.set(1)
        else:
            gilded_skip_bool.set(1)
        gilded_skip_label = tk.Label(
            configuration_frame, text='Skip Gilded items:')
        gilded_skip_check_button = tk.Checkbutton(
            configuration_frame, variable=gilded_skip_bool,
            command=lambda: reddit.set_reddit_gilded_skip(gilded_skip_bool, reddit_state))

        # White listing
        whitelist_label = tk.Label(
            configuration_frame, text='Whitelist comments or submissions:')
        modify_whitelist_comments_button = tk.Button(
            configuration_frame, text='Pick comments to whitelist',
            command=lambda: reddit.set_reddit_whitelist(
                root, True, reddit_state)
        )
        modify_whitelist_posts_button = tk.Button(
            configuration_frame, text='Pick posts to whitelist',
            command=lambda: reddit.set_reddit_whitelist(
                root, False, reddit_state)
        )

        # Allows the user to actually delete comments or submissions
        deletion_section_label = tk.Label(deletion_frame, text='Deletion')
        deletion_section_label.config(font=('arial', 25))

        currently_deleting_text = tk.StringVar()
        currently_deleting_text.set('')
        deletion_progress_label = tk.Label(
            deletion_frame, textvariable=currently_deleting_text)

        deletion_progress_bar = ttk.Progressbar(
            deletion_frame, orient='horizontal',
            length=100, mode='determinate')

        num_deleted_items_text = tk.StringVar()
        num_deleted_items_text.set('')
        num_deleted_items_label = tk.Label(
            deletion_frame, textvariable=num_deleted_items_text)

        delete_comments_button = tk.Button(
            deletion_frame, text='Delete comments',
            command=lambda: reddit.delete_reddit_items(
                root, True, currently_deleting_text,
                deletion_progress_bar, num_deleted_items_text, reddit_state, False)
        )

        delete_submissions_button = tk.Button(
            deletion_frame, text='Delete submissions',
            command=lambda: reddit.delete_reddit_items(
                root, False, currently_deleting_text,
                deletion_progress_bar, num_deleted_items_text, reddit_state, False)
        )

        # Allows the user to schedule runs
        scheduler_section_label = tk.Label(scheduler_frame, text='Scheduler')
        scheduler_section_label.config(font=('arial', 25))

        scheduler_bool = tk.IntVar()
        scheduler_bool.set(0)

        scheduler_text = 'Select to delete reddit comments + submissions daily at'

        scheduler_hours_dropdown = create_dropdown(scheduler_frame, 2, 24)

        scheduler_currently_set_text = tk.StringVar()
        if 'scheduled_time' in reddit_state:
            scheduler_currently_set_text.set(
                f'Currently set to: {reddit_state["scheduled_time"]}')
        else:
            scheduler_currently_set_text.set('Currently set to: No time set')
        scheduler_currently_set_time_label = tk.Label(
            scheduler_frame, textvariable=scheduler_currently_set_text)

        scheduler_check_button = tk.Checkbutton(
            scheduler_frame, text=scheduler_text,
            variable=scheduler_bool,
            command=lambda: reddit.set_reddit_scheduler(
                root, scheduler_bool,
                int(scheduler_hours_dropdown.get()),
                tk.StringVar(), ttk.Progressbar(), scheduler_currently_set_text, reddit_state))

        # This part actually builds the reddit tab
        configuration_label.grid(row=0, column=0, sticky='w')
        time_keep_label.grid(row=1, column=0, sticky='w')
        hours_dropdown.grid(row=1, column=1, sticky='w')
        hours_label.grid(row=1, column=2, sticky='w')
        days_dropdown.grid(row=1, column=3, sticky='w')
        days_label.grid(row=1, column=4, sticky='w')
        weeks_dropdown.grid(row=1, column=5, sticky='w')
        weeks_label.grid(row=1, column=6, sticky='w')
        years_dropdown.grid(row=1, column=7, sticky='w')
        years_label.grid(row=1, column=8, sticky='w')
        set_time_button.grid(row=1, column=9, columnspan=2)
        time_currently_set_label.grid(row=1, column=11)

        max_score_label.grid(row=2, column=0, sticky='w')
        max_score_entry_field.grid(row=2, column=1, sticky='w')
        set_max_score_button.grid(row=2, column=9, sticky='w')
        set_max_score_unlimited_button.grid(row=2, column=10, sticky='w')
        max_score_currently_set_label.grid(row=2, column=11, sticky='w')

        gilded_skip_label.grid(row=3, column=0, sticky='w')
        gilded_skip_check_button.grid(row=3, column=1, sticky='w')

        whitelist_label.grid(row=4, column=0, sticky='w')
        modify_whitelist_comments_button.grid(
            row=4, column=1, columnspan=4, sticky='w')
        modify_whitelist_posts_button.grid(
            row=4, column=5, columnspan=4, sticky='w')

        ttk.Separator(configuration_frame, orient=tk.HORIZONTAL).grid(
            row=5, columnspan=13, sticky='ew', pady=5)

        deletion_section_label.grid(row=0, column=0, sticky='w')

        delete_comments_button.grid(row=1, column=0, sticky='w')
        delete_submissions_button.grid(row=1, column=1, sticky='w')

        deletion_progress_bar.grid(row=2, column=0, sticky='w')
        num_deleted_items_label.grid(row=2, column=1, sticky='w')
        deletion_progress_label.grid(row=2, column=2, sticky='w')

        ttk.Separator(deletion_frame, orient=tk.HORIZONTAL).grid(
            row=3, columnspan=3, sticky='ew', pady=5)

        scheduler_section_label.grid(
            row=0, column=0, sticky='w')
        scheduler_check_button.grid(row=1, column=0, sticky='w')
        scheduler_hours_dropdown.grid(row=1, column=1, sticky='w')
        scheduler_currently_set_time_label.grid(row=1, column=2, sticky='w')

        return frame

    def build_twitter_tab(self):
        """
        Builds tab that handles twitter config and actions
        :return: A set up Twitter tab
        """
        frame = tk.Frame(self.tabs)

        configuration_frame = tk.Frame(frame)
        configuration_frame.grid(row=0, column=0, sticky='w')

        deletion_frame = tk.Frame(frame)
        deletion_frame.grid(row=1, column=0, sticky='w')

        scheduler_frame = tk.Frame(frame)
        scheduler_frame.grid(row=2, column=0, sticky='w')

        # Configuration section title
        configuration_label = tk.Label(
            configuration_frame, text='Configuration')
        configuration_label.config(font=('arial', 25))

        # Configuration to set total time of items to save
        current_time_to_save = tk.StringVar()
        if 'hours' in twitter_state:
            def get_text(time, text):
                return '' if time == '0' else time + text
            hours_text = get_text(twitter_state['hours'], 'hours')
            days_text = get_text(twitter_state['days'], 'days')
            weeks_text = get_text(twitter_state['weeks'], 'weeks')
            years_text = get_text(twitter_state['years'], 'years')
            current_time_to_save.set(
                f'Currently set to save: [{years_text} {weeks_text} {days_text} {hours_text}] of items')
        else:
            current_time_to_save.set('Currently set to save: [nothing]')
        time_keep_label = tk.Label(
            configuration_frame, text='Keep items younger than: ')

        hours_dropdown = create_dropdown(configuration_frame, 2, 24)
        days_dropdown = create_dropdown(configuration_frame, 2, 7)
        weeks_dropdown = create_dropdown(configuration_frame, 2, 52)
        years_dropdown = create_dropdown(configuration_frame, 2, 15)

        hours_label = tk.Label(configuration_frame, text='hours')
        days_label = tk.Label(configuration_frame, text='days')
        weeks_label = tk.Label(configuration_frame, text='weeks')
        years_label = tk.Label(configuration_frame, text='years')

        time_currently_set_label = tk.Label(
            configuration_frame, textvariable=current_time_to_save)
        set_time_button = tk.Button(
            configuration_frame, text='Set Total Time To Keep',
            command=lambda: twitter.set_twitter_time_to_save(
                hours_dropdown.get(), days_dropdown.get(),
                weeks_dropdown.get(), years_dropdown.get(), current_time_to_save, twitter_state)
        )

        # Configuration to set saving items with a certain amount of favorites
        current_max_favorites = tk.StringVar()
        if 'max_favorites' in twitter_state:
            if twitter_state['max_favorites'] == 9999999999:
                twitter.set_twitter_max_favorites(
                    'Unlimited', current_max_favorites, twitter_state)
            else:
                twitter.set_twitter_max_favorites(
                    twitter_state['max_favorites'], current_max_favorites, twitter_state)
        else:
            current_max_favorites.set('Currently set to: 0 upvotes')
        max_favorites_label = tk.Label(
            configuration_frame, text='Delete tweets that have fewer favorites than:')
        max_favorites_entry_field = tk.Entry(configuration_frame, width=5)
        max_favorites_currently_set_label = tk.Label(
            configuration_frame, textvariable=current_max_favorites)
        set_max_favorites_button = tk.Button(
            configuration_frame, text='Set Max Favorites',
            command=lambda: twitter.set_twitter_max_favorites(
                max_favorites_entry_field.get(), current_max_favorites, twitter_state)
        )
        set_max_favorites_unlimited_button = tk.Button(
            configuration_frame, text='Set Unlimited',
            command=lambda: twitter.set_twitter_max_favorites(
                'Unlimited', current_max_favorites, twitter_state)
        )

        # Configuration to set saving items with a certain amount of retweets
        current_max_retweets = tk.StringVar()
        if 'max_retweets' in twitter_state:
            if twitter_state['max_retweets'] == 9999999999:
                twitter.set_twitter_max_retweets(
                    'Unlimited', current_max_retweets, twitter_state)
            else:
                twitter.set_twitter_max_retweets(
                    twitter_state['max_retweets'], current_max_retweets, twitter_state)
        else:
            current_max_retweets.set('Currently set to: 0 upvotes')
        max_retweets_label = tk.Label(
            configuration_frame, text='Delete tweets that have fewer retweets than: ')
        max_retweets_entry_field = tk.Entry(configuration_frame, width=5)
        max_retweets_currently_set_label = tk.Label(
            configuration_frame, textvariable=current_max_retweets)
        set_max_retweets_button = tk.Button(
            configuration_frame, text='Set Max Retweets',
            command=lambda: twitter.set_twitter_max_retweets(
                max_retweets_entry_field.get(), current_max_retweets, twitter_state)
        )
        set_max_retweets_unlimited_button = tk.Button(
            configuration_frame, text='Set Unlimited',
            command=lambda: twitter.set_twitter_max_retweets(
                'Unlimited', current_max_retweets, twitter_state)
        )

        # White listing tweets or favorites
        whitelist_label = tk.Label(
            configuration_frame, text='Whitelist tweets or favorites:')
        modify_whitelist_tweets_button = tk.Button(
            configuration_frame, text='Pick tweets to whitelist',
            command=lambda: twitter.set_twitter_whitelist(
                root, True, twitter_state)
        )
        modify_whitelist_favorites_button = tk.Button(
            configuration_frame, text='Pick favorites to whitelist',
            command=lambda: twitter.set_twitter_whitelist(
                root, False, twitter_state)
        )

        # Allows the user to delete tweets or remove favorites
        deletion_section_label = tk.Label(deletion_frame, text='Deletion')
        deletion_section_label.config(font=('arial', 25))

        currently_deleting_text = tk.StringVar()
        currently_deleting_text.set('')

        deletion_progress_label = tk.Label(
            deletion_frame, textvariable=currently_deleting_text)
        deletion_progress_bar = ttk.Progressbar(deletion_frame, orient='horizontal',
                                                length=100, mode='determinate')

        num_deleted_items_text = tk.StringVar()
        num_deleted_items_text.set('')
        num_deleted_items_label = tk.Label(
            deletion_frame, textvariable=num_deleted_items_text)

        delete_comments_button = tk.Button(
            deletion_frame, text='Delete tweets',
            command=lambda: twitter.delete_twitter_tweets(
                root, currently_deleting_text, deletion_progress_bar, num_deleted_items_text, twitter_state, False)
        )

        delete_submissions_button = tk.Button(
            deletion_frame, text='Remove Favorites',
            command=lambda: twitter.delete_twitter_favorites(
                root, currently_deleting_text, deletion_progress_bar, num_deleted_items_text, twitter_state, False)
        )

        # Allows the user to schedule runs
        scheduler_section_label = tk.Label(scheduler_frame, text='Scheduler')
        scheduler_section_label.config(font=('arial', 25))

        scheduler_bool = tk.IntVar()
        scheduler_bool.set(0)

        scheduler_text = 'Select to delete twitter comments + submissions daily at'

        scheduler_hours_dropdown = create_dropdown(scheduler_frame, 2, 24)

        scheduler_currently_set_text = tk.StringVar()
        if 'scheduled_time' in twitter_state:
            scheduler_currently_set_text.set(
                f'Currently set to: {twitter_state["scheduled_time"]}')
        else:
            scheduler_currently_set_text.set('Currently set to: No time set')
        scheduler_currently_set_time_label = tk.Label(
            scheduler_frame, textvariable=scheduler_currently_set_text)

        scheduler_check_button = tk.Checkbutton(
            scheduler_frame, text=scheduler_text,
            variable=scheduler_bool,
            command=lambda: twitter.set_twitter_scheduler(
                root, scheduler_bool, int(scheduler_hours_dropdown.get()),
                tk.StringVar(), ttk.Progressbar(), scheduler_currently_set_text, twitter_state))

        # Actually build the twitter tab
        configuration_label.grid(row=0, column=0, sticky='w')
        time_keep_label.grid(row=1, column=0, sticky='w')
        hours_dropdown.grid(row=1, column=1, sticky='w')
        hours_label.grid(row=1, column=2, sticky='w')
        days_dropdown.grid(row=1, column=3, sticky='w')
        days_label.grid(row=1, column=4, sticky='w')
        weeks_dropdown.grid(row=1, column=5, sticky='w')
        weeks_label.grid(row=1, column=6, sticky='w')
        years_dropdown.grid(row=1, column=7, sticky='w')
        years_label.grid(row=1, column=8, sticky='w')
        set_time_button.grid(row=1, column=9, columnspan=2)
        time_currently_set_label.grid(row=1, column=11, sticky='w')

        max_favorites_label.grid(row=2, column=0, sticky='w')
        max_favorites_entry_field.grid(
            row=2, column=1, sticky='w')
        set_max_favorites_button.grid(row=2, column=9, sticky='w')
        set_max_favorites_unlimited_button.grid(row=2, column=10, sticky='w')
        max_favorites_currently_set_label.grid(row=2, column=11, sticky='w')

        max_retweets_label.grid(row=3, column=0, sticky='w')
        max_retweets_entry_field.grid(row=3, column=1, sticky='w')
        set_max_retweets_button.grid(row=3, column=9, sticky='w')
        set_max_retweets_unlimited_button.grid(row=3, column=10, sticky='w')
        max_retweets_currently_set_label.grid(row=3, column=11, sticky='w')

        whitelist_label.grid(row=4, column=0, sticky='w')
        modify_whitelist_tweets_button.grid(
            row=4, column=1, columnspan=4, sticky='w')
        modify_whitelist_favorites_button.grid(
            row=4, column=5, columnspan=4, sticky='w')

        ttk.Separator(configuration_frame, orient=tk.HORIZONTAL).grid(
            row=5, columnspan=13, sticky='ew', pady=5)

        deletion_section_label.grid(row=0, sticky='w')

        delete_comments_button.grid(row=1, column=0, sticky='w')
        delete_submissions_button.grid(row=1, column=1, sticky='w')

        deletion_progress_bar.grid(row=2, column=0, sticky='w')
        num_deleted_items_label.grid(row=2, column=1, sticky='w')
        deletion_progress_label.grid(row=2, column=2, sticky='w')

        ttk.Separator(deletion_frame, orient=tk.HORIZONTAL).grid(
            row=3, columnspan=3, sticky='ew', pady=5)

        scheduler_section_label.grid(
            row=0, column=0, sticky='w')
        scheduler_check_button.grid(row=1, column=0, sticky='w')
        scheduler_hours_dropdown.grid(row=1, column=1, sticky='w')
        scheduler_currently_set_time_label.grid(row=1, column=2, sticky='w')

        return frame


if __name__ == '__main__':
    create_storage_folder()

    root = tk.Tk()
    root.style = ttk.Style()
    root.style.theme_use('clam')
    app = MainApp(root)
    root.mainloop()
