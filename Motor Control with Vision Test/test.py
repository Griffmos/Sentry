import personTracking
import RPiMotorController

from time import sleep

personTracker = personTracking.tracker(True)

motor = RPiMotorController.stepperMotor()

maxSpeed:float=1.58

Ka:float

maxArea:float = 307200 #camera frame size


def calcSpeed(currTarget:list):

    target:list=currTarget[0]

    distFromTarget = 320-target[0]

    if (abs(distFromTarget)<25):
        return 0
    

    distCoeff=-1*(distFromTarget/320)


    

    box:list = currTarget[1]

    area:float=(box[2]-box[0])*(box[3]-box[1])

    areaCoeff= (maxArea-area)/maxArea



    return maxSpeed*distCoeff*areaCoeff

    #print(distFromTarget)


while (True):
    currTarget = personTracker.startSearch()

    #print(currTarget)

    currSpeed:float = calcSpeed(currTarget=currTarget)
    
    
   
    
    print(currSpeed)
    


    


    motor.setSpeed(currSpeed)

    sleep(0.05)


    

    