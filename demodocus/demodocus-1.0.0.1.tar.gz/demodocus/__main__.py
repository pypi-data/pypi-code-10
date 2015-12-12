#!/usr/bin/env python
# coding=utf-8

"""
demodocus is Python CLI program to quickly check synchronization maps.

This is the main demodocus script, intended to be run from command line.
"""

from __future__ import absolute_import
from io import open
import argparse
import json
import os
import pyaudio
import re
import subprocess
import sys
import time
import wave

from demodocus.command_line import COMMAND_LINE_PARAMETERS
from demodocus.command_line import DESCRIPTION
from demodocus.command_line import EPILOG
from demodocus.command_line import USAGE
from demodocus.command_line import check_arguments
from demodocus.command_line import set_default_values
from demodocus.utilities import create_temp_file
from demodocus.utilities import delete_file
from demodocus.utilities import print_error
from demodocus.utilities import print_info

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "alberto@albertopettarin.it"
__status__ = "Production"

# pattern to match 00:00:00.000 time strings
HHMMSSMMM_PATTERN = re.compile(r"([0-9]*):([0-9]*):([0-9]*)\.([0-9]*)")

# global variable for pyaudio callback
g_current_frame_index = 0
g_next_stop_frame_index = 0 
g_current_fragment_index = 0
g_current_increment = 1 
g_current_duration = 2.0
g_current_wait = 0.0

def read_syncmap(path):

    def read_json(path):
        with open(path, "r") as file_obj:
            json_obj = json.loads(file_obj.read())
            return json_obj["fragments"]
        return []

    def hhmmssmmm_to_float(string):
        v_length = 0
        match = HHMMSSMMM_PATTERN.search(string)
        if match is not None:
            v_h = int(match.group(1))
            v_m = int(match.group(2))
            v_s = int(match.group(3))
            v_f = float("0." + match.group(4))
            v_length = v_h * 3600 + v_m * 60 + v_s + v_f 
        return v_length

    def string_to_time(string):
        if ":" in string:
            return hhmmssmmm_to_float(string)
        return float(string)

    def read_ssv(path):
        fragments = []
        with open(path, "r") as file_obj:
            for line in file_obj.readlines():
                arr = line.strip().split(" ")
                fragments.append({
                    "begin": string_to_time(arr[0]),
                    "end": string_to_time(arr[1]),
                    "id": arr[2],
                    "lines": [u" ".join(arr[3:])[1:-1]]
                })
        return fragments

    syncmap = None
    try:
        syncmap = read_json(path)
    except ValueError:
        try:
            syncmap = read_ssv(path)
        except:
            print_error("Unable to read the given syncmap file '%s' (wrong format?)" % (path))
            sys.exit(1)
    return syncmap

