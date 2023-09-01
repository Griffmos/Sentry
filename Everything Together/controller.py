import clientPersonTracking
import RPiMotorController
from time import sleep
import time

from threading import Thread

maxSpeed:float=3.14
minSpeed:float = RPiMotorController.toRadiansPerSecond(14000)

Karea:float=0.8

Kdist:float=0.5

 # ~ Kdamp:float=0.3

maxArea:float = 307200 #camera frame size

TIMES_TARGET_NONE_TO_STOP=2


def calcSpeed(currTarget:list, lastSpeed:float):

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
    
    
    # ~ speedDiff=abs(lastSpeed-speed)
    
    # ~ dampeningCoeff = Kdamp/(Kdamp if speedDiff==0 else speedDiff)
    
    # ~ print(f"speedDiff: {speedDiff}")
    
    # ~ print(f"dampeningCoeff: {dampeningCoeff}")
    
    # ~ speed = speed * (1 if dampeningCoeff>1 else dampeningCoeff)
    

    return max(speed,minSpeed) if speed>0 else min(speed,-minSpeed)

    #print(distFromTarget)



def main():

    tracker = clientPersonTracking.tracker(True, '192.168.1.96', 8888) #.43 for desktop, .96 for laptop
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

            currSpeed:float = calcSpeed(tracker.currTarget, lastSpeed)



            motor.setSpeed(currSpeed)

            lastSpeed=currSpeed
        
        sleep(0.1)


main()    
