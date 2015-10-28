#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""
import argparse
import logging
import numpy as np
import shutil

usage_line = ' press <enter> to quit, +<enter> or -<enter> to change scaling '

try:
    columns, _ = shutil.get_terminal_size()
except AttributeError:
    columns = 80

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-l', '--list-devices', action='store_true',
                    help='list audio devices and exit')
parser.add_argument('-b', '--block-duration', type=float,
                    metavar='DURATION', default=50,
                    help='block size (default %(default)s milliseconds)')
parser.add_argument('-c', '--columns', type=int, default=columns,
                    help='width of spectrogram')
parser.add_argument('-d', '--device', type=int, help='input device ID')
parser.add_argument('-g', '--gain', type=float, default=10,
                    help='initial gain factor (default %(default)s)')
parser.add_argument('-r', '--range', type=float, nargs=2,
                    metavar=('LOW', 'HIGH'), default=[100, 2000],
                    help='frequency range (default %(default)s Hz)')
args = parser.parse_args()

low, high = args.range
if high <= low:
    parser.error("HIGH must be greater than LOW")

# Create a nice output gradient using ANSI escape sequences.
# Stolen from https://gist.github.com/maurisvh/df919538bcef391bc89f
colors = 30, 34, 35, 91, 93, 97
chars = ' :%#\t#%:'
gradient = []
for bg, fg in zip(colors, colors[1:]):
    for char in chars:
        if char == '\t':
            bg, fg = fg, bg
        else:
            gradient.append('\x1b[{};{}m{}'.format(fg, bg + 10, char))

try:
    import sounddevice as sd

    if args.list_devices:
        sd.print_devices()
        parser.exit()

    if args.device is None:
        args.device = sd.default.device['input']
    samplerate = sd.query_devices(args.device)['default_samplerate']

    delta_f = (high - low) / (args.columns - 1)
    fftsize = np.ceil(samplerate / delta_f).astype(int)
    low_bin = np.floor(low / delta_f)

    statuses = sd.CallbackFlags()

    def callback(indata, frames, time, status):
        global statuses
        statuses |= status
        if any(indata):
            magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
            magnitude *= args.gain / fftsize
            line = (gradient[int(np.clip(x, 0, 1) * (len(gradient) - 1))]
                    for x in magnitude[low_bin:low_bin + args.columns])
            print(*line, sep='', end='\x1b[0m\n', flush=True)
        else:
            print('no input', flush=True)

    with sd.InputStream(device=args.device, channels=1, callback=callback,
                        blocksize=int(samplerate * args.block_duration / 1000),
                        samplerate=samplerate):
        while True:
            response = input()
            if response in ('', 'q', 'Q'):
                break
            for ch in response:
                if ch == '+':
                    args.gain *= 2
                elif ch == '-':
                    args.gain /= 2
                else:
                    print('\x1b[31;40m', usage_line.center(args.columns, '#'),
                          '\x1b[0m', sep='')
                    break
    if statuses:
        logging.warning(str(statuses))
except KeyboardInterrupt:
    parser.exit('Interrupted by user')
except Exception as e:
    parser.exit(str(e))
