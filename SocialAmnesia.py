import os
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from tkinter import messagebox

from services import reddit, twitter

user_home = os.path.expanduser('~')


def create_storage_folder():
    storage_folder_path = os.path.join(user_home, '.SocialAmnesia')
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


class MainApp(tk.Frame):
    def __init__(self, master: tk.Tk, **kw):
        self.master = master
        super().__init__(self.master, **kw)

        self.tabs = ttk.Notebook(self.master)
        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.master.title('Social Amnesia')
        self.master.protocol('WM_DELETE_WINDOW', self.master.withdraw)
        self.master.createcommand('tk::mac::ReopenApplication', self.master.deiconify)
        self.master.report_callback_exception = self.handle_callback_error

    def create_widgets(self):
        self.setup_tabs()

    def setup_tabs(self):
        login_frame = tk.Frame(self.tabs)

        self.build_login_tab(login_frame)
        self.tabs.add(login_frame, text='Login to accounts')

        reddit_frame = tk.Frame(self.tabs)
        self.build_reddit_tab(reddit_frame)
        self.tabs.add(reddit_frame, text='Reddit')

        twitter_frame = tk.Frame(self.tabs)
        self.build_twitter_tab(twitter_frame)
        self.tabs.add(twitter_frame, text='Twitter')

        self.tabs.pack(expand=1, fill='both')

    def handle_callback_error(*args):
        """
        Informs the user of errors in a friendly manner
        :param args: list of errors
        :return: None
        """
        received_error = str(args[1])
        errors = {
            # reddit error, happens if you try to run `reddit.user.me()` and login fails
            'received 401 HTTP response': 'Failed to login to reddit!',
            "'user'": 'You are not logged into reddit!',
            "[{'code': 215, 'message': 'Bad Authentication data.'}]": 'Failed to login to twitter!',
            'list index out of range': 'No tweets or favorites found!',
            "'api'": 'You are not logged in to twitter!'
        }

        messagebox.showerror('Error', errors.get(received_error, received_error))

    def build_login_tab(self, login_frame: tk.Frame):
        """
        Builds the tab that lets the user log into their social media accounts
        :param login_frame:
        :return:
        """
        login_frame.grid()
        self.build_reddit_frame(login_frame)
        self.build_twitter_frame(login_frame)

    @staticmethod
    def build_twitter_frame(login_frame: tk.Frame):
        # twitter login
        twitter_label = tk.Label(login_frame, text='twitter')
        twitter_label.config(font=('arial', 25))
        twitter_consumer_key_label = tk.Label(login_frame, text='Enter twitter Consumer Key:')
        twitter_consumer_key_entry = tk.Entry(login_frame)
        twitter_consumer_secret_label = tk.Label(login_frame, text='Enter twitter Consumer Secret:')
        twitter_consumer_secret_entry = tk.Entry(login_frame)
        twitter_access_token_label = tk.Label(login_frame, text='Enter twitter Access Token:')
        twitter_access_token_entry = tk.Entry(login_frame)
        twitter_access_token_secret_label = tk.Label(login_frame, text='Enter twitter Access Token Secret:')
        twitter_access_token_secret_entry = tk.Entry(login_frame)
        twitter_login_confirm_text = tk.StringVar()
        twitter_login_confirm_text.set('Waiting for Login')
        twitter_login_confirmed_label = tk.Label(login_frame, textvariable=twitter_login_confirm_text)
        twitter_login_button = tk.Button(
            login_frame, text='Login to twitter',
            command=lambda: twitter.setTwitterLogin(
                twitter_consumer_key_entry.get(),
                twitter_consumer_secret_entry.get(),
                twitter_access_token_entry.get(),
                twitter_access_token_secret_entry.get(),
                twitter_login_confirm_text)
        )

        twitter_label.grid(row=0, column=2, columnspan=2)
        twitter_consumer_key_label.grid(row=1, column=2)
        twitter_consumer_key_entry.grid(row=1, column=3)
        twitter_consumer_secret_label.grid(row=2, column=2)
        twitter_consumer_secret_entry.grid(row=2, column=3)
        twitter_access_token_label.grid(row=3, column=2)
        twitter_access_token_entry.grid(row=3, column=3)
        twitter_access_token_secret_label.grid(row=4, column=2)
        twitter_access_token_secret_entry.grid(row=4, column=3)
        twitter_login_button.grid(row=5, column=2)
        twitter_login_confirmed_label.grid(row=5, column=3)

    @staticmethod
    def build_reddit_frame(login_frame: tk.Frame):
        """
        Set up reddit frame
        :param login_frame:
        :return:
        """
        # Create elements
        reddit_label = tk.Label(login_frame, text='reddit')
        reddit_label.config(font=('arial', 25))
        reddit_username_label = tk.Label(login_frame, text='Enter reddit username:')
        reddit_username_entry = tk.Entry(login_frame)
        reddit_password_label = tk.Label(login_frame, text='Enter reddit password:')
        reddit_password_entry = tk.Entry(login_frame)
        reddit_client_id_label = tk.Label(login_frame, text='Enter reddit client ID:')
        reddit_client_id_entry = tk.Entry(login_frame)
        reddit_client_secret_label = tk.Label(login_frame, text='Enter reddit client secret:')
        reddit_client_secret_entry = tk.Entry(login_frame)
        reddit_login_confirm_text = tk.StringVar()
        reddit_login_confirm_text.set('Waiting for Login')
        reddit_login_confirmed_label = tk.Label(login_frame, textvariable=reddit_login_confirm_text)
        reddit_login_button = tk.Button(
            login_frame, text='Login to reddit',
            command=lambda: reddit.set_login(
                reddit_username_entry.get(),
                reddit_password_entry.get(),
                reddit_client_id_entry.get(),
                reddit_client_secret_entry.get(),
                reddit_login_confirm_text,
                False)
        )

        # Place elements
        reddit_label.grid(row=0, column=0, columnspan=2)
        reddit_username_label.grid(row=1, column=0)
        reddit_username_entry.grid(row=1, column=1)
        reddit_password_label.grid(row=2, column=0)
        reddit_password_entry.grid(row=2, column=1)
        reddit_client_id_label.grid(row=3, column=0)
        reddit_client_id_entry.grid(row=3, column=1)
        reddit_client_secret_label.grid(row=4, column=0)
        reddit_client_secret_entry.grid(row=4, column=1)
        reddit_login_button.grid(row=5, column=0)
        reddit_login_confirmed_label.grid(row=5, column=1)

        # If a praw.ini file exists, log in to reddit
        praw_config_file = Path(os.path.join(user_home, '.config/praw.ini'))
        if praw_config_file.is_file():
            reddit.set_login('', '', '', '', reddit_login_confirm_text, True)

    @staticmethod
    def build_reddit_tab(reddit_frame: tk.Frame):
        """
        Build the tab that will handle reddit configuration and actions
        :param reddit_frame: frame to set up
        :return: None
        """
        reddit_frame.grid()

        # Configuration section title
        configuration_label = tk.Label(reddit_frame, text='Configuration')
        configuration_label.config(font=('arial', 25))

        # Configuration to set total time of items to save
        current_time_to_save = tk.StringVar()
        current_time_to_save.set('Currently set to save: [nothing]')
        time_keep_label = tk.Label(reddit_frame, text='Keep comments/submissions younger than: ')

        # TODO: reduce redundancy
        hours_drop_down = ttk.Combobox(reddit_frame, width=2)
        hours_drop_down['values'] = build_number_list(24)
        hours_drop_down['state'] = 'readonly'
        hours_drop_down.current(0)

        days_drop_down = ttk.Combobox(reddit_frame, width=2)
        days_drop_down['values'] = build_number_list(7)
        days_drop_down['state'] = 'readonly'
        days_drop_down.current(0)

        weeks_drop_down = ttk.Combobox(reddit_frame, width=2)
        weeks_drop_down['values'] = build_number_list(52)
        weeks_drop_down['state'] = 'readonly'
        weeks_drop_down.current(0)

        years_drop_down = ttk.Combobox(reddit_frame, width=2)
        years_drop_down['values'] = build_number_list(15)
        years_drop_down['state'] = 'readonly'
        years_drop_down.current(0)

        hours_label = tk.Label(reddit_frame, text='hours')
        days_label = tk.Label(reddit_frame, text='days')
        weeks_label = tk.Label(reddit_frame, text='weeks')
        years_label = tk.Label(reddit_frame, text='years')

        time_currently_set_label = tk.Label(reddit_frame, textvariable=current_time_to_save)
        set_time_button = tk.Button(
            reddit_frame, text='Set Total Time To Keep',
            command=lambda: reddit.set_reddit_time_to_save(
                hours_drop_down.get(), days_drop_down.get(),
                weeks_drop_down.get(), years_drop_down.get(),
                current_time_to_save)
        )

        # Configuration to set saving items with a certain amount of upvotes
        current_max_score = tk.StringVar()
        current_max_score.set('Currently set to: 0 upvotes')

        max_score_label = tk.Label(reddit_frame, text='Delete comments/submissions less than score:')
        max_score_entry_field = tk.Entry(reddit_frame, width=5)
        max_score_currently_set_label = tk.Label(reddit_frame, textvariable=current_max_score)

        set_max_score_button = tk.Button(
            reddit_frame, text='Set Max Score',
            command=lambda: reddit.set_reddix_max_score(max_score_entry_field.get(), current_max_score)
        )
        set_max_score_unlimited_button = tk.Button(
            reddit_frame, text='Set Unlimited',
            command=lambda: reddit.set_reddix_max_score('Unlimited', current_max_score)
        )

        # Configuration to let user skip over gilded comments
        gilded_skip_bool = tk.IntVar()
        gilded_skip_bool.set(1)
        gilded_skip_label = tk.Label(reddit_frame, text='Skip Gilded comments:')
        gilded_skip_check_button = tk.Checkbutton(
            reddit_frame, variable=gilded_skip_bool,
            command=lambda: reddit.set_reddit_gilded_skip(gilded_skip_bool))

        # Allows the user to actually delete comments or submissions
        deletion_section_label = tk.Label(reddit_frame, text='Deletion')
        deletion_section_label.config(font=('arial', 25))

        currently_deleting_text = tk.StringVar()
        currently_deleting_text.set('')
        deletion_progress_label = tk.Label(reddit_frame, textvariable=currently_deleting_text)

        deletion_progress_bar = ttk.Progressbar(reddit_frame, orient='horizontal',
                                                length=100, mode='determinate')

        num_deleted_items_text = tk.StringVar()
        num_deleted_items_text.set('')
        num_deleted_items_label = tk.Label(reddit_frame, textvariable=num_deleted_items_text)

        delete_comments_button = tk.Button(
            reddit_frame, text='Delete comments',
            command=lambda: reddit.delete_reddit_items(
                root, True, currently_deleting_text,
                deletion_progress_bar, num_deleted_items_text)
        )

        delete_submissions_button = tk.Button(
            reddit_frame, text='Delete submissions',
            command=lambda: reddit.delete_reddit_items(
                root, False, currently_deleting_text,
                deletion_progress_bar, num_deleted_items_text)
        )

        test_run_bool = tk.IntVar()
        test_run_bool.set(1)
        test_run_text = 'TestRun - Checking this will show you what would be deleted, without deleting anything'
        test_run_check_button = tk.Checkbutton(
            reddit_frame, text=test_run_text,
            variable=test_run_bool,
            command=lambda: reddit.set_reddit_test_run(test_run_bool))

        # Allows the user to schedule runs
        scheduler_section_label = tk.Label(reddit_frame, text='Scheduler')
        scheduler_section_label.config(font=('arial', 25))

        scheduler_reddit_bool = tk.IntVar()
        scheduler_reddit_text = 'Select to delete reddit comments + submissions daily at'

        hours_selection_drop_down = ttk.Combobox(reddit_frame, width=2)
        hours_selection_drop_down['values'] = build_number_list(24)
        hours_selection_drop_down['state'] = 'readonly'
        hours_selection_drop_down.current(0)

        scheduler_reddit_check_button = tk.Checkbutton(
            reddit_frame, text=scheduler_reddit_text,
            variable=scheduler_reddit_bool,
            command=lambda: reddit.set_reddit_scheduler(
                root, scheduler_reddit_bool,
                int(hours_selection_drop_down.get()),
                tk.StringVar(), ttk.Progressbar()))

        # This part actually builds the reddit tab
        configuration_label.grid(row=0, columnspan=11, sticky=(tk.N, tk.S), pady=5)

        time_keep_label.grid(row=1, column=0)
        hours_drop_down.grid(row=1, column=1, sticky=(tk.W,))
        hours_label.grid(row=1, column=2, sticky=(tk.W,))
        days_drop_down.grid(row=1, column=3, sticky=(tk.W,))
        days_label.grid(row=1, column=4, sticky=(tk.W,))
        weeks_drop_down.grid(row=1, column=5, sticky=(tk.W,))
        weeks_label.grid(row=1, column=6, sticky=(tk.W,))
        years_drop_down.grid(row=1, column=7, sticky=(tk.W,))
        years_label.grid(row=1, column=8, sticky=(tk.W,))
        set_time_button.grid(row=1, column=9, columnspan=2)
        time_currently_set_label.grid(row=1, column=11)

        max_score_label.grid(row=2, column=0)
        max_score_entry_field.grid(row=2, column=1, columnspan=8, sticky=(tk.W,))
        set_max_score_button.grid(row=2, column=9)
        set_max_score_unlimited_button.grid(row=2, column=10)
        max_score_currently_set_label.grid(row=2, column=11)

        gilded_skip_label.grid(row=3, column=0)
        gilded_skip_check_button.grid(row=3, column=1)

        ttk.Separator(reddit_frame, orient=tk.HORIZONTAL).grid(
            row=4, columnspan=13, sticky=(tk.E, tk.W), pady=5)

        deletion_section_label.grid(row=5, columnspan=11, sticky=(tk.N, tk.S), pady=5)

        delete_comments_button.grid(row=6, column=0, sticky=tk.W)
        delete_submissions_button.grid(row=6, column=0, sticky=(tk.E,))
        test_run_check_button.grid(row=6, column=1, columnspan=11)

        deletion_progress_label.grid(row=7, column=0)
        deletion_progress_bar.grid(row=8, column=0, sticky=(tk.W,))
        num_deleted_items_label.grid(row=8, column=0, sticky=(tk.E,))

        ttk.Separator(reddit_frame, orient=tk.HORIZONTAL).grid(
            row=9, columnspan=13, sticky=(tk.E, tk.W), pady=5)

        scheduler_section_label.grid(row=10, columnspan=11, sticky=(tk.N, tk.S), pady=5)

        scheduler_reddit_check_button.grid(row=11, column=0)
        hours_selection_drop_down.grid(row=11, column=1)

    @staticmethod
    def build_twitter_tab(frame):
        """
        Builds tab that handles twitter config and actions
        :param frame: frame to set up
        :return:
        """
        frame.grid()

        # Configuration section title
        configuration_label = tk.Label(frame, text='Configuration')
        configuration_label.config(font=('arial', 25))

        # Configuration to set total time of items to save
        current_time_to_save = tk.StringVar()
        current_time_to_save.set('Currently set to save: [nothing]')
        time_keep_label = tk.Label(frame, text='Keep items younger than: ')

        hours_drop_down = ttk.Combobox(frame, width=2)
        hours_drop_down['values'] = build_number_list(24)
        hours_drop_down['state'] = 'readonly'
        hours_drop_down.current(0)

        days_drop_down = ttk.Combobox(frame, width=2)
        days_drop_down['values'] = build_number_list(7)
        days_drop_down['state'] = 'readonly'
        days_drop_down.current(0)

        weeks_drop_down = ttk.Combobox(frame, width=2)
        weeks_drop_down['values'] = build_number_list(52)
        weeks_drop_down['state'] = 'readonly'
        weeks_drop_down.current(0)

        years_drop_down = ttk.Combobox(frame, width=2)
        years_drop_down['values'] = build_number_list(15)
        years_drop_down['state'] = 'readonly'
        years_drop_down.current(0)

        hours_label = tk.Label(frame, text='hours')
        days_label = tk.Label(frame, text='days')
        weeks_label = tk.Label(frame, text='weeks')
        years_label = tk.Label(frame, text='years')

        time_currently_set_label = tk.Label(frame, textvariable=current_time_to_save)
        set_time_button = tk.Button(
            frame, text='Set Total Time To Keep',
            command=lambda: twitter.setTwitterTimeToSave(
                hours_drop_down.get(), days_drop_down.get(),
                weeks_drop_down.get(), years_drop_down.get(), current_time_to_save)
        )

        # Configuration to set saving items with a certain amount of favorites
        current_max_favorites = tk.StringVar()
        current_max_favorites.set('Currently set to: 0 Favorites')
        max_favorites_label = tk.Label(frame, text='Delete tweets that have fewer favorites than:')
        max_favorites_entry_field = tk.Entry(frame, width=5)
        max_favorites_currently_set_label = tk.Label(frame, textvariable=current_max_favorites)
        set_max_favorites_button = tk.Button(
            frame, text='Set Max Favorites',
            command=lambda: twitter.setTwitterMaxFavorites(
                max_favorites_entry_field.get(), current_max_favorites)
        )
        set_max_favorites_unlimited_button = tk.Button(
            frame, text='Set Unlimited',
            command=lambda: twitter.setTwitterMaxFavorites('Unlimited', current_max_favorites)
        )

        # Configuration to set saving items with a certain amount of retweets
        current_max_retweets = tk.StringVar()
        current_max_retweets.set('Currently set to: 0 Retweets')
        max_retweets_label = tk.Label(frame, text='Delete tweets that have fewer retweets than: ')
        max_retweets_entry_field = tk.Entry(frame, width=5)
        max_retweets_currently_set_label = tk.Label(frame, textvariable=current_max_retweets)
        set_max_retweets_button = tk.Button(
            frame, text='Set Max Retweets',
            command=lambda: twitter.setTwitterMaxRetweets(
                max_retweets_entry_field.get(), current_max_retweets)
        )
        set_max_retweets_unlimited_button = tk.Button(
            frame, text='Set Unlimited',
            command=lambda: twitter.setTwitterMaxRetweets(
                'Unlimited', current_max_retweets)
        )

        # Allows the user to delete tweets or remove favorites
        deletion_section_label = tk.Label(frame, text='Deletion')
        deletion_section_label.config(font=('arial', 25))

        currently_deleting_text = tk.StringVar()
        currently_deleting_text.set('')

        deletion_progress_label = tk.Label(frame, textvariable=currently_deleting_text)
        deletion_progress_bar = ttk.Progressbar(frame, orient='horizontal',
                                                length=100, mode='determinate')

        num_deleted_items_text = tk.StringVar()
        num_deleted_items_text.set('')
        num_deleted_items_label = tk.Label(frame, textvariable=num_deleted_items_text)

        delete_comments_button = tk.Button(
            frame, text='Delete tweets',
            command=lambda: twitter.deleteTwitterTweets(
                root, currently_deleting_text, deletion_progress_bar, num_deleted_items_text)
        )

        delete_submissions_button = tk.Button(
            frame, text='Remove Favorites',
            command=lambda: twitter.delete_twitter_favorites(
                root, currently_deleting_text, deletion_progress_bar, num_deleted_items_text)
        )

        test_run_bool = tk.IntVar()
        test_run_bool.set(1)
        test_run_text = 'TestRun - Checking this will show you what would be deleted, without actually deleting anything'
        test_run_check_button = tk.Checkbutton(
            frame, text=test_run_text,
            variable=test_run_bool,
            command=lambda: twitter.setTwitterTestRun(test_run_bool))

        # Allows the user to schedule runs
        scheduler_section_label = tk.Label(frame, text='Scheduler')
        scheduler_section_label.config(font=('arial', 25))

        scheduler_twitter_bool = tk.IntVar()
        scheduler_twitter_text = 'Select to delete twitter comments + submissions daily at'

        hours_selection_drop_down = ttk.Combobox(frame, width=2)
        hours_selection_drop_down['values'] = build_number_list(24)
        hours_selection_drop_down['state'] = 'readonly'
        hours_selection_drop_down.current(0)

        scheduler_twitter_check_button = tk.Checkbutton(
            frame, text=scheduler_twitter_text,
            variable=scheduler_twitter_bool,
            command=lambda: twitter.setTwitterScheduler(
                root, scheduler_twitter_bool, int(hours_selection_drop_down.get()),
                tk.StringVar(), ttk.Progressbar()))

        # Actually build the twitter tab
        configuration_label.grid(row=0, columnspan=11, sticky=(tk.N, tk.S), pady=5)
        time_keep_label.grid(row=1, column=0)
        hours_drop_down.grid(row=1, column=1, sticky=(tk.W,))
        hours_label.grid(row=1, column=2, sticky=(tk.W,))
        days_drop_down.grid(row=1, column=3, sticky=(tk.W,))
        days_label.grid(row=1, column=4, sticky=(tk.W,))
        weeks_drop_down.grid(row=1, column=5, sticky=(tk.W,))
        weeks_label.grid(row=1, column=6, sticky=(tk.W,))
        years_drop_down.grid(row=1, column=7, sticky=(tk.W,))
        years_label.grid(row=1, column=8, sticky=(tk.W,))
        set_time_button.grid(row=1, column=9, columnspan=2)
        time_currently_set_label.grid(row=1, column=11)

        max_favorites_label.grid(row=2, column=0)
        max_favorites_entry_field.grid(row=2, column=1, columnspan=8, sticky=(tk.W,))
        set_max_favorites_button.grid(row=2, column=9)
        set_max_favorites_unlimited_button.grid(row=2, column=10)
        max_favorites_currently_set_label.grid(row=2, column=11)

        max_retweets_label.grid(row=3, column=0)
        max_retweets_entry_field.grid(row=3, column=1, columnspan=8, sticky=(tk.W,))
        set_max_retweets_button.grid(row=3, column=9)
        set_max_retweets_unlimited_button.grid(row=3, column=10)
        max_retweets_currently_set_label.grid(row=3, column=11)

        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            row=4, columnspan=13, sticky=(tk.E, tk.W), pady=5)

        deletion_section_label.grid(row=5, columnspan=11, sticky=(tk.N, tk.S), pady=5)

        delete_comments_button.grid(row=6, column=0, sticky=(tk.W,))
        delete_submissions_button.grid(row=6, column=0, sticky=(tk.E,))
        test_run_check_button.grid(row=6, column=1, columnspan=11)

        deletion_progress_label.grid(row=7, column=0)
        deletion_progress_bar.grid(row=8, column=0, sticky=(tk.W,))
        num_deleted_items_label.grid(row=8, column=0, sticky=(tk.E,))

        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            row=9, columnspan=13, sticky=(tk.E, tk.W), pady=5)

        scheduler_section_label.grid(row=10, columnspan=11, sticky=(tk.N, tk.S), pady=5)

        scheduler_twitter_check_button.grid(row=11, column=0)
        hours_selection_drop_down.grid(row=11, column=1)


if __name__ == '__main__':
    create_storage_folder()

    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
