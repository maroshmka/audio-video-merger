import logging
from os import walk
from os.path import isfile, isdir, join, splitext

from numpy.core.numeric import extend_all

from util import *

logger = logging.getLogger(__name__)

"""
interface Organizer:

    __init__(input_file=None)
        Organizer can use labels from input_file
        to create mappings into output_dir for
        records.

    get_dest_paths(record_files, output_dir)
        Return dict of destination file locations
        for record files in the output_dir.
"""

"""
Mandatory keys in mapping dict.
"""
MAPPING_PROPS = {'old_path', 'new_path'}


class DateBasedOrganizer:
    """
    Organize records (create mappings) based on
    record creation time.
    """

    class Record:
        """Util struct for working with record data."""
        def __init__(self, filename, creation_time, duration):
            self.filename = filename
            self.creation_time = creation_time
            self.duration = duration
            self.finish_time = creation_time + duration

        def overlap_with(self, record):
            return ((self.creation_time < record.finish_time) and
                    (record.creation_time < self.finish_time))

    def __init__(self, input_file=None):
        # Input file will be needed for annotations
        # self.input_file = input_file
        pass

    def _create_sorted_records(self, record_filenames):
        """
        Create list of DateBasedOrganizer.Record objects
        sorted by creation date.
        """
        records = []
        for filename in record_filenames:
            try:
                creation_time = get_encoded_date_in_sec(filename)
            except NoEncodedDateException:
                logger.warning('Using \"creation / last modified '
                               'time\" for file \'%s\'!\n'
                               'Reason: The file does not contain \"Encoded'
                               ' Date\" metadata!\n')
                creation_time = get_creation_time_in_sec(filename)
            except FileNotFoundError as e:
                logger.error(str(e))
                creation_time = None
            finally:
                if creation_time is not None:
                    record = self.Record(filename, creation_time,
                                         get_duration_in_sec(filename))
                    records.append(record)

        records = sorted(records, key=lambda rec: rec.creation_time)

        return records

    def _group_records(self, records):
        """
        Group records into groups based on recording
        time overlap.
        :param records: List of DateBasedOrganizer.Record
                        objects.
        :return: List of lists of records.
        """
        record_groups = []
        if len(records) == 0:
            return record_groups
        active_record = records.pop(0)
        active_group = [active_record]

        for record in records:

            # Add record to group
            if active_record.overlap_with(record):
                active_group.append(record)

                # Change active record
                if active_record.finish_time < record.finish_time:
                    active_record = record

            # Finish active group
            else:
                record_groups.append(active_group)
                active_group = [record]
                active_record = record

        record_groups.append(active_group)

        return record_groups

    def _generate_dest_paths(self, record_groups, output_dir):
        """
        Simplest method preserving records basename and
        moving them to folders based on ordering in
        record_groups.
        :param record_groups: List of lists of records.
        :return Dict of destination filepaths for records.
        """
        if len(record_groups) >= 1000:
            raise NotImplementedError('This method generates'
                                      'only 3 digit filenames!')

        dest_paths = {}

        for i, record_group in enumerate(record_groups):
            folder_name = '%03d' % i

            for record in record_group:
                dest_paths[record.filename] = join(output_dir, folder_name, os.path.basename(record.filename))

        return dest_paths

    def get_dest_paths(self, record_files, output_dir):
        """
        Get dict of destination file locations
        for record files in the output_dir.
        """
        assert isdir(output_dir)

        logger.debug('Sorting records based on creation time...')

        records = self._create_sorted_records(record_files)

        logger.debug('Grouping records into groups based '
                     'on recording time overlap...')

        record_groups = self._group_records(records)

        logger.debug('Generating destination filepaths for records...')

        dest_paths = self._generate_dest_paths(record_groups, output_dir)

        return dest_paths


supported_extensions = {
    '.aiff', '.ape', '.au', '.flac', '.m4a', '.mp3', '.mpc',
    '.pcm', '.raw', '.wav', '.wma', '.wv',
    '.avi', '.m4v', '.m4p', '.mp2', '.mp4', '.mpg', '.mpeg',
    '.mkv', '.mov', '.webm', '.wmv'
}


def is_record(file):
    """
    Determine if the file is desired audio
    or video record.
    """
    global supported_extensions
    _, extension = splitext(file)
    return extension.lower() in supported_extensions


def get_record_filenames(dirname):
    filenames = []
    for (dirpath, dirnames, _filenames) in walk(dirname):
        filenames.extend([join(dirpath, f) for f in _filenames if is_record(f)])
    return filenames


def load_csv():
    # todo - use loader for this
    combinations = {
        1: {
            'folder_name': 'scene1',
            'audio': 'a1',
            'video': 'v1'
        },
        2: {
            'folder_name': 'scene2',
            'audio': 'a2',
            'video': 'v2'
        }
    }

    return combinations