def convert_audio(orig_path, tmp_path):
    print_info("Converting audio (temporary file: '%s')..." % (tmp_path))
    arguments = [
        "ffmpeg",
        "-i",
        orig_path,
        "-ac",
        "2",
        "-ar",
        "44100",
        "-y",
        "-f",
        "wav",
        tmp_path
    ]
    proc = subprocess.Popen(
        arguments,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    proc.communicate()
    proc.stdout.close()
    proc.stdin.close()
    proc.stderr.close()
    print_info("Converting audio... done")

def main():
    global g_current_increment
    global g_current_duration
    global g_current_wait
    parser = argparse.ArgumentParser(
        usage=USAGE,
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    for param in COMMAND_LINE_PARAMETERS:
        if param["short"] is None:
            parser.add_argument(
                param["long"],
                help=param["help"],
                action=param["action"],
                default=argparse.SUPPRESS
            )
        else:
            parser.add_argument(
                param["short"],
                param["long"],
                help=param["help"],
                action=param["action"],
                default=argparse.SUPPRESS
            )
    arguments = parser.parse_args()

    # no arguments: show help and exit
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)

    # print version and exit
    if "version" in arguments:
        print_info("demodocus v%s" % (__version__))
        sys.exit(0)

    # check we have all the required arguments
    # if not, it will sys.exit() with some error code
    check_arguments(arguments)

    # set default values
    set_default_values(arguments)

    # check that we have the audio and syncmap files
    audio_file_path = arguments.audio
    syncmap_file_path = arguments.syncmap
    if not os.path.isfile(audio_file_path):
        print_error("Audio file '%s' does not exist" % (audio_file_path))
        sys.exit(1)
    if not os.path.isfile(syncmap_file_path):
        print_error("Syncmap file '%s' does not exist" % (syncmap_file_path))
        sys.exit(1)

    # read syncmap
    syncmap_obj = read_syncmap(syncmap_file_path)
    if (syncmap_obj is None) or (len(syncmap_obj) == 0):
        print_error("Syncmap file '%s' could not be read or it has no fragments" % (syncmap_file_path))
        sys.exit(1)
    max_index = len(syncmap_obj)

    # convert file to .wav
    tmp_handler, tmp_path = create_temp_file(extension=".wav")
    convert_audio(audio_file_path, tmp_path)

    # open wave file
    wave_obj = wave.open(tmp_path, "rb")
    sample_width = wave_obj.getsampwidth()
    channels = wave_obj.getnchannels()
    frame_rate = wave_obj.getframerate()

    # raw_input was renamed to input in Python 3.2
    input_function = input
    try:
        input_function = raw_input
    except NameError:
        pass

    # set global parameters (default or provided by the user)
    g_current_increment = int(arguments.increment)
    g_current_duration = float(arguments.duration)
    g_current_wait = float(arguments.wait)

    # define pyaudio callback
    def callback(in_data, frame_count, time_info, status):
        global g_current_frame_index
        global g_next_stop_frame_index
        global g_current_fragment_index
        global g_current_increment
        global g_current_duration
        global g_current_wait

        if g_current_frame_index >= g_next_stop_frame_index:
            # we played what we had to play
            # so we either move to next fragment
            # or we wait for user input
            if arguments.continuous:
                g_current_fragment_index += g_current_increment
            else:
                print("Press r, q, x, dVAL, iVAL, +VAL, -VAL, or [1 ... %d]:" % (max_index))
                request = input_function()
                if len(request) == 0:
                    g_current_fragment_index += g_current_increment
                elif (request == "x") or (request == "q"):
                    # exit
                    g_current_fragment_index = max_index + 1
                elif request == "r":
                    # do nothing => will repeat current fragment
                    pass
                elif request.startswith("d"):
                    try:
                        g_current_duration = float(request[1:])
                    except:
                        pass
                elif request.startswith("i"):
                    try:
                        g_current_increment = int(request[1:])
                    except:
                        pass
                elif request.startswith("+") or request.startswith("-"):
                    try:
                        g_current_fragment_index += int(request)
                    except:
                        pass
                else:
                    try:
                        g_current_fragment_index = int(request)
                    except:
                        pass
            
            if g_current_fragment_index > max_index:
                # completed, return
                return (None, pyaudio.paComplete)
            
            fragment = syncmap_obj[g_current_fragment_index - 1]
            fragment_position = int(frame_rate * float(fragment["begin"]))
            fragment_duration = int(frame_rate * (float(fragment["end"]) - float(fragment["begin"])))
            fragment_duration = min(fragment_duration, int(frame_rate * g_current_duration))
            
            fragment_text = " ".join(fragment["lines"])
            print("  [%06d] %s\n" % (g_current_fragment_index, fragment_text))
           
            wave_obj.setpos(fragment_position)
            g_current_frame_index = fragment_position
            g_next_stop_frame_index = fragment_position + fragment_duration

        # read data from the current position and return it
        data = wave_obj.readframes(frame_count)
        g_current_frame_index += frame_count
        return (data, pyaudio.paContinue)

    # create object
    pyaudio_obj = pyaudio.PyAudio()
    stream = pyaudio_obj.open(
        format=pyaudio_obj.get_format_from_width(sample_width),
        channels=channels,
        rate=frame_rate,
        output=True,
        stream_callback=callback
    )

    # play stream until it stays active
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)

    # close the stream
    stream.stop_stream()
    stream.close()
    wave_obj.close()
    pyaudio_obj.terminate()

    # remove temp file
    delete_file(tmp_handler, tmp_path)
    print_info("Removed file '%s'" % (tmp_path))

    # return 0
    sys.exit(0)



if __name__ == "__main__":
    main()



