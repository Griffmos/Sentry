import RPiGPIO as GPIO
from time import sleep

#constants
degreesPerStep: float = 1.8
CW: int = 1 #clockwise
CCW: int =0 #counterclockwise


class stepperMotor:

    def __init__(self, pulsePin:int, dirPin:int, microStep: int, accel:int, deccel:int, maxSpeed:int):
        self.pulsePin = pulsePin
        self.dirPin = dirPin
        self.accel = accel
        self.deccel= deccel
        self.microStep = microStep
        self.maxSpeed = maxSpeed

        self.degreesPerStep = degreesPerStep/microStep

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(dirPin, GPIO.OUT)

        GPIO.setup(pulsePin, GPIO.OUT)
    
    def degressToSteps(self, degrees):
        return int(degrees/degreesPerStep)
    
    def step(self, steps:int):
        #negative = ccw, positive =cw
        if (steps<0):
            GPIO.output(self.dirPin, CCW)
            steps = abs(steps)
        else:
            GPIO.output(self.dirPin, CW)
        for s in range(steps):
                #hard coded speed
                GPIO.output(self.pulsePin,GPIO.HIGH)
                sleep(0.1)
                GPIO.output(self.pulsePin, GPIO.LOW)
                sleep(0.1)


    def turnDegrees(self, degrees):
        #negative = ccw, positive =cw
        self.step(self.degreesToSteps(degrees))
        
