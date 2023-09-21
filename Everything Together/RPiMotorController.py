from time import sleep
import serial;
import numpy
import math
import constants


#constants


#motor constants


#utilities

#POSITIVE is ccw, NEGATIVE is cw


def toDelay(radiansPerSecond):
        if (radiansPerSecond==0):
            return 0
        secsPerRev=(2*constants.Pi)/radiansPerSecond
        secsPerPulse=(secsPerRev/(constants.STEPS_PER_REV*constants.GEAR_RATIO))
        secsPerDelaymS=(secsPerPulse*constants.microsPerSec)*0.5
        
        return int(secsPerDelaymS)
    
def toRadiansPerSecond(delay):
    if (delay==0):
        return 0
        
    secsPerStep = delay/(0.5*constants.microsPerSec)

    secsPerRev = secsPerStep*(constants.STEPS_PER_REV*constants.GEAR_RATIO)

    radsPerSec = 1/(secsPerRev/(2*constants.Pi))

    return radsPerSec


class stepperMotor:

    

    def __init__(self):
        print("inited motor")
        self.arduino = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=0.1) #port = '/dev/ttyACM0' for pi, 'COM3' for computer
        
        self.currSpeed=0
        

        sleep(2)
        self.arduino.write('r'.encode())
        self.arduino.write('\n'.encode())

        sleep(2)
        self.setSpeed(0)


    


    def setSpeed(self, radiansPerSecond:float):
        speedToSet = toDelay(radiansPerSecond) #make this min(MAX_SPEED, toDelay(radiansPerSeond)
        self.setDelay(speedToSet) 
        self.currSpeed=speedToSet
        #print(self.currSpeed)

    def setDelay(self, delay:int):
        delay=delay
        self.arduino.write(bytes(str(delay), encoding='UTF-8'))
        self.arduino.write('\n'.encode())

        self.arduino.read()

        #print(delay)

    def getPos(self):
        self.arduino.write('g'.encode())
        self.arduino.write('\n'.encode())

        return int.from_bytes(self.arduino.read(),"big",signed=True)

    def terminate(self):
         self.arduino.write('q'.encode())
         self.arduino.write('\n'.encode())

    



#depricated (for now)
# class stepperMotor:

#     DEGREES_PER_STEP=0.9

#     MAX_SPEED:float=0 #TBD

#     def __init__(self):
#         self.currSpeed=0

#     def setSpeed(self, radiansPerSecond:float):
#         speedToSet = toDelay(radiansPerSecond) #make this min(MAX_SPEED, toDelay(radiansPerSeond)

#         self.setDelay(speedToSet) 
#         self.currSpeed=speedToSet

#     def setDelay(self, delay:int):
#         self.arduino.write(bytes(delay, 'utf-8'))
#         self.arduino.write('\n'.encode())



# #depricated (for)
# class motorController:

#     def __init__(self, port, numMotors:int, motorNames:list):
#         self.arduino = serial.Serial(port, baudrate=9600, timeout=0.1) #port = '/dev/ttyACM0' for pi
#         self.motors = {}

#         for i in range(numMotors):
#             self.motors[motorNames[i]]= stepperMotor()

#         sleep(2)
#         self.arduino.write('r'.encode())

#     def setSpeed(self, motorName, radiansPerSec):
#         self.motors[motorName].setSpeed(radiansPerSec)

#     def setDelay(self,motorName,delay):
#         self.motors[motorName].setDelay(delay)

# ~ s = stepperMotor()

# ~ print(toDelay(0.285))

# ~ print (toRadiansPerSecond(s.toDelay(0.285)))
    

# ~ stepper:stepperMotor = stepperMotor()

# ~ stepper.setSpeed(0.5)




def main():
     stepper:stepperMotor = stepperMotor()
     while True:
          print(stepper.getPos())
          sleep(0.01)





    



    
