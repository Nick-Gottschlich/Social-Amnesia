import praw
from tkinter import *
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

def printState():
  print(state)

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
  root = Tk()
  frame = Frame(root)
  
  frame.grid()

  hoursLabel = Label(frame, text="Hours to keep:")
  hoursEntry = Entry(frame)
  setHoursButton = Button(
    frame,
    text="Set Hours To Keep",
    command=lambda: setState(72)
  )

  deleteCommentsButton = Button(
    frame,
    text='Delete comments',
    command=deleteComments
  )

  deleteSubmissionsButton = Button(
    frame,
    text='Delete submissions',
    command=deleteSubmissions
  )

  showStateButton = Button(
    frame,
    text='Show Options',
    command=printState
  )

  hoursLabel.grid(row=0, column=0)
  hoursEntry.grid(row=0, column=1)
  setHoursButton.grid(row=0, column=2)
  deleteCommentsButton.grid(row=1, column=0)
  deleteSubmissionsButton.grid(row=1, column=1)
  showStateButton.grid(row=2)

  root.mainloop()

def main():
  setState()
  createUI()

if __name__ == "__main__":
  main()
