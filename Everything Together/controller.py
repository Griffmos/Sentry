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


STOP = False

def getStop():
    global STOP
    return STOP
def setStop(val:bool):
    global STOP
    STOP = val
    

def main():

    tracker = clientPersonTracking.tracker(False, '192.168.1.96', 8888) #.43 for desktop, .96 for laptop
    motor = RPiMotorController.stepperMotor()
    gun = gunController.Nemesis() 
    PID = PIDcontroller.PIDcontroller(constants.controller.maxSpeed, constants.controller.minSpeed, 0, 0.02, 0.005)
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(constants.controller.STOP_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    


    def quit():
        motor.terminate()
        sleep(0.01)
        tracker.terminateTracker()
        sleep(0.01)
        gun.shutdown()

    def checkButton():
        
        while not getStop():
            if (GPIO.input(constants.controller.STOP_BUTTON_PIN)==GPIO.HIGH):
                print("stop request from button")
                setStop(True)
                quit()
                GPIO.cleanup()

    def scanRoutine():
        
        dir:int = -1
        
        while tracker.currTarget is None and not getStop():
            print(motor.getPos())
            # ~ print(f"end: {constants.GEAR_RATIO*constants.STEPS_PER_REV*0.9*0.5}")
            # ~ print()

            if abs(motor.getPos())>=0.9*0.5*constants.GEAR_RATIO*constants.STEPS_PER_REV:
                dir = -dir
                motor.setSpeed(dir*0.10)
                sleep(0.1)

            
            motor.setSpeed(dir*0.10)
            
            success=tracker.findTarget()
            if not success:
                setStop(True)
                quit()



        return True

    runButton = Thread(target=checkButton)

    runButton.start()


    #keyboard.add_hotkey('q', quit)

    noneCounter = 0
    lastSpeed = 0
    
    while not getStop():
        startTime=time.perf_counter()
        success=tracker.findTarget()
        
        if not success:
            print("stop request from server")
            setStop(True)
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
                
            
        # ~ print(f"speed: {motor.currSpeed}")
        print(f"pos: {motor.getPos()}")
        
    print("shutdown for some reason")
        
        


main()    
