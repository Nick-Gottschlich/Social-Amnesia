import schedule
import time

# reddit scheduler
def setRedditScheduler(root, schedulerBool):
    print(schedulerBool.get())
    if not schedulerBool.get():
        return
    # schedule.every().second.do(lambda: print('ayy lmao'))

    # while(schedulerBool.get()):
    #     schedule.run_con
    #     time.sleep(1)

    print ('ayy lmao')
    root.after(1000, lambda: setRedditScheduler(root, schedulerBool))
