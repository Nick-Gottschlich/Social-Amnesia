import praw
from secrets import CLIENT_ID, CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD

USER_AGENT = 'Social Scrubber: v0.0.1 (by /u/JavaOffScript)'

reddit = praw.Reddit(
  client_id=CLIENT_ID,
  client_secret=CLIENT_SECRET,
  user_agent=USER_AGENT,
  username=REDDIT_USERNAME,
  password=REDDIT_PASSWORD
)
user = reddit.redditor(REDDIT_USERNAME)

# print(reddit.read_only)  # Output: False
# print(reddit.user)

# Get and delete comments
def deleteComments(user):
  for comment in user.comments.new(limit=None):
    print(comment.body)
    # comment.delete()
    # print(f'Comment `{comment.body}` Deleted`')

# Get and delete submissions
def deleteSubmissions(user):
  print (user.submissions)
  for submission in user.submissions.new(limit=None):
    # print(submission.title)
    # submission.delete()
    # print(f'Comment `{comment.body}` Deleted`')

# deletecomments(user)
# deleteSubmissions(user)

