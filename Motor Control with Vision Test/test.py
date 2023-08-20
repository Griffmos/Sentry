import personTracking
import RPiMotorController

from time import sleep

personTracker = personTracking.tracker(True)

motor = RPiMotorController.stepperMotor()

maxSpeed:float=1.58

while (True):
    currTarget = personTracker.startSearch()

    print(currTarget)
    
    distFromTarget = 320-currTarget[0]

    print(distFromTarget)

    currSpeed:float
    if (abs(distFromTarget)<50):
        currSpeed=0
    else:
        currSpeed=-1*(distFromTarget/320)*maxSpeed
    
    print(currSpeed)
    


    


    motor.setSpeed(currSpeed)

    sleep(0.05)


    

    