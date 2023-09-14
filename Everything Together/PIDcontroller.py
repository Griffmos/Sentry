import constants

class PIDcontroller:
    def __init__(self, maxSpeed, minSpeed, errTol, kP):

        self.maxSpeed = maxSpeed
        self.minSpeed = minSpeed
        
        self.errorTolerance = errTol

        self.kP = kP

    
    def calculate(self, currTarget):

        targetPoint = currTarget[0]
        error = (constants.SCREEN_WIDTH/2)-targetPoint[0]

        if (abs(error)<self.errorTolerance):
            return 0

        P = self.kP*error

        return P