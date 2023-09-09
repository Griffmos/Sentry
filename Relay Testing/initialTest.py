import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

GPIO.setup(32,GPIO.OUT)
GPIO.output(32, GPIO.HIGH)


while True:
	
	GPIO.output(32,GPIO.HIGH)
	sleep(1)
	GPIO.output(32,GPIO.LOW)
	sleep(1)


GPIO.cleanup();
