import RPiMotorController
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 160

SCREEN_AREA = SCREEN_WIDTH*SCREEN_HEIGHT


Pi:float = 3.14159
microsPerSec=1000000


#little gear
STEPS_PER_REV=1600

GEAR_RATIO:float=1/1

DEGREES_PER_STEP:float=360.0/STEPS_PER_REV

class controller:
    maxSpeed:float=1.58
    minSpeed:float = RPiMotorController.toRadiansPerSecond(14000) #14000 is the max delay, and therefor min speed, anything much greater makes the stepper behave weirdly


    Karea:float=0.1

    Kdist:float=0.2

    Kerror:float=0.1    

    NONE_TARGET_SPEED_DIVISOR = 2
    TIMES_TARGET_NONE_TO_STOP = 1
    #pixels
    SHOOTING_DISTANCE = 20 
    STOPPING_DISTANCE = 10


    STOP_BUTTON_PIN = 15



