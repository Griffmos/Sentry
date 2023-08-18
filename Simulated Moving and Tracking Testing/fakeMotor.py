from time import sleep
import threading
from threading import Event

delay:float = 0.02

distMargin:int = 20

class fakeMotor:

    

    def __init__ (self):
        self.currPos=0
        self.interruption:Event = Event()

    def moveTo(self, dest:int):

        self.interrupt()

        while not(dest-distMargin<self.currPos<dest+distMargin):
            if (self.currPos<dest):
                self.currPos+=1

            elif (self.currPos>dest):
                self.currPos-=1

            sleep(delay)

            print(self.currPos)

            if (self.interruption.is_set()):
                #self.interruption=Event()
                break



    def move(self, dist:int):
        x:int =0

        self.interrupt()


        incDir = 1 if dist>=0 else -1

        dist=abs(dist)


        while (x<dist):

            self.currPos+=incDir

            

            sleep(delay)

            x+=1

            


            print(self.currPos)

            if (self.interruption.is_set()):
                #self.interruption=Event()
                break
        

    def interrupt(self):
        self.interruption.set()
        sleep(delay+0.01)
        self.interruption=Event()

    def runMotor(self,func, args:int):
        runningMotor=threading.Thread(target=func, args=[args])

        runningMotor.start()





  
