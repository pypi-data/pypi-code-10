import os
import subprocess
import traceback
from xenonmkv.utils.mkv_info_parser import MKVInfoParser
from xenonmkv.utils.track import MKVTrack, VideoTrack

from process_handler import ProcessHandler

video_codec_table = {
    "V_MPEG4/ISO/AVC": ".h264"
}

audio_codec_table = {
    "A_AC3": ".ac3",
    "A_EAC3": ".eac3",  # mplayer should play EAC3 correctly
    "A_AAC": ".aac",
    "A_AAC/MPEG2/LC": ".aac",  # low complexity AAC
    "A_DTS": ".dts",
    "A_MP3": ".mp3",
    "A_MPEG/L3": ".mp3",
    "A_MS/ACM": ".mp3",  # MS/ACM: anime tends to have this identifier
    "A_VORBIS": ".ogg"
}


class MKVFile:
    def __init__(self, args, log):
        self.options = args
        self.options.tracks = {}
        self.video = []
        self.audio = []
        self.logger = log

    def get_mkvinfo(self):
        args = ['mkvinfo', self.options.source_file]
        self.logger.debug("Executing '{0}'".format(' '.join(args)))
        try:
            proc = subprocess.Popen(args, shell=False, bufsize=0, close_fds=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True)
            result, errs = proc.communicate()
        except subprocess.CalledProcessError:
            self.logger.debug("mkvinfo process error: {0}".format(traceback.format_exc()))
            raise Exception("Error occurred while obtaining MKV information "
                            "for {0} - please make sure the file exists, is readable and "
                            "a valid MKV file".format(self.options.source_file))

        self.logger.debug("mkvinfo finished; attempting to parse output")
        try:
            self.parse_mkvinfo(result)
        except:
            # Punt back exception from inner function to the main application
            raise Exception("Do not parse mkvinfo result.")

    # Parse the output from mkvinfo for the file.
    def parse_mkvinfo(self, result):
        track_detect_string = "| + A track"

        if not track_detect_string in result:
            raise Exception("mkvinfo: output did not contain any tracks")

        # Multiple track support:
        # Extract mediainfo profile for all tracks in file,
        # then cross-reference them with the output from mkvinfo.
        # This prevents running mediainfo multiple times.
        mediainfo_video_output = self.get_mediainfo('video')
        self.select_video(mediainfo_video_output)

        mediainfo_audio_output = self.get_mediainfo('audio')
        self.select_audio(mediainfo_audio_output)

        # For ease of use, throw these values into a dictionary
        # with the key being the track ID.
        try:
            mediainfo = {
                self.video[0]: self.video,
                self.audio[0]: self.audio
            }
        except Exception:
            traceback.print_exc()

        info_parser = MKVInfoParser(self.logger)
        while track_detect_string in result:
            if track_detect_string in result:
                result = result[result.index(track_detect_string) +
                                len(track_detect_string):]
            else:
                break

            track_number, track_mkvtoolnix_id = (
                info_parser.parse_track_number(result)
            )

            if not mediainfo.get(str(track_number)):
                continue

            track = mediainfo.get(str(track_number))
            self.logger.debug("Track {0} will use ID {1} when taking actions "
                              "with the mkvtoolnix suite"
                              .format(track_number, track_mkvtoolnix_id))

            # Set individual track properties for the object by track ID
            track.insert(5, str(track_mkvtoolnix_id))
            track_codec = track[1]
            if track_codec in video_codec_table:
                self.options.tracks['video'] = track
            elif track_codec in audio_codec_table:
                self.options.tracks['audio'] = track

        # All tracks detected here
        self.logger.debug("All tracks detected from mkvinfo output; "
                          "total number is {0}".format(len(self.options.tracks)))

    # Open the mediainfo process to obtain detailed info on the file.
    def get_mediainfo(self, track_type):
        if track_type == "video":
            parameters = ("Video;%ID%,%CodecID%,%Height%,%Width%,"
                          "%Format_Settings_RefFrames%,%Language%,%FrameRate%,"
                          "%DisplayAspectRatio%,%FrameRate_Original%,~")
        elif track_type == "audio":
            parameters = "Audio;%ID%,%CodecID%,%Language%,%Channels%,~"

        subprocess_args = ["mediainfo",
                           "--Inform=" + parameters, self.options.source_file]
        self.logger.debug("Executing '{0}'".format(' '.join(subprocess_args)))
        result = subprocess.check_output(subprocess_args)
        self.logger.debug("mediainfo finished; attempting to parse output "
                          "for {0} settings".format(track_type))
        return self.parse_mediainfo(result)

    def parse_mediainfo(self, result):
        output = []
        result = result.replace(os.linesep, "")

        # Obtain multiple tracks if they are present
        lines = result.split("~")
        lines = lines[0:-1]  # remove last tilde separator character

        for line in lines:
            # remove last element from array that will always be present
            values = line.split(",")
            # print values
            output.append(values)
        return output

    def select_audio(self, audio_track_list):
        temp = 0
        for audio_track in audio_track_list:
            channels = int(audio_track[3])
            if temp < channels:
                temp = channels
                self.audio = audio_track

        if temp < self.options.channels:
            self.options.channels = temp

        self.logger.debug('Select audio channels: {channels}'
                          .format(channels=str(self.options.channels)))

    def select_video(self, video_track_list):
        codec = ''
        for video_track in video_track_list:
            codec = video_track[1]
            if codec in video_codec_table:
                self.video = video_track

        self.logger.debug('Select video codec: {codec}'
                          .format(codec=codec))

    def extract_mkv(self):
        self.logger.debug("Executing mkvextract on '{0}'".format(self.options.source_file))
        os.chdir(self.options.scratch_dir)

        if self.options.scratch_dir != ".":
            self.logger.debug("Using {0} as scratch directory for "
                              "MKV extraction".format(self.options.scratch_dir))

        video_track_id = int(self.options.tracks.get('video')[5]) - 1
        video_codec = self.options.tracks.get('video')[1]
        audio_track_id = int(self.options.tracks.get('audio')[5]) - 1
        audio_codec = self.options.tracks.get('audio')[1]
        try:
            temp_video_file = "temp_video{extension}".format(
                extension=video_codec_table[video_codec])
            self.logger.debug("Detected video extension: {extension}".format(
                extension=video_codec_table[video_codec]))

            temp_audio_file = "temp_audio{extension}".format(
                extension=audio_codec_table[audio_codec])
            self.logger.debug("Detected audio extension: {extension}".format(
                extension=audio_codec_table[audio_codec]))
        except UnsupportedCodecError:
            # Send back to main application
            raise

        if (os.path.isfile(temp_video_file) and
                os.path.isfile(temp_audio_file)):
            self.logger.debug("Temporary video and audio files already exist; "
                              "cancelling extract")
            temp_video_file = os.path.join(self.options.scratch_dir, temp_video_file)
            temp_audio_file = os.path.join(self.options.scratch_dir, temp_audio_file)
            return temp_video_file, temp_audio_file

        # Remove any existing files with the same names
        if os.path.isfile(temp_video_file):
            self.logger.debug("Deleting temporary video file {0}".format(
                os.path.join(self.options.scratch_dir, temp_video_file)))
            os.unlink(temp_video_file)
        if os.path.isfile(temp_audio_file):
            self.logger.debug("Deleting temporary audio file {0}".format(
                os.path.join(self.options.scratch_dir, temp_audio_file)))
            os.unlink(temp_audio_file)

        for step in range(3):
            self.logger.debug("Using video track from MKV file with ID {0} "
                              .format(str(video_track_id)))
            self.logger.debug("Using audio track from MKV file with ID {0} "
                              .format(str(audio_track_id)))

            video_output = str(video_track_id) + ":" + temp_video_file
            audio_output = str(audio_track_id) + ":" + temp_audio_file

            cmd = ['mkvextract', "tracks",
                   self.options.source_file, video_output, audio_output]
            ph = ProcessHandler(self.options, self.logger)
            process = ph.start_output(cmd)

            if process == 0:
                break

            if process != 0 and step == 2:
                raise Exception("An error occurred while extracting tracks from {0}"
                                " - please make sure this file exists and is readable"
                                .format(self.options.source_file))
            video_track_id += 1
            audio_track_id += 1

        temp_video_file = os.path.join(self.options.scratch_dir, temp_video_file)
        temp_audio_file = os.path.join(self.options.scratch_dir, temp_audio_file)

        self.logger.debug("mkvextract finished; attempting to parse output")

        if not temp_video_file or not temp_audio_file:
            raise Exception("Audio or video file missing from "
                            "mkvextract output")

        return temp_video_file, temp_audio_file


class UnsupportedCodecError(Exception):
    pass
