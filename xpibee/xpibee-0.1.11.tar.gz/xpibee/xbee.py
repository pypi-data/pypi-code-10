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
    cmd = ''.join(b for b in arr)

    return cmd


def send_transmit_request(address, data, port='/dev/ttyUSB0', baudrate=9600, timeout=3.0):
    frame = create_frame(address, data)
    ba = bytearray.fromhex(frame)
    ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
    fcntl.flock(ser.fileno(), fcntl.LOCK_EX)
    ser.write(ba)
    return ba, frame


def escape(msg):
    escaped = bytearray()
    reserved = bytearray(b"\x7E\x7D\x11\x13")

    escaped.append(msg[0])
    for m in msg[1:]:
        if m in reserved:
            escaped.append(0x7D)
            escaped.append(m ^ 0x20)
        else:
            escaped.append(m)

    return escaped


def send_transmit_request_2(msg, addr=0xFFFF, options=0x01, frameid=0x00):
    msg = msg.encode('utf-8')
    if not msg:
        return 0

    hexs = '7E 00 {:02X} 01 {:02X} {:02X} {:02X} {:02X}'.format(
        len(msg) + 5,           # LSB (length)
        frameid,
        (addr & 0xFF00) >> 8,   # Destination address high byte
         addr & 0xFF,            # Destination address low byte
         options)

    frame = bytearray.fromhex(hexs)
    #  Append message content
    frame.extend(msg)

    # Calculate checksum byte
    frame.append(0xFF - (sum(frame[3:]) & 0xFF))

    # Escape any bytes containing reserved characters
    frame = escape(frame)

    return frame
