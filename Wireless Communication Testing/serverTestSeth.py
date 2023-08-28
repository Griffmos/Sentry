#https://wiki.python.org/moin/TcpCommunication
#https://stackoverflow.com/questions/24423162/how-to-send-an-array-over-a-socket-in-python
#https://www.pythonclear.com/errors/connectionrefusederror-errno-111-connection-refused/#:~:text=The%20ConnectionRefusedError%20errno%20111%20connection%20refused%20is%20generated%20when%20the,that%20needed%20to%20be%20connected.


import socket
import time
from threading import Timer
import pickle


#server

def startServer():

    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',5233))
    s.listen(1)
    print("server runnig")
    print(s.getsockname())


    connection,address = s.accept()
    print(f"Connection from {address} worked!")
    
    count =0
    while True:
        dataLen=0
        data=None
        while(dataLen<921600):
            try:
                currData = connection.recv(4096)
            except:
                print("error recv, restaring")
                return -1
            

            # print(pickle.loads(data))

            if not currData: return -1

            if (data is None):
                data=currData
            else:
                data+=currData


            dataLen+=len(currData)
            # nums:list=[]

            
            # for i in range(0, len(data), 2): #must be 1d array
            #     byte1 = data[i]
            #     byte2 = data[i+1]
            #     nums.append(byte1 + (byte2*256))

            # print(data)

            # print(nums)
            print(len(data))
            count+=1
            print(count)

            
        print(f"got data of size {len(data)}")
        try:
            connection.send(bytes('got it','utf-8'))
        except:
            print("error send, restaring")
            return -1


def main():
    while True:
        startServer()


main()

