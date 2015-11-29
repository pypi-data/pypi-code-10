from rambutan3.check_args.file.RFilePathMatcher import RFilePathMatcher
from rambutan3.op_sys.RFileAccessEnum import RFileAccessEnum
from rambutan3.op_sys.RFileTypeEnum import RFileTypeEnum


# noinspection PyPep8Naming
def CHECKED_FILE_PATH(file_type: RFileTypeEnum, *file_access_tuple: RFileAccessEnum):
    x = RFilePathMatcher(file_type, *file_access_tuple)
    return x
