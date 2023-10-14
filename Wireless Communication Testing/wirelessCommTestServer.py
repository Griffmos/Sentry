#https://wiki.python.org/moin/TcpCommunication
#https://stackoverflow.com/questions/24423162/how-to-send-an-array-over-a-socket-in-python
#https://www.pythonclear.com/errors/connectionrefusederror-errno-111-connection-refused/#:~:text=The%20ConnectionRefusedError%20errno%20111%20connection%20refused%20is%20generated%20when%20the,that%20needed%20to%20be%20connected.

import socket
import time
from threading import Timer
import pickle


#server


s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',2500))
s.listen(1)
print("server runnig")
print(s.getsockname())

# def background_controller():
#     message = 'Hello client'
#     print(message)
#     connection.send(bytes(message, "utf-8"))
#     Timer(5, background_controller).start()

connection,address = s.accept()
print(f"Connection from {address} worked!")

count =0
while True:

    data = connection.recv(4096)

    # print(pickle.loads(data))

    dataString = data.decode("utf-8")

    print(dataString)

    count+=1
    print(count)


    #connection.send(data)

    if not data: break

    #background_controller()


#client

# s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(("raspberrypi", 5000))

# while True:
#     print(s.recv(1024).decode("utf-8"))
