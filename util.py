import os
import platform
import subprocess
import re
from datetime import datetime


class ThirdPartyMissing(Exception):
    pass


def _check_in_cli(command):
    try:
        args = (command)
        popen = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise ThirdPartyMissing('Zabudol si nainstalovat %s! Pozri README.md.' % command)


def check_third_party():
    _check_in_cli("mediainfo")
    _check_in_cli("ffprobe")


def get_duration_in_sec(filepath):
    """
    Valid for any audio file accepted by ffprobe.
    Smoke tested on formats
      audio: .aiff .mp3 .wav
      video: .avi .mp4 .webm
    """
    args = ("ffprobe", "-show_entries", "format=duration", "-i", filepath)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = popen.communicate()

    if type(output) == bytes:
        output = output.decode("utf-8")
    if output == '':
        raise Exception(err.decode("utf-8"))

    match = re.search(r"[-+]?\d*\.\d+|\d+", output)
    return float(match.group())


# !!! Cannot use create date: https://www.infonautics.ch/blog/how-to-correct-wrong-file-dates/
def get_creation_time_in_sec(filepath):
    """
    Try to get creation time of file, on fail
    get last modified.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(filepath)
    else:
        stat = os.stat(filepath)
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
def get_encoded_date_in_sec(filepath):
    """
    Use mediainfo to get Encoded date if present in file.
    :return:
    """
    args = ("mediainfo", filepath)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = popen.communicate()

    if type(output) == bytes:
        output = output.decode("utf-8")
    if output == '\n':
        raise FileNotFoundError('File \'%s\' not found!' % filepath)

    match = re.search(r"Encoded date *: (?:[A-Z]+ )?(.*)\n", output)

    if match is None:
        raise NoEncodedDateException('File does not contain Encoded date info!')

    encoded_date_str = match.group(1).strip()

    encoded_date = datetime.strptime(encoded_date_str, '%Y-%m-%d %H:%M:%S').timestamp()

    return encoded_date


def load_config():
    with open('config.txt', 'r') as f:
        config = {}
        for line in f.readlines():
            item = line.strip().split('=')
            config[item[0]] = item[1]
        return config


def inject_config_if_missing(args, config, config_var_name, logger):
    if getattr(args, config_var_name) is None:
        if (config_var_name not in config.keys()) or \
                (config[config_var_name] == '') or \
                (config[config_var_name][0] == '<'):
            logger.error('Nastav \'%s\' ty baran!' % config_var_name)
            exit(1)
        setattr(args, config_var_name, config[config_var_name])


def setup_logger(_logging, logger_name):
    if not os.path.isdir('log'):
        os.mkdir('log')

    log_filename = '{}.log'.format(datetime.now().isoformat(timespec='minutes'))
    log_filepath = os.path.join('log', log_filename)

    file_handler = _logging.FileHandler(log_filepath)
    file_handler.setLevel(_logging.DEBUG)

    console_handler = _logging.StreamHandler()
    console_handler.setLevel(_logging.INFO)

    _logging.basicConfig(level=_logging.DEBUG,
                        format='%(asctime)s [%(name)-10.10s] [%(levelname)-7.7s]  %(message)s',
                        handlers=[file_handler, console_handler])

    return _logging.getLogger(logger_name)


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
