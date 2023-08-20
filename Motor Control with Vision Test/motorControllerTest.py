import RPiMotorController
from time import sleep

motor = RPiMotorController.stepperMotor(port='COM3')


sleep(2)
motor.setDelay(delay=100)

sleep(2)
motor.setDelay(delay=-100)

sleep(2)

motor.setDelay(0)

sleep(5)
motor.setSpeed(6.28)
