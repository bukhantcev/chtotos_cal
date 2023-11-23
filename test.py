import time
from threading import Timer


def job():
    print("I'm working...")

t = Timer(5, job)



t.start()
