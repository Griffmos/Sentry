#https://wiki.python.org/moin/TcpCommunication
#https://stackoverflow.com/questions/24423162/how-to-send-an-array-over-a-socket-in-python
#https://www.pythonclear.com/errors/connectionrefusederror-errno-111-connection-refused/#:~:text=The%20ConnectionRefusedError%20errno%20111%20connection%20refused%20is%20generated%20when%20the,that%20needed%20to%20be%20connected.


import socket
import time
from threading import Timer
import pickle
import cv2



#server

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',5000))
s.listen(1)
print("server runnig")
print(s.getsockname())



connection,address = s.accept()
print(f"Connection from {address} worked!")
while True:
    data=[]
    while True:
        packet=s.recv(4096)
        if not packet:break

        data.append(packet)

    data_arr = pickle.loads(b"".join(data))


    cv2.imshow(data_arr)

    connection.send(pickle.dumps([10,1]))


    #background_controller()
