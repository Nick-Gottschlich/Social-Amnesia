from datetime import datetime

from reddit import deleteItems

alreadyRanBool = False

# reddit scheduler
def setRedditScheduler(root, schedulerBool, stringVar, progressVar):
    global alreadyRanBool
    if not schedulerBool.get():
        return

    print(datetime.now().time().hour)

    if (datetime.now().time().hour == 22 and not alreadyRanBool):
        print('it is 10pm my dudes')
        deleteItems(root, True, stringVar, progressVar, stringVar)
        deleteItems(root, False, stringVar, progressVar, stringVar)
        alreadyRanBool = True
    if (datetime.now().time().hour == 23):
        alreadyRanBool = False

        
    root.after(1000, lambda: setRedditScheduler(root, schedulerBool, stringVar, progressVar))
