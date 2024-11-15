import serial, time, math
from Adafruit_IO import Client
aio = Client ('antaldf', '<secret>')
 
goodLow=0.0
goodHigh=9.0
moderateLow=9.1
moderateHigh=35.4
sensitiveGroupsLow=35.5
sensitiveGroupsHigh=55.4
unhealthyLow=55.5
unhealthyHigh=125.4
veryLow=125.5
veryHigh=225.4
hazardousLow=225.5
ser = serial.Serial('/dev/ttyUSB0')
 
while True:
    data = []
    for index in range(0,10):
        datum = ser.read()
        data.append(datum)
     
    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
    if pmtwofive <= goodHigh:
      aqitwofive = math.floor(( 50 / 9 ) * pmtwofive)
    elif pmtwofive <= moderateHigh:
      aqitwofive = math.floor(( ( 100 - 51 ) / ( 35.4 - 9.1 ) ) * (pmtwofive - 9.1) + 51)
    elif pmtwofive <= sensitiveGroupsHigh:
      aqitwofive = math.floor(( ( 150 - 101 ) / ( 55.4 - 35.5 ) ) * (pmtwofive - 35.5) + 101)
    elif pmtwofive <= unhealthyHigh:
      aqitwofive = math.floor(( ( 200 - 151 ) / ( 125.4 - 55.5 ) ) * (pmtwofive - 55.5) + 151)
    elif pmtwofive <= veryHigh:
      aqitwofive = math.floor(( ( 300 - 201 ) / ( 225.4 - 125.5 ) ) * (pmtwofive - 125.5) + 201)
    else:
      aqitwofive = math.floor(( ( 500 - 301 ) / ( 225.5 - 300 ) ) * (pmtwofive - 225.5) + 301)

    aio.send('silverdaletwofive', pmtwofive)
    aio.send('aqi25', aqitwofive)
    print( pmtwofive)
    print( aqitwofive)
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
    aio.send('silverdaleten', pmten)
    time.sleep(10)
