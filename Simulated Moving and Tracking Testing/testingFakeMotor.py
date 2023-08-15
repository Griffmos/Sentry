from time import sleep
import fakeMotor

    


if (__name__=='__main__'):
    motor = fakeMotor.fakeMotor()

    print("running motor")
    motor.runMotor(10)
    print("just after runMotor")
    
    sleep(5)

    print("interrupt time!")

    motor.interrupt()



    motor.runMotor(-5)




