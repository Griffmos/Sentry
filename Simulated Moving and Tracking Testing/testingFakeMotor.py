from time import sleep
import fakeMotor

    


if (__name__=='__main__'):
    motor = fakeMotor.fakeMotor()

    print("running motor")
    motor.runMotor(motor.move, 180)
    print("just after runMotor")
    
    sleep(3)

    print("interrupt time!")




    motor.runMotor(motor.move,-90)




