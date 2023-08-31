import clientPersonTracking
from time import sleep
import time


def main():

    tracker = clientPersonTracking.tracker(True, '192.168.1.43', 8888)


    while True:
        startTime=time.perf_counter()
        success=tracker.findTarget()
        
        print(tracker.currTarget)
        print(f"total time: {time.perf_counter()-startTime}")



main()