import schedule
import time

# reddit scheduler
def setRedditScheduler(schedulerBool):
    print(schedulerBool.get())

    schedule.every().second.do(lambda: print('ayy lmao'))

    while(schedulerBool.get()):
        schedule.run_pending()
        time.sleep(1)
