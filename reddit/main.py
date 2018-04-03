import praw
import tkinter as tk
import arrow

from secrets import CLIENT_ID, CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD

USER_AGENT = 'Social Scrubber: v0.0.1 (by /u/JavaOffScript)'

# hardcoded for now, this will eventually be set by user, somehow
reddit = praw.Reddit(
  client_id=CLIENT_ID,
  client_secret=CLIENT_SECRET,
  user_agent=USER_AGENT,
  username=REDDIT_USERNAME,
  password=REDDIT_PASSWORD
)

#lets have a python dictionary that will hold state stuff, that will eventually be factored out to a different file
state = {}

def setState(hoursToSave=0):
  state['user'] = reddit.redditor(REDDIT_USERNAME)
  state['recentlyPostedCutoff'] = arrow.now().replace(hours=-hoursToSave)

# Get and delete comments
def deleteComments():
  for comment in state['user'].comments.new(limit=None):
    timeCreated = arrow.get(comment.created_utc)

    if (timeCreated > state['recentlyPostedCutoff']):
      print (f'Comment `{comment.body}` is more recent than cutoff. skipping')
    else:
      # comment.delete()
      # print(f'Comment `{comment.body}` Deleted`')
      print (f'TESTING: We would delete `{comment.body}`')

# Get and delete submissions
def deleteSubmissions():
  for submission in state['user'].submissions.new(limit=None):
    timeCreated = arrow.get(submission.created_utc)

    if (timeCreated > state['recentlyPostedCutoff']):
      print (f'Comment `{submission.title}` is more recent than cutoff. skipping')
    else:
      # submission.delete()
      # print(f'Comment `{submission.title}` Deleted`')
      print (f'TESTING: We would delete `{submission.title}`')

# Builds and runs the tkinter UI
def createUI():
  root = tk.Tk()
  frame = tk.Frame(root)
  frame.pack()

  deleteCommentsButton = tk.Button(
    frame,
    text='Delete comments',
    fg='red',
    command=deleteComments)
  deleteCommentsButton.pack(side=tk.LEFT)

  deleteSubmissionsButton = tk.Button(
    frame,
    text='Delete submissions',
    fg='red',
    command=deleteSubmissions)
  deleteSubmissionsButton.pack(side=tk.LEFT)

  root.mainloop()

def main():
  setState()
  createUI()

if __name__ == "__main__":
  main()
