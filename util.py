import os
import platform
import subprocess
import re
from datetime import datetime


def get_duration_in_sec(filename):
    """
    Valid for any audio file accepted by ffprobe.
    Smoke tested on formats
      audio: .aiff .mp3 .wav
      video: .avi .mp4 .webm
    """
    args = ("ffprobe", "-show_entries", "format=duration", "-i", filename)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = popen.communicate()

    if type(output) == bytes:
        output = output.decode("utf-8")
    if output == '':
        raise Exception(err.decode("utf-8"))

    match = re.search(r"[-+]?\d*\.\d+|\d+", output)
    return float(match.group())


# !!! Cannot use create date: https://www.infonautics.ch/blog/how-to-correct-wrong-file-dates/
def get_creation_time_in_sec(filename):
    """
    Try to get creation time of file, on fail
    get last modified.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(filename)
    else:
        stat = os.stat(filename)
        try:
            return stat.st_birthtime
        except AttributeError:
            # Probably on Linux - it is hard to get
            # creation time so get last modified
            return stat.st_mtime


class NoEncodedDateException(Exception):
    """Media file does not contain Encoded Date information."""
    pass


# See https://mediaarea.net/en/MediaInfo
def get_encoded_date_in_sec(filename):
    """
    Use mediainfo to get Encoded date if present in file.
    :return:
    """
    args = ("mediainfo", filename)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = popen.communicate()

    if type(output) == bytes:
        output = output.decode("utf-8")
    if output == '\n':
        raise FileNotFoundError('File \'%s\' not found!' % filename)

    match = re.search(r"Encoded date *: (?:[A-Z]+ )?(.*)\n", output)

    if match is None:
        raise Exception('File does not contain Encoded date info!')

    return datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S').timestamp()

# NOTE: When labeling of records will be decided
#
# def get_input_file_time_format():
#     """
#     Get string format of recorded time in which
#     a take of a scene occurred.
#
#     For format modification see official docs:
#     https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
#     """
#     return '%d-%m-%Y %I:%M:%S %p'
