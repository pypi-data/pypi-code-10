import sys

def writeflush(dest, s):
    dest.write(s)
    dest.flush()

def get_headers(line):
    """
    Parse Supervisor message headers.
    """

    return dict([x.split(':') for x in line.split()])

def supervisor_events(stdin, stdout, stderr):
    """
    An event stream from Supervisor.
    """

    while True:

        writeflush(stdout, 'READY\n')

        line = stdin.readline()
        headers = get_headers(line)
        payload = stdin.read(int(headers['len']))
        yield payload

        writeflush(stdout, 'RESULT 2\nOK')

def main():
    for payload in supervisor_events(sys.stdin, sys.stdout, sys.stderr):
        writeflush(sys.stderr, payload + '\n')

if __name__ == '__main__':
    main()
