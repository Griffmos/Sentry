import constants

class PIDcontroller:
    def __init__(self, maxSpeed, minSpeed, errTol, kP, kD):

        self.maxSpeed = maxSpeed
        self.minSpeed = minSpeed
        
        self.errorTolerance = errTol

        self.kP = kP
        self.kD = kD

        self.lastError=0

    
    def calculate(self, currTarget):

        targetPoint = currTarget[0]
        error = (constants.SCREEN_WIDTH/2)-targetPoint[0]

        if (abs(error)<self.errorTolerance):
            return 0

        P=self.calcP(error)

        D=self.calcD(error, self.lastError)
        


        lastError=error
        return min(P+D,self.maxSpeed)
    
    def calcP(self, error):
        return self.kP * error
    
    def calcD(self, error, lastError):
        return self.kD * (error-lastError)