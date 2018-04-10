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

def setInitState():
  state['user'] = reddit.redditor(REDDIT_USERNAME)

def setHoursToSave(hoursToSave, currentHoursToSave):
  if (hoursToSave == ''):
    hoursToSave = 0
  else:
    hoursToSave = int(hoursToSave)

  state['recentlyPostedCutoff'] = arrow.now().replace(hours=-hoursToSave)
  currentHoursToSave.set(f'Currently set to: {str(hoursToSave)} hours')

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

  currentHoursToSave = StringVar()
  currentHoursToSave.set('Currently set to: 0 hours')

  hoursTextLabel = Label(frame, text='Hours to keep:')
  hoursEntryField = Entry(frame)
  hoursCurrentlySetLabel = Label(frame, textvariable=currentHoursToSave)
  setHoursButton = Button(
    frame,
    text='Set Hours To Keep',
    command=lambda: setHoursToSave(hoursEntryField.get(), currentHoursToSave)
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

  hoursTextLabel.grid(row=0, column=0)
  hoursEntryField.grid(row=0, column=1)
  setHoursButton.grid(row=0, column=2)
  hoursCurrentlySetLabel.grid(row=0, column=3)
  deleteCommentsButton.grid(row=1, column=0)
  deleteSubmissionsButton.grid(row=1, column=1)
  showStateButton.grid(row=2)

  root.mainloop()

def main():
  setInitState()
  createUI()

if __name__ == '__main__':
  main()
