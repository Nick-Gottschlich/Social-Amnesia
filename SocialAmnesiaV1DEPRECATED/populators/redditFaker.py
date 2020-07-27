"""
Simple script to build up a bunch of comments and submissions on a test subreddit for a test user
"""
import praw
from datetime import datetime

# TODO: Use `os.env`?
from secrets import CLIENT_ID, CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD

USER_AGENT = 'RapidCommenter (by /u/JavaOffScript)'

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD
)

# https://www.reddit.com/r/socialamnesiatest/comments/8w39cr/imma_test_it/
submission = reddit.submission(id='8w39cr')
subreddit = reddit.subreddit('socialamnesiatest')

while True:
    try:
        submission.reply(datetime.now())
        print('comment: ', datetime.now())
    except Exception as e:
        print(e)

    try:
        subreddit.submit(datetime.now(), selftext=datetime.now())
        print('submission: ', datetime.now())
    except Exception as e:
        print(e)
