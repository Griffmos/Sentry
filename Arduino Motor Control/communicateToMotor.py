import serial

from time import sleep

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=0.1) #port = '/dev/ttyACM0' for pi

def sendNum(x:float):
    arduino.write(bytes(x, 'utf-8'))
    arduino.write('\n'.encode())


sleep(2)

arduino.write('r'.encode())

while True:
    num = input("enter a delay: ")

    sendNum(num)
