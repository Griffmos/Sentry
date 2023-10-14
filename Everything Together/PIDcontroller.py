import constants

class PIDcontroller:
    def __init__(self, maxSpeed, minSpeed, errTol, kP, kD):

        self.maxSpeed = maxSpeed
        self.minSpeed = minSpeed
        
        self.errorTolerance = errTol

        self.kP = kP
        self.kD = kD

        self.lastError=-1
        self.lastDeltaError=-1

    
    def calculate(self, currTarget):

        targetPoint = currTarget[0]
        error = (constants.SCREEN_WIDTH/2)-targetPoint[0]

        if (abs(error)<self.errorTolerance):
            return 0

        P=self.calcP(error)

        D=self.calcD(error)
        


        self.lastError=error
        
        PD = P+D
        
        print(f"P+D: {PD}")
        
        direction = 1 if PD>0 else -1
        
        PD = abs(PD)
        
        if (PD<self.minSpeed):
                return direction*self.minSpeed
        if (PD>self.maxSpeed):
                return direction*self.maxSpeed
        return direction*PD
        
    
    def calcP(self, error):
        return self.kP * error
    
    def calcD(self, error):
        if (self.lastError==-1):
	        return 0
        currDeltaError=error-self.lastError
        kCoeff=self.kD * (currDeltaError-self.lastDeltaError) if (self.lastDeltaError!=-1) else 0
        self.lastDeltaError=currDeltaError
        return kCoeff
