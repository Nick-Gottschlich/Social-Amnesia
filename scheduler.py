from datetime import datetime
from tkinter import messagebox

from reddit import deleteItems

alreadyRanBool = False

# reddit scheduler
def setRedditScheduler(root, schedulerBool, hourOfDay, stringVar, progressVar):
    global alreadyRanBool
    if not schedulerBool.get():
        alreadyRanBool = False
        return

    currentTime = datetime.now().time().hour

    if (currentTime == hourOfDay and not alreadyRanBool):
        messagebox.showinfo('Scheduler', 'Social Amnesia is now erasing your past on reddit.')

        deleteItems(root, True, stringVar, progressVar, stringVar)
        deleteItems(root, False, stringVar, progressVar, stringVar)

        alreadyRanBool = True
    if (currentTime < 23):
        if (currentTime == hourOfDay + 1):
            alreadyRanBool = False
    else:
        if (currentTime == 0):
            alreadyRanBool = False

    root.after(1000, lambda: setRedditScheduler(root, schedulerBool, hourOfDay, stringVar, progressVar))
