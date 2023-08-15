from time import sleep
delay:float = 0.2

class fakeMotor:
    

    def __init__ (self):
        self.currPos=0

    def move(self, dist:int):
        for x in range(dist):
            self.currPos+= 1 if dist>=0 else -1
            sleep(delay)
