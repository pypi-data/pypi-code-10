import enum
import os
from rambutan3.enumeration.REnum import REnum


@enum.unique
class RFileAccessEnum(REnum):

    READ = os.R_OK
    WRITE = os.W_OK
    EXECUTE = os.X_OK
