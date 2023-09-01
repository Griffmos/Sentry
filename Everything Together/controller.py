import clientPersonTracking
import RPiMotorController
from time import sleep
import time

maxSpeed:float=1.58
minSpeed:float = 0.285 #approx 14000 delay, the max delay

Karea:float=0.5

Kdist:float=0.8

maxArea:float = 307200 #camera frame size

TIMES_TARGET_NONE_TO_STOP=2

def calcSpeed(currTarget:list):

    if (currTarget is None):
        return 0

    target:list=currTarget[0]

    distFromTarget = 320-target[0]

    if (abs(distFromTarget)<25):
        return 0
    

    distCoeff=Kdist*-1*(distFromTarget/320)

    
    

    box:list = currTarget[1]

    area:float=(box[2]-box[0])*(box[3]-box[1])

    areaCoeff= Karea*((maxArea-area)/maxArea)


    multiplier = distCoeff*areaCoeff

    multiplier = min(multiplier, 1)

    speed = maxSpeed*multiplier

    return max(speed,minSpeed) if speed>0 else min(speed,-minSpeed)

    #print(distFromTarget)



def main():

    tracker = clientPersonTracking.tracker(True, '192.168.1.43', 8888)
    motor = RPiMotorController.stepperMotor()

    noneCounter = 0
    lastSpeed = 100000

    while True:
        startTime=time.perf_counter()
        success=tracker.findTarget()
        
        print(tracker.currTarget)
        print(f"total time: {time.perf_counter()-startTime}")

        currTarget = tracker.currTarget
        if (currTarget is None):
            if (noneCounter<TIMES_TARGET_NONE_TO_STOP):
                noneCounter+=1
                motor.setSpeed(lastSpeed)
            else:
                motor.setSpeed(0)
        else:
            noneCounter = 0

            currSpeed:float = calcSpeed(tracker.currTarget)



            motor.setSpeed(currSpeed)

            lastSpeed=currSpeed


main()    
