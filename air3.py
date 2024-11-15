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

def aqi(current, aqihi, aqilow, hi, low):
  return math.floor(( ( aqihi - aqilow ) / ( hi - low ) ) * (current - low) + aqilow)

while True:
    data = []
    for index in range(0,10):
        datum = ser.read()
        data.append(datum)
     
    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
    if pmtwofive <= goodHigh:
      aqitwofive = aqi(pmtwofive, 50, 0, 9.0, 0)
    elif pmtwofive <= moderateHigh:
      aqitwofive = aqi(pmtwofive, 100, 51, 35.4, 9.1)
    elif pmtwofive <= sensitiveGroupsHigh:
      aqitwofive = aqi(pmtwofive, 150, 101, 55.4, 35.5)
    elif pmtwofive <= unhealthyHigh:
      aqitwofive = aqi(pmtwofive, 200, 151, 125.4, 55.5)
    elif pmtwofive <= veryHigh:
      aqitwofive = aqi(pmtwofive, 300, 201, 225.4, 125.5)
    else:
      aqitwofive = aqi(pmtwofive, 500, 301, 500, 225.5)

    aio.send('silverdaletwofive', pmtwofive)
    aio.send('aqi25', aqitwofive)
#    print( pmtwofive)
    print( aqitwofive)
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
    aio.send('silverdaleten', pmten)
    time.sleep(10)

