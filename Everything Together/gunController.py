import RPi.GPIO as GPIO
from time import sleep
from threading import Thread


TRIGGER_PIN = 32
REV_PIN = 36

class Nemesis: 

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setup(TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(REV_PIN, GPIO.OUT)

        GPIO.output(TRIGGER_PIN, GPIO.HIGH)
        GPIO.output(REV_PIN, GPIO.HIGH)

        self.reqShooting = False
        self.reqRevving = False

        self.isShooting=False
        self.isRevving=False

        self.turnOff=False

        self.schedulerThread = Thread(self.scheduler)
        self.schedulerThread.start()


    def reqShoot(self, state:bool):
        self.reqShooting=state

    def reqRev(self, state:bool):
        self.reqRevving=state

    def scheduler(self):
        while not self.turnOff:
            if (self.reqRevving and not self.isRevving):
                self.rev()
                self.isRevving = True
            if (not self.reqRevving and self.isRevving):
                if (self.isShooting):
                    self.unshoot()
                    self.isShooting=False
                    self.reqShooting=False
                self.unrev()
                self.isRevving=False

            if (self.reqShooting and not self.isShooting):
                if (not self.isRevving):
                    self.rev()
                    self.isRevving=True
                    self.reqRevving=True
                self.shoot()
                self.isShooting=True
            if (not self.reqShooting and self.isShooting):
                self.unshoot()
                self.isShooting=False
    
    def rev(self):
        GPIO.output(REV_PIN, GPIO.LOW)
        sleep(1)
    
    def unrev(self):
        GPIO.output(REV_PIN, GPIO.HIGH)

    def shoot(self):
        GPIO.output(TRIGGER_PIN, GPIO.LOW)
    
    def unshoot(self):
        GPIO.output(TRIGGER_PIN, GPIO.HIGH)
        sleep(0.2)

    # def off(self):
    #     GPIO.output(TRIGGER_PIN, GPIO.HIGH)

    #     sleep(1)
    #     self.isShooting=False
        
    #     GPIO.output(REV_PIN, GPIO.HIGH)
    #     self.isRevving=False
        
    def shutdown(self):
        self.turnOff=True
        GPIO.cleanup()

        

        
