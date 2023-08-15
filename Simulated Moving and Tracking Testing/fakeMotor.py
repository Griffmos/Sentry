from time import sleep
import threading
from threading import Event

delay:float = 1

class fakeMotor:

    

    def __init__ (self):
        self.currPos=0
        self.interruption:Event = Event()

    def move(self, dist:int):
        x:int =0

        

        while (x<abs(dist)):

            if (dist>=0):
                self.currPos+= 1
            else:
                self.currPos-=1

            sleep(delay)

            x+=1

            


            print(self.currPos)

            if (self.interruption.is_set()):
                self.interruption=Event()
                break
        

    def interrupt(self):
        self.interruption.set()

    def runMotor(self,dist:int):
        runningMotor=threading.Thread(target=self.move, args=[dist])

        runningMotor.start()




  
