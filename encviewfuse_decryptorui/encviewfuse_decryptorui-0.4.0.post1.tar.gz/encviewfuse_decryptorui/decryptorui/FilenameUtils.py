import re
class FilenameUtils(object):

    @staticmethod
    def splitSegmentedFileName(filename):
        match = re.match('(.*)\.seg\.([0-9]+)', filename)
        if match is None:
            return filename, None
        return match.group(1), int(match.group(2))