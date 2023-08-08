import numpy

class rollingAvg:

    # numVals:int=0

    # vals:list=[]

    # avg:int=0

    def __init__(self, nV:int):
        self.numVals=nV
        self.vals=numpy.zeros(nV)
        self.avg:0

    def addVal(self, val:int):
        tempAvg=0
        for i in range(0,self.numVals-1):
            currV:int=self.vals[i]
            tempAvg+=currV
            self.vals[i+1]=currV
        self.vals[0]=val
        tempAvg+=val

        self.avg=int(tempAvg/self.numVals)

            