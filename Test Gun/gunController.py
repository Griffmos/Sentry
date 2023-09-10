import RPi.GPIO as GPIO
from time import sleep


TRIGGER_PIN = 32
REV_PIN = 36

class Nemesis: 

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setup(TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(REV_PIN, GPIO.OUT)

        GPIO.output(TRIGGER_PIN, GPIO.HIGH)
        GPIO.output(REV_PIN, GPIO.HIGH)

    
    def rev(self):
        GPIO.output(REV_PIN, GPIO.LOW)
    
    def unrev(self):
        GPIO.output(REV_PIN, GPIO.HIGH)

    def shoot(self):
        GPIO.output(TRIGGER_PIN, GPIO.LOW)
    
    def unshoot(self):
        GPIO.output(TRIGGER_PIN, GPIO.HIGH)

    def off(self):
        GPIO.output(TRIGGER_PIN, GPIO.HIGH)

        sleep(1)
        
        GPIO.output(REV_PIN, GPIO.HIGH)
        
        GPIO.cleanup()

        

        
