import clientPersonTracking
from time import sleep


def main():

    tracker = clientPersonTracking.tracker(True, '192.168.1.43', 8888)


    while True:
        success=tracker.findTarget()
        
        print(tracker.currTarget)



main()