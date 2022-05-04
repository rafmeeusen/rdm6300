import serial
import time

'''
background: 
    - rdm6300 is a bit annoying for software: while same card is in field, it spits out the card ID continuously
    - time between two "frames" is about 0.0662 seconds
    - frame format = start byte + ID + CRC + stop byte (1 + 10 + 2 + 1 bytes)
    - what we want: only 1x trigger when card is entering the field

principles: 
    - on serial port: 
        -- try keep in sync with 14-byte frames from module
        -- read per frame
    - detecting new enter/exit field:
        -- read out serial port continuously, and put timestamp on each frame
        -- take into account both data and timestamps to decide if new frame is also a new badge reading event 
'''

# globals -- ugly, I know
ser = serial.Serial('/dev/serial0')

'''
helper class; keep track of data and time stamps
    data is new if 
        data is DIFFERENT
        OR 
        timestamp delta LONG ENOUGH
    todo: did not cover case where wasnew would be called before adding any data...
'''
class RfidDataTimeKeeper:
    def __init__(self):
        self.prevdata = None
        self.prevtime = None
        self.newtime = None
        self.newdata = None
        self.EXPECTED_DELTA_TIME=0.0662
    def adddata(self, data, time):
        # shift previous new to previous
        self.prevdata = self.newdata
        self.prevtime = self.newtime
        # add new input
        self.newdata = data
        self.newtime = time
    def wasnew(self):
        if not self.prevtime:
            # first time data always new
            return True
        else:
            # we have at least 2 frames and 2 times
            deltat = self.newtime - self.prevtime
            if deltat > (1.1 * self.EXPECTED_DELTA_TIME):
                return True
            if self.newdata != self.prevdata:
                return True
        return False

# read until end a whatever partial frame that might be in buffer
def sync():
    ser.read_until(b'\x03')

# warning: fun raises exceptions for now
def checkdata(data):
    if not frame[0] == 2:
        raise Exception('no 2 at index 0; mmm thought that sync would have avoided this')
    if not frame[13] == 3:
        raise Exception('no 3 at index 13; mmm thought that sync would have avoided this')
    #todo : crc check
    return True


# init:
sync()
keeper = RfidDataTimeKeeper()
while True:
    frame = ser.read(14)
    ts = time.time()
    if not checkdata(frame):
        continue

    data_crc=frame[1:13]
    data=frame[1:11]

    keeper.adddata(data, ts)
    if keeper.wasnew():
        print(data)
        

