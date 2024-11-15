import serial, time
from Adafruit_IO import Client
aio = Client ('antaldf', '<secret>')
 
ser = serial.Serial('/dev/ttyUSB0')
 
while True:
    data = []
    for index in range(0,10):
        datum = ser.read()
        data.append(datum)
     
    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    aio.send('silverdaletwofive', pmtwofive)
    print( pmtwofive)
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
    aio.send('silverdaleten', pmten)
    time.sleep(10)
