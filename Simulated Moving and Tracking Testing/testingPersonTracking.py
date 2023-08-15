
from time import sleep
import personTracking

personTracker = personTracking.tracker(True)

print("finished starting person tracker")


print("got to while loop")
while True:
    print(personTracker.startSearch())
    sleep(0.1)

