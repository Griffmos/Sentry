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


# ~ Kdamp:float=0.3






# def calcSpeed(currTarget:list):

#     if (currTarget is None):
#         return 0


#     #distance term
#     target:list=currTarget[0]
    

#     distFromTarget = (constants.SCREEN_WIDTH/2)-target[0]
    
#     direction = 1 if distFromTarget<1 else -1
    
#     distFromTarget = abs(distFromTarget)
    
#     print(distFromTarget)

#     if (distFromTarget<STOPPING_DISTANCE):
#         return 0
    

#     distCoeff=Kdist*(distFromTarget/(constants.SCREEN_WIDTH/2))

    
    
#     #area term
#     box:list = currTarget[1]

#     area:float=(box[2]-box[0])*(box[3]-box[1])

#     areaCoeff= Karea*((maxArea-area)/maxArea)
    
    
    
#     #error term
#     errorCoeff = Kerror * (distFromTarget)/((calcSpeed.lastError) if calcSpeed.lastError !=0 else distFromTarget)


#     #print(f"last error: {calcSpeed.lastError}")

    
#     # ~ print(distCoeff)
#     # ~ print(errorCoeff)
#     # ~ print(areaCoeff)
    

#     multiplier = distCoeff+errorCoeff+areaCoeff

#     multiplier = min(multiplier, 1)
    
#     # ~ print(multiplier)

    
#     #dampening term (not using)
#     # ~ speedDiff=abs(lastSpeed-speed)
    
#     # ~ dampeningCoeff = Kdamp/(Kdamp if speedDiff==0 else speedDiff)
    
#     # ~ print(f"speedDiff: {speedDiff}")
    
#     # ~ print(f"dampeningCoeff: {dampeningCoeff}")
    
#     # ~ speed = speed * (1 if dampeningCoeff>1 else dampeningCoeff)

#     speed = maxSpeed*multiplier
    
#     print(f"speed: {speed}")
#     print(f"multiplier: {multiplier}")
#     print(f"direction: {direction}")

#     calcSpeed.lastError = distFromTarget
#     return direction*max(speed,minSpeed)

#     #print(distFromTarget)








def main():

    tracker = clientPersonTracking.tracker(True, '192.168.1.96', 8888) #.43 for desktop, .96 for laptop
    motor = RPiMotorController.stepperMotor()
    gun = gunController.Nemesis() 
    PID = PIDcontroller.PIDcontroller(constants.controller.maxSpeed, constants.controller.minSpeed, 0, 0.02, 0.005)
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(constants.controller.STOP_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    


    stop=False
    def quit():
        tracker.terminateTracker()
        motor.terminate()
        gun.shutdown()

    def checkButton():
        global stop
        if (GPIO.input(constants.controller.STOP_BUTTON_PIN)==GPIO.HIGH):
                print("stop request from button")
                stop=True
                quit()
                GPIO.cleanup()

    def scanRoutine():
        
        dir:int = 1
        
        while tracker.currTarget is None and not stop:

            if abs(motor.getPos())>=0.9*constants.GEAR_RATIO*constants.STEPS_PER_REV:
                dir = -dir
            
            motor.setSpeed(dir*constants.controller.minSpeed)

            success=tracker.findTarget()



        return True

    runButton = Thread(target=checkButton)

    runButton.start()


    #keyboard.add_hotkey('q', quit)

    noneCounter = 0
    lastSpeed = 0
    
    while not stop:
        startTime=time.perf_counter()
        success=tracker.findTarget()
        
        if not success:
            print("stop request from server")
            stop=True
            quit()
            GPIO.cleanup()
            break

    
        
        
        #print(f"total time: {time.perf_counter()-startTime}")

        currTarget = tracker.currTarget
        print(f"currTarget: {currTarget}")
        if (currTarget is None):
            PID.lastError = -1
            if (noneCounter<constants.controller.TIMES_TARGET_NONE_TO_STOP):
                noneCounter+=1
                motor.setSpeed(lastSpeed/constants.controller.NONE_TARGET_SPEED_DIVISOR)
            else:
                motor.setSpeed(0)
                gun.reqShoot(False)
                gun.reqRev(False)
                scanRoutine()
        else:
            noneCounter = 0

            gun.reqRev(True)

            currSpeed:float = PID.calculate(currTarget)

            motor.setSpeed(currSpeed)

            if (abs((constants.SCREEN_WIDTH/2)-currTarget[0][0])<constants.controller.SHOOTING_DISTANCE):
                gun.reqShoot(True)
            else:
                gun.reqShoot(False)

            lastSpeed=currSpeed
                
            
        print(f"speed: {motor.currSpeed}")
        
    print("shutdown for some reason")
        
        


main()    
