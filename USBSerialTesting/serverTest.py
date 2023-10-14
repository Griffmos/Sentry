import serial

ser = serial.Serial(port='COM1', baudrate=9600)

while True:
    ser.write("g".encode())