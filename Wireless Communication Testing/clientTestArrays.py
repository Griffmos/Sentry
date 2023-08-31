import socket
import struct         
#import cv2                
from time import sleep
import numpy


#while amtBytes<maxSize append null/blank bits
def findNumDimensions(arr, dimensions:int=0):
    print(type(arr))
    if (not (type(arr) is numpy.ndarray) or (dimensions==3)):
        return dimensions
    else:
        return findNumDimensions(arr[0], dimensions=dimensions+1)

#bytesPerInt is either 1 or 2
def sendIntArr(arr:numpy.ndarray, s:socket.socket, bytesPerInt, maxByteSize=4):

    if (type(arr) is list):
        arr = numpy.array(arr)

    dimensions=findNumDimensions(arr)
    dimensionsBytes=struct.pack('>B',dimensions)
    print(dimensionsBytes)
    print(dimensions)



    
    byteArr=None
    dataFormat = ('>B' if bytesPerInt==1 else '>H')
    for x in arr:
        if (dimensions>1):
            for y in x:
                if(dimensions>2):
                    for z in y:
                        currByte=struct.pack(dataFormat, z)
                        if byteArr is None:
                            byteArr=currByte
                        else:
                            byteArr+=currByte
        
                else:
                    currByte=struct.pack(dataFormat, y)
                    if byteArr is None:
                        byteArr=currByte
                    else:
                        byteArr+=currByte
                   
        else:
            currByte=struct.pack(dataFormat, x)
            if byteArr is None:
                byteArr=currByte
            else:
                byteArr+=currByte
          
    #print(byteArr)


    amtBytes=struct.pack('>I',len(byteArr))
    print(amtBytes)

    bytesPerInt=struct.pack('>B',bytesPerInt)
    print(bytesPerInt)


    

    infoBytes=amtBytes+bytesPerInt+dimensionsBytes

    print(infoBytes)
    # infoBytes.append(amtBytes)
    # infoBytes.append(bytesPerInt)
    # infoBytes.append(dimensions)

    currDimension=arr
    for i in range(dimensions):
        infoBytes+=(struct.pack('>H',len(currDimension)))
        currDimension=currDimension[0]
    
    print(infoBytes)

    sendData=infoBytes+byteArr

    #print(sendData)

    print("sending")
    print(len(sendData))
    #print(byteArr)

    s.send(sendData)








    


def main():


    #cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    #arr=numpy.array([1,2,3,1000])
    #arr=[[1,2],[2,3],[3,4],[999,1000]]
    arr=[[[1,2,3],[4,5,6],[7,8,9]],[[1000,2000,3000],[4000,5000,6000],[7000,8000,9000]]]




    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    s.connect(('192.168.1.96',8888))
    print("connected")

    sendIntArr(arr,s,2)


    #ret, frame =cap.read()

    #print(frame)
    #sendIntArr(frame,s,1)

    #sleep(20)



main()


