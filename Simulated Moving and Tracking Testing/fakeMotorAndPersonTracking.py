
from time import sleep
import personTracking
import fakeMotor

personTracker = personTracking.tracker(True)

print("finished starting person tracker")

motor = fakeMotor.fakeMotor()


print("got to while loop")
while True:


    print(personTracker.startSearch())
    sleep(0.1)

