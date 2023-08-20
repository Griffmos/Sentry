import stepperMotor
from time import sleep

motor = stepperMotor.stepperMotor(PULSE PIN, DIR PIN, 1, -1, -1, -1)

motor.step(4)

motor.turnDegrees(180)

sleep(1)

motor.turnDegrees(-180)