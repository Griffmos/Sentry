import socket
import numpy
import cv2

def recvIntArr(s:socket.socket,maxByteSize:int=4,maxDimensions=3):
    data:bytes=None
    amtBytes:int=-1
    arrDimensions=[]
    numDimensions:int
    bytesPerInt:-1

    arr=None


    #getting base info
    while amtBytes ==-1:
        if (data is None):
            data=s.recv(50)
        else:
            data+=s.recv(50)
        

        #parse order where (x) is x bytes: amtBytes(6), bytesPerInt(1), dimensions(1),shape(3)

        #maxSize bytes for amtBytes + 1 byte for bytesPerInt + 1 byte for dimensions + maxDimesions*2 bytes for a 16 bit max size in each direction 
        infoBytesParsed:int=0
        if (len(data)>=(maxByteSize-1)+1+1+maxDimensions*2):
            amtBytes=int.from_bytes(data[0:maxByteSize], "big")
            print(f'amtBytes: {amtBytes}')
            infoBytesParsed+=maxByteSize

            bytesPerInt=data[maxByteSize]
            print(f'bytesPerInt: {bytesPerInt}')
            infoBytesParsed+=1

            numDimensions=int(data[maxByteSize+1])
            print(f'numDimensions: {numDimensions}')
            infoBytesParsed+=1

            for i in range(0,numDimensions*2, 2):
                #maxSize+2 to account for the data parsing above, i+2 to accound for each appenened int is a 2 byte int
                arrDimensions.append(int.from_bytes(data[maxByteSize+2+i:maxByteSize+2+i+2],"big"))
                infoBytesParsed+=1

            print(f'arrDimensions: {arrDimensions}')

            data=data[infoBytesParsed+numDimensions:len(data)]
            
    bP:int=0 #bytesParsed

    incrementors=numpy.zeros(shape=numDimensions,dtype=numpy.int16)


    #limited to hold either 8 bit or 16 bit ints, and 3d array
    arr=numpy.empty(shape=arrDimensions,dtype=(numpy.uint8 if (bytesPerInt==1) else numpy.uint16))

    while bP<amtBytes:
        data+=s.recv(amtBytes-bP)
        #print(data)

        #parsing each data

        thisRecvBP=0
        
        while(thisRecvBP<len(data) and thisRecvBP+bP<amtBytes):


            bPBefore=thisRecvBP

            #getting byte to write

            byte=None

            if (bytesPerInt==1):
                byte=data[thisRecvBP]
            else:
                byte=int.from_bytes(data[thisRecvBP:thisRecvBP+2],"big")

            #print(byte)
            
            #getting to the right dimension
            if len(arrDimensions)==1:
                arr[incrementors[0]]=byte
            elif len(arrDimensions)==2:
                arr[incrementors[0]][incrementors[1]]=byte
            elif len(arrDimensions)==3:     
                arr[incrementors[0]][incrementors[1]][incrementors[2]]=byte
                
            
            thisRecvBP+=bytesPerInt

            #incrementing whatever the least significant incrementer is
            incrementors[len(incrementors)-1]+=1

            for i in range(len(incrementors)):
                #if the incrementor is = the dimension, it goes to zero and the next most significant increases
                
                if (incrementors[len(incrementors)-1-i]==arrDimensions[len(incrementors)-1-i]-1):
                    incrementors[len(incrementors)-1-i]=0
                    incrementors[len(incrementors)-1-i-1]+=1 #this MIGHT error out if this byte is the last possible value and it tries to increment the next most significant incrementor which doesn't exists
                else: #if this one didn't increment, then next one def won't
                    break


            #indicates couldn't parse anything since there is a hanging byte for the next data recieve
            if (bPBefore==thisRecvBP):
                data=data[thisRecvBP:amtBytes] #should leave remainder
                break
                
        print(thisRecvBP)
        bP+=thisRecvBP

    print(bP)


    return arr








def main():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',8888))
    s.listen(1)
    print("server runnig")
    print(s.getsockname())

    conn,address = s.accept()
    print(f"Connection from {address} worked!")

    
    count=0

    print(recvIntArr(conn))
    while True:
        arr=recvIntArr(conn)
        print(arr)
        cv2.imwrite(f'recievedFrame{count}.jpg',arr)
        count+=1



main()