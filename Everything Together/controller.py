import clientPersonTracking
import RPiMotorController
from time import sleep
import time

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



def main():

    tracker = clientPersonTracking.tracker(True, '192.168.1.43', 8888)
    motor = RPiMotorController.stepperMotor()


    while True:
        startTime=time.perf_counter()
        success=tracker.findTarget()
        
        print(tracker.currTarget)
        print(f"total time: {time.perf_counter()-startTime}")

        currSpeed:float = calcSpeed(tracker.currTarget)

        motor.setSpeed(currSpeed)


main()    
