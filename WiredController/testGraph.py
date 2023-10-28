from time import sleep
import random
import graphingUtility
from threading import Thread


graph = graphingUtility.graph()

#graph.updateGraph()

#graph.runGraph()

for x in range(25):

    print("running")


    err=random.randint(-160,160)

    graph.putError([err,0])


    sleep(0.2)

graph.reset()

sleep(5)

for x in range(25):

    print("running")


    err=random.randint(-160,160)

    graph.putError([err,0])


    sleep(0.2)
