#https://wiki.python.org/moin/TcpCommunication
#https://stackoverflow.com/questions/24423162/how-to-send-an-array-over-a-socket-in-python
#https://www.pythonclear.com/errors/connectionrefusederror-errno-111-connection-refused/#:~:text=The%20ConnectionRefusedError%20errno%20111%20connection%20refused%20is%20generated%20when%20the,that%20needed%20to%20be%20connected.


import socket
import time
from threading import Timer
import pickle



#server

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',5000))
s.listen(5)
print("server runnig")
print(s.getsockname())



connection,address = s.accept()
print(f"Connection from {address} worked!")

while True:
    data=None
    while (data ==None):
        data = connection.recv(4096)
    while (len(data)<4):
        data+=connection.recv(4096)

    pickleData = pickle.loads(data)
    print(data)

    if not data: break
    connection.send(data)
connection.close()

    #background_controller()
