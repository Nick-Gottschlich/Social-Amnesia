import praw
from secrets import CLIENT_ID, CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD

USER_AGENT='Social Scrubber: v0.0.1 (by /u/JavaOffScript)'

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT,
                     username=REDDIT_USERNAME,
                     password=REDDIT_PASSWORD)

# print(reddit.read_only)  # Output: False
# print(reddit.user)

# print(reddit.redditor('socialScrubberTest').comments)

for comment in reddit.redditor('socialScrubberTester').comments.new(limit=None):
    print(comment.body.split('\n', 1)[0][:79])
