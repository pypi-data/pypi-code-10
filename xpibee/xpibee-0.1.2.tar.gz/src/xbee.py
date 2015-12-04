import fcntl
import serial


def calculate_checksum(frameData):
    print 'calculating checksum'
    checksum = 0
    for a in frameData:
        checksum += int(a, 16)
    return hex(int('0xFF', 16)-int(str(hex(checksum))[-2:], 16))


def create_frame(address, data):
    print 'creating frame'
    frameDelimiter = "7E"
    frameType = "10"
    frameId = "01"
    destAdd = "FF FE"
    broadcastR = "00"
    options = "00"

    d = ' '.join([frameType, frameId, address, destAdd, broadcastR, options])
    arr = d.split(' ')
    for a in data:
        arr.append(str(a.encode('hex')))

    checksum = calculate_checksum(arr)
    arr = arr[::-1]
    arr.append(str(hex(len(arr))).replace('0x', ''))
    arr.append("00")
    arr.append(frameDelimiter)
    arr = arr[::-1]
    arr.append(str(checksum).replace('0x', ''))
    print(arr)
    cmd = ''.join(b for b in arr)

    return cmd


def send(address, data):
    frame = create_frame(address, data)
    print bytearray.fromhex(frame)
    ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=3.0)
    #ser = serial.Serial('/dev/tty.usbserial-DA00T246', baudrate=9600, timeout=3.0)
    fcntl.flock(ser.fileno(), fcntl.LOCK_EX)
    ser.write(bytearray.fromhex(frame))