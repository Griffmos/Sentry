
from time import sleep
import personTracking
import fakeMotor

personTracker = personTracking.tracker(True)

print("finished starting person tracker")

motor = fakeMotor.fakeMotor()


print("got to while loop")
while True:

    currTarget = personTracker.startSearch()

    print(currTarget)
    
    motor.runMotor(motor.moveTo, currTarget[0])

    personTracker.displayPoint(motor.currPos, currTarget[1])

    if (currTarget[0]-10<motor.currPos<currTarget[0]+10):
        print("on target!")
    sleep(0.1)

