import argparse
import logging
from os import mkdir
from os.path import dirname, join, isdir

from loader import DateBasedOrganizer, get_record_filepaths
from merge import move_files, copy_files
from util import load_config, inject_config_if_missing, setup_logger

# Setup logging
logger = setup_logger(logging, __name__)


# Main function
def run(video_dir, audio_dir, output_dir=None, move=False):
    if output_dir is None:
        output_dir = join(dirname(__file__), 'results')
        if not isdir(output_dir):
            mkdir(output_dir)

    logger.info('Prehladavam zlozky ktore si zadal...')

    files = get_record_filepaths(video_dir)
    files.extend( get_record_filepaths(audio_dir) )

    logger.info('Nasiel som %d nahravok. (konkretne mas v logu)' % len(files))
    logger.debug('Najdene nahravky:\n%s' % '\n'.join(files))

    logger.info('Skupinkujem ti nahravky...')

    organizer = DateBasedOrganizer()
    dest_paths = organizer.get_dest_paths(files, output_dir)

    logger.debug('Takto premiestnim/zkopirujem nahravky:\n')
    logger.debug('\n'.join(['\'%s\' -> \'%s\'' % mapping for mapping in dest_paths.items()]))

    if move:
        move_files(dest_paths)
    else:
        copy_files(dest_paths)


# Arguments handling
if __name__ == '__main__':
    logger.debug('Asi budes zmäteny z toho ze raz pisem po slovensky'
                 'a raz po anglicky. Nezufaj!')
    parser = argparse.ArgumentParser()
    parser.add_argument('video_dir', type=str, nargs='?',
                        help='Toto je zlozka kde mas videjka.')

    parser.add_argument('audio_dir', type=str, nargs='?',
                        help='Toto je zlozka kde mas videjka.')

    parser.add_argument('output_dir', type=str, nargs='?', default=None,
                        help='Tu ti to vypluje. Ak to nezadas tak ti to hodim sem '
                             'do projektu do zlozky results.')

    parser.add_argument('-m', '--move', type=bool,
                        help='Ci to chces premiestnit miesto kopirovania.')

    args = parser.parse_args()

    config = {}
    try:
        config = load_config()
    except FileNotFoundError:
        logger.warning('Nemas este nastaveny \'config.txt\' file!'
                       ' Vytvor kopiu \'config.txt.template\', premenuj'
                       ' ju na \'config.txt\' a uprav parametre v nom.')

    inject_config_if_missing(args, config, 'video_dir', logger)
    inject_config_if_missing(args, config, 'audio_dir', logger)
    inject_config_if_missing(args, config, 'output_dir', logger)

    run(args.video_dir, args.audio_dir, args.output_dir, args.move)
