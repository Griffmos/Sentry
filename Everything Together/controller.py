import clientPersonTracking
import RPiMotorController
import constants
import RPi.GPIO as GPIO
from time import sleep
import time
import PIDcontroller
#import keyboard

from threading import Thread
import gunController

maxSpeed:float=1.58
minSpeed:float = RPiMotorController.toRadiansPerSecond(14000)
maxArea:float = constants.SCREEN_AREA #camera frame size


Karea:float=0.1

Kdist:float=0.2

Kerror:float=0.1    

NONE_TARGET_SPEED_DIVISOR = 2
TIMES_TARGET_NONE_TO_STOP = 1
#pixels
SHOOTING_DISTANCE = 20 
STOPPING_DISTANCE = 10


STOP_BUTTON_PIN = 15

# ~ Kdamp:float=0.3






def calcSpeed(currTarget:list):

    if (currTarget is None):
        return 0


    #distance term
    target:list=currTarget[0]
    

    distFromTarget = (constants.SCREEN_WIDTH/2)-target[0]
    
    direction = 1 if distFromTarget<1 else -1
    
    distFromTarget = abs(distFromTarget)
    
    print(distFromTarget)

    if (distFromTarget<STOPPING_DISTANCE):
        return 0
    

    distCoeff=Kdist*(distFromTarget/(constants.SCREEN_WIDTH/2))

    
    
    #area term
    box:list = currTarget[1]

    area:float=(box[2]-box[0])*(box[3]-box[1])

    areaCoeff= Karea*((maxArea-area)/maxArea)
    
    
    
    #error term
    errorCoeff = Kerror * (distFromTarget)/((calcSpeed.lastError) if calcSpeed.lastError !=0 else distFromTarget)


    #print(f"last error: {calcSpeed.lastError}")

    
    # ~ print(distCoeff)
    # ~ print(errorCoeff)
    # ~ print(areaCoeff)
    

    multiplier = distCoeff+errorCoeff+areaCoeff

    multiplier = min(multiplier, 1)
    
    # ~ print(multiplier)

    
    #dampening term (not using)
    # ~ speedDiff=abs(lastSpeed-speed)
    
    # ~ dampeningCoeff = Kdamp/(Kdamp if speedDiff==0 else speedDiff)
    
    # ~ print(f"speedDiff: {speedDiff}")
    
    # ~ print(f"dampeningCoeff: {dampeningCoeff}")
    
    # ~ speed = speed * (1 if dampeningCoeff>1 else dampeningCoeff)

    speed = maxSpeed*multiplier
    
    print(f"speed: {speed}")
    print(f"multiplier: {multiplier}")
    print(f"direction: {direction}")

    calcSpeed.lastError = distFromTarget
    return direction*max(speed,minSpeed)

    #print(distFromTarget)





    


def main():

    tracker = clientPersonTracking.tracker(True, '192.168.1.96', 8888) #.43 for desktop, .96 for laptop
    motor = RPiMotorController.stepperMotor()
    gun = gunController.Nemesis() 
    PID = PIDcontroller.PIDcontroller(maxSpeed, minSpeed, 0, 0.02, 0.005)
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(STOP_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    


    stop=False
    def quit():
        tracker.terminateTracker()
        motor.terminate()
        gun.shutdown()
        stop=True



    #keyboard.add_hotkey('q', quit)

    noneCounter = 0
    lastSpeed = 0
    calcSpeed.lastError = 0

    while not stop:
        startTime=time.perf_counter()
        success=tracker.findTarget()

    
        
        
        #print(f"total time: {time.perf_counter()-startTime}")

        currTarget = tracker.currTarget
        print(f"currTarget: {currTarget}")
        if (currTarget is None):
            PID.lastError = -1
            if (noneCounter<TIMES_TARGET_NONE_TO_STOP):
                noneCounter+=1
                motor.setSpeed(lastSpeed/NONE_TARGET_SPEED_DIVISOR)
            else:
                motor.setSpeed(0)
                gun.reqShoot(False)
                gun.reqRev(False)
        else:
            noneCounter = 0

            gun.reqRev(True)

            currSpeed:float = -PID.calculate(currTarget)

            motor.setSpeed(currSpeed)

            if (abs((constants.SCREEN_WIDTH/2)-currTarget[0][0])<SHOOTING_DISTANCE):
                gun.reqShoot(True)
            else:
                gun.reqShoot(False)

            lastSpeed=currSpeed
            
        
        if (GPIO.input(STOP_BUTTON_PIN)==GPIO.HIGH):
            print("stopping")
            quit()
            GPIO.cleanup()  
            
        print(f"speed: {motor.currSpeed}")
        
        


main()    
