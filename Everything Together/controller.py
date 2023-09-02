import clientPersonTracking
import RPiMotorController
from time import sleep
import time

from threading import Thread

maxSpeed:float=1.58
minSpeed:float = RPiMotorController.toRadiansPerSecond(14000)
maxArea:float = 19200 #camera frame size


Karea:float=0.2

Kdist:float=0.3

Kerror:float=0.3

noneSpeedDivisor = 2
TIMES_TARGET_NONE_TO_STOP = 2 

# ~ Kdamp:float=0.3






def calcSpeed(currTarget:list):

    if (currTarget is None):
        return 0


    #distance term
    target:list=currTarget[0]
    

    distFromTarget = 160-target[0]
    
    direction = 1 if distFromTarget<1 else -1
    
    distFromTarget = abs(distFromTarget)

    if (distFromTarget<10):
        return 0
    

    distCoeff=Kdist*(distFromTarget/160)

    
    
    #area term
    box:list = currTarget[1]

    area:float=(box[2]-box[0])*(box[3]-box[1])

    areaCoeff= Karea*((maxArea-area)/maxArea)
    
    
    
    #error term
    errorCoeff = Kerror * (distFromTarget)/((calcSpeed.lastError) if calcSpeed.lastError !=0 else distFromTarget)


    #print(f"last error: {calcSpeed.lastError}")

    
    print(distCoeff)
    print(errorCoeff)
    print(areaCoeff)
    

    multiplier = distCoeff+errorCoeff+areaCoeff

    multiplier = min(multiplier, 1)
    
    print(multiplier)

    
    #dampening term (not using)
    # ~ speedDiff=abs(lastSpeed-speed)
    
    # ~ dampeningCoeff = Kdamp/(Kdamp if speedDiff==0 else speedDiff)
    
    # ~ print(f"speedDiff: {speedDiff}")
    
    # ~ print(f"dampeningCoeff: {dampeningCoeff}")
    
    # ~ speed = speed * (1 if dampeningCoeff>1 else dampeningCoeff)

    speed = maxSpeed*multiplier
    
    print(f"speed: {speed}")

    calcSpeed.lastError = distFromTarget
    return direction*max(speed,minSpeed)

    #print(distFromTarget)



def main():

    tracker = clientPersonTracking.tracker(True, '192.168.1.96', 8888) #.43 for desktop, .96 for laptop
    motor = RPiMotorController.stepperMotor()

    noneCounter = 0
    lastSpeed = 100000
    calcSpeed.lastError = 0

    while True:
        startTime=time.perf_counter()
        success=tracker.findTarget()

    
        
        print(tracker.currTarget)
        print(f"total time: {time.perf_counter()-startTime}")

        currTarget = tracker.currTarget
        if (currTarget is None):
            if (noneCounter<TIMES_TARGET_NONE_TO_STOP):
                noneCounter+=1
                motor.setSpeed(lastSpeed/noneSpeedDivisor)
            else:
                motor.setSpeed(0)
        else:
            noneCounter = 0

            currSpeed:float = calcSpeed(tracker.currTarget)



            motor.setSpeed(currSpeed)

            lastSpeed=currSpeed
        
        sleep(0.1)


main()    
