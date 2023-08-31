import clientPersonTracking
from time import sleep


def main():

    tracker = clientPersonTracking.tracker(True, '', '8888')


    while True:
        tracker.findTarget()
        print(tracker.currTarget)

        sleep(0.1)