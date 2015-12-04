import RPi.GPIO as GPIO


SET_OUTPUT = 'set_output'
SET_INPUT = 'set_input'
WRITE = 'write'
READ = 'read'
PIN = 'pin'
ACTION = 'action'
VALUE = 'value'
SUCCESS = 'ok '


def set_output(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)


def set_input(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def output(pin, value):
    GPIO.output(pin, value == 1)


def read(pin):
    return GPIO.input(pin)


def process_gpio_request(options):
    print options
    action = options[ACTION]
    pin = int(options[PIN])

    if action == WRITE:
        output(pin, int(options[VALUE]))
        return SUCCESS + WRITE
    elif action == READ:
        return read(pin)
    elif action == SET_INPUT:
        set_input(pin)
        return SUCCESS + SET_INPUT
    elif action == SET_OUTPUT:
        set_output(pin)
        return SUCCESS + SET_OUTPUT