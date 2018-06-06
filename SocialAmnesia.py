# standard python imports
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import os
from pathlib import Path

#local files
from reddit import setRedditLogin, setTimeToSave, setMaxScore, deleteItems, setTestRun, setGildedSkip

# cx_freeze needs this import to run
from multiprocessing import Queue

# define tkinter UI
root = Tk()

# create the storage folder
storageFolder = Path(f'{os.path.expanduser("~")}/.SocialAmnesia')
redditStorageFolder = Path(f'{os.path.expanduser("~")}/.SocialAmnesia/reddit')
if not os.path.exists(storageFolder):
    os.makedirs(storageFolder)
    os.makedirs(redditStorageFolder)

# If the user needs to be informed of an error, this will let tkinter take
#   care of that
def callbackError(self, *args):
    # reddit error, happens if you try to run `reddit.user.me()` 
    #   and login fails
    if (str(args[1]) == 'received 401 HTTP response'):
        messagebox.showerror('ERROR', 'Failed to login to reddit!')
    elif (str(args[1]) == "'user'"):
        messagebox.showerror('ERROR', 'You are not logged into reddit!')
    else:
        messagebox.showerror('ERROR', str(args[1]))


# Builds a list of numbers from 0 up to `max`.
def buildNumberList(max):
    numList = []
    for i in range(0, max):
        numList.append(str(i))
    return numList


# Builds the tab that lets the user log into their social media accounts
def buildLoginTab(loginFrame):
    loginFrame.grid()

    redditLabel = Label(loginFrame, text='reddit')

    redditUsernameLabel = Label(loginFrame, text='Enter reddit username:')
    redditUsernameEntry = Entry(loginFrame)

    redditPasswordLabel = Label(loginFrame, text='Enter reddit password:')
    redditPasswordEntry = Entry(loginFrame)

    redditClientIDLabel = Label(loginFrame, text='Enter reddit client ID:')
    redditClientIDEntry = Entry(loginFrame)

    redditClientSecretLabel = Label(
        loginFrame, text='Enter reddit client secret:')
    redditClientSecretEntry = Entry(loginFrame)

    redditLoginConfirmText = StringVar()
    redditLoginConfirmText.set('Waiting for Login')
    redditLoginConfirmedLabel = Label(
        loginFrame, textvariable=redditLoginConfirmText)

    redditLoginButton = Button(
        loginFrame,
        text='Login to reddit',
        command=lambda: setRedditLogin(redditUsernameEntry.get(), 
                                       redditPasswordEntry.get(),
                                       redditClientIDEntry.get(), 
                                       redditClientSecretEntry.get(),
                                       redditLoginConfirmText,
                                       False)
    )

    redditLabel.grid(row=0, column=0)
    redditUsernameLabel.grid(row=1, column=0)
    redditUsernameEntry.grid(row=1, column=1)
    redditPasswordLabel.grid(row=2, column=0)
    redditPasswordEntry.grid(row=2, column=1)
    redditClientIDLabel.grid(row=3, column=0)
    redditClientIDEntry.grid(row=3, column=1)
    redditClientSecretLabel.grid(row=4, column=0)
    redditClientSecretEntry.grid(row=4, column=1)
    redditLoginButton.grid(row=5, column=0)
    redditLoginConfirmedLabel.grid(row=5, column=1)

    # If a praw.ini file exists, log in to reddit
    prawConfigFile = Path(
        f'{os.path.expanduser("~")}/.config/praw.ini')
    if prawConfigFile.is_file():
        setRedditLogin('', '', '', '', redditLoginConfirmText, True)


