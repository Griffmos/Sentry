import pandas as pd
import matplotlib.pyplot as plt
import constants
from itertools import count
from matplotlib.animation import FuncAnimation
import time
from threading import Thread
import random

import pylab as plt

class graph:

    def __init__(self):

        
        self.x = []
        self.y = []
        self.index = count()


        #plt.axis([0,50,-200,200])
        plt.ion()

        plt.show(block=False)




    
    def updateGraph(self):

        plt.plot(self.x, self.y)
       
        plt.draw()
        plt.pause(0.001)

    
        


    
    def putError(self, currTarget):
        if currTarget is not None and len(currTarget)>0:
            err = self.findError(currTarget)            
            self.x.append(next(self.index))
            self.y.append(err)

            self.updateGraph()

    def findError(self, currTarget):
        correctedTarget = currTarget[0]+constants.controller.OFFSET
        error = (constants.SCREEN_WIDTH/2)-correctedTarget
        return error



    def reset(self):
        self.x=[]
        self.y=[]
        plt.cla()