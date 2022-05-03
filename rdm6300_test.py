import serial
import time

ser = serial.Serial('/dev/serial0')

print(ser)

print('TODO: find and use the start and stop characters')
print('TODO: keep the raw reading/analysis code as well, with isascii or whatever')

# i hope this is emptying any buffer in serial:
ser.read_all()

mybytes = bytes()
while True:
    b = ser.read()
    t = time.time_ns()
    print('SOMETHING HAPPENED')
    rest=[]
    rest.clear()
    for i in range(7):
        time.sleep(0.1)
        rest.append( ser.read_all() )
    print('rest sizes:', [len(r) for r in rest])
    mybytes = b
    for r in rest:
        mybytes+=r
    print(mybytes.hex())
    print('    ',mybytes.decode())
    print('    ',str(mybytes.decode()))