# Builds the tab that will handle reddit configuration and actions
def buildRedditTab(redditFrame):
    redditFrame.grid()

    # Configuration section title
    configurationLabel = Label(redditFrame, text='Configuration')
    configurationLabel.config(font=('arial', 25))

    # Configuration to set total time of items to save
    currentTimeToSave = StringVar()
    currentTimeToSave.set('Currently set to save: [nothing]')
    timeKeepLabel = Label(
        redditFrame, text='Keep comments/submissions younger than: ')

    hoursDropDown = Combobox(redditFrame, width=2)
    hoursDropDown['values'] = buildNumberList(24)
    hoursDropDown['state'] = 'readonly'
    hoursDropDown.current(0)

    daysDropDown = Combobox(redditFrame, width=2)
    daysDropDown['values'] = buildNumberList(7)
    daysDropDown['state'] = 'readonly'
    daysDropDown.current(0)

    weeksDropDown = Combobox(redditFrame, width=2)
    weeksDropDown['values'] = buildNumberList(52)
    weeksDropDown['state'] = 'readonly'
    weeksDropDown.current(0)

    yearsDropDown = Combobox(redditFrame, width=2)
    yearsDropDown['values'] = buildNumberList(15)
    yearsDropDown['state'] = 'readonly'
    yearsDropDown.current(0)

    hoursLabel = Label(redditFrame, text='hours')
    daysLabel = Label(redditFrame, text='days')
    weeksLabel = Label(redditFrame, text='weeks')
    yearsLabel = Label(redditFrame, text='years')

    timeCurrentlySetLabel = Label(
        redditFrame, textvariable=currentTimeToSave)
    setTimeButton = Button(
        redditFrame,
        text='Set Total Time To Keep',
        command=lambda: setTimeToSave(
            hoursDropDown.get(), daysDropDown.get(), 
            weeksDropDown.get(), yearsDropDown.get(), currentTimeToSave)
    )

    # Configuration to set saving items with a certain amount of upvotes
    currentMaxScore = StringVar()
    currentMaxScore.set('Currently set to: 0 upvotes')
    maxScoreLabel = Label(
        redditFrame, text='Delete comments/submissions less than score:')
    maxScoreEntryField = Entry(redditFrame, width=5)
    maxScoreCurrentlySetLabel = Label(
        redditFrame, textvariable=currentMaxScore)
    setMaxScoreButton = Button(
        redditFrame,
        text='Set Max Score',
        command=lambda: setMaxScore(maxScoreEntryField.get(), currentMaxScore)
    )
    setMaxScoreUnlimitedButton = Button(
        redditFrame,
        text='Set Unlimited',
        command=lambda: setMaxScore('Unlimited', currentMaxScore)
    )

    # Configuration to let user skip over gilded comments
    gildedSkipBool = IntVar()
    gildedSkipLabel = Label(redditFrame, text='Skip Gilded comments:')
    gildedSkipCheckButton = Checkbutton(
         redditFrame, variable=gildedSkipBool, command=lambda: setGildedSkip(gildedSkipBool))

    # Allows the user to actually delete comments or submissions
    currentlyDeletingText = StringVar()
    currentlyDeletingText.set('')
    deletionProgressLabel = Label(redditFrame, textvariable=currentlyDeletingText)

    deletionProgressBar = Progressbar(
        redditFrame, orient='horizontal', length=100, mode='determinate')

    numDeletedItemsText = StringVar()
    numDeletedItemsText.set('')
    numDeletedItemsLabel = Label(redditFrame, textvariable=numDeletedItemsText)

    deleteCommentsButton = Button(
        redditFrame,
        text='Delete comments',
        command=lambda: deleteItems(True, currentlyDeletingText, deletionProgressBar, numDeletedItemsText, root)
    )

    deleteSubmissionsButton = Button(
        redditFrame,
        text='Delete submissions',
        command=lambda: deleteItems(False, currentlyDeletingText, deletionProgressBar, numDeletedItemsText, root)
    )

    testRunBool = IntVar()
    testRunText = 'TestRun - Checking this will show you what would be deleted, without deleting anything'
    testRunCheckButton = Checkbutton(redditFrame, text=testRunText, variable=testRunBool, command=lambda: setTestRun(testRunBool))

    configurationLabel.grid(row=0, columnspan=11, sticky=(N, S), pady=5)

    timeKeepLabel.grid(row=1, column=0)
    hoursDropDown.grid(row=1, column=1, sticky=(W))
    hoursLabel.grid(row=1, column=2, sticky=(W))
    daysDropDown.grid(row=1, column=3, sticky=(W))
    daysLabel.grid(row=1, column=4, sticky=(W))
    weeksDropDown.grid(row=1, column=5, sticky=(W))
    weeksLabel.grid(row=1, column=6, sticky=(W))
    yearsDropDown.grid(row=1, column=7, sticky=(W))
    yearsLabel.grid(row=1, column=8, sticky=(W))
    setTimeButton.grid(row=1, column=9, columnspan=2)
    timeCurrentlySetLabel.grid(row=1, column=11)

    maxScoreLabel.grid(row=2, column=0)
    maxScoreEntryField.grid(row=2, column=1, columnspan=8, sticky=(W))
    setMaxScoreButton.grid(row=2, column=9)
    setMaxScoreUnlimitedButton.grid(row=2, column=10)
    maxScoreCurrentlySetLabel.grid(row=2, column=11)

    gildedSkipLabel.grid(row=3, column=0)
    gildedSkipCheckButton.grid(row=3, column=1)

    Separator(redditFrame, orient=HORIZONTAL).grid(row=4, columnspan=13, sticky=(E,W), pady=5)

    deleteCommentsButton.grid(row=5, column=0, sticky=(W))
    deleteSubmissionsButton.grid(row=5, column=0, sticky=(E))
    testRunCheckButton.grid(row=5, column=1, columnspan=11)

    deletionProgressLabel.grid(row=6, column=0)
    deletionProgressBar.grid(row=7, column=0, sticky=(W))
    numDeletedItemsLabel.grid(row=7, column=0, sticky=(E))

# Builds and runs the tkinter UI
def createUI():
    Tk.report_callback_exception = callbackError

    root.title('Social Amnesia')

    root.protocol("WM_DELETE_WINDOW", root.withdraw)
    root.createcommand('tk::mac::ReopenApplication', root.deiconify)

    tabs = Notebook(root)

    loginFrame = Frame(tabs)
    buildLoginTab(loginFrame)
    tabs.add(loginFrame, text='Login To Accounts')

    redditFrame = Frame(tabs)
    buildRedditTab(redditFrame)
    tabs.add(redditFrame, text='reddit')

    tabs.pack(expand=1, fill="both")

    root.mainloop()


def main():
    createUI()


if __name__ == '__main__':
    main()
