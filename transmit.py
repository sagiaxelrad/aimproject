import serial

ser = serial.Serial('COM3', baudrate=115200, timeout=1)

ser.write(b'hello com')
response = ser.readline()
print(response.decode())

ser.close()
