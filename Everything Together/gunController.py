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

        self.shooting=False
        self.revving=False

    
    def rev(self):
        GPIO.output(REV_PIN, GPIO.LOW)
        self.revving=True
    
    def unrev(self):
        if (self.shooting):
            self.off()
        else:
            GPIO.output(REV_PIN, GPIO.HIGH)
            self.revving=False

    def shoot(self):
        if (not self.revving):
            self.rev()
            sleep(1)
        
            
        GPIO.output(TRIGGER_PIN, GPIO.LOW)

        self.shooting=True
    
    def unshoot(self):
        GPIO.output(TRIGGER_PIN, GPIO.HIGH)
        self.shooting=False

    def off(self):
        GPIO.output(TRIGGER_PIN, GPIO.HIGH)

        sleep(1)
        self.shooting=False
        
        GPIO.output(REV_PIN, GPIO.HIGH)
        self.revving=False
        
    def shutdown(self):
        self.off()
        GPIO.cleanup()

        

        
