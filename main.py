from loader import DateBasedOrganizer, get_record_filenames
from merge import move_files, copy_files
import argparse


def run(records_dir, output_dir=None, move=False):
    if output_dir is None:
        output_dir = records_dir

    files = get_record_filenames(records_dir)
    organizer = DateBasedOrganizer()
    dest_paths = organizer.get_dest_paths(files, output_dir)
    if move:
        move_files(dest_paths)
    else:
        copy_files(dest_paths)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('records_dir', type=str,
                        help='Specify path to directory containing'
                             ' desired video or audio files.')

    parser.add_argument('output_dir', type=str, nargs='?', default=None,
                        help='Specify path to video or audio files.')

    parser.add_argument('-m', '--move', type=bool,
                        help='Move video or audio files instead of copying.')

    # parser.add_argument('-i', '--input', type=str,
    #                     help='Specify path to input file.')

    args = parser.parse_args()

    if not args.records_dir:
        print('You need to specify path to video or audio files. Use -h for help.')
        exit(1)

    run(args.records_dir, args.output_dir, args.move)
