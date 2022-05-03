import serial

ser = serial.Serial('/dev/serial0')

'''
principles: 
    - try keep in sync with 14-byte frames from module, and read per frame
    - 
'''


def sync():
    ser.read_until(b'\x03')


sync()

while True:
    frame = ser.read(14)
    if not frame[0] == 2:
        raise Exception('no 2 at index 0; mmm thought that sync would have avoided this')
    if not frame[13] == 3:
        raise Exception('no 3 at index 13; mmm thought that sync would have avoided this')
    data=frame[1:13]
    print(data)


