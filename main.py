from loader import load_csv
from merge import merge_audio_video
import argparse


def run(video_files_path):
    combinations = load_csv()
    merge_audio_video(combinations, video_files_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-vf', '--video-files', type=str,
                        help='Specify path to video file.')

    parser.add_argument('-i', '--input', type=str,
                        help='Specify path to input file.')

    args = parser.parse_args()

    if not args.video_files:
        print('You need to specify path to video files. Use -h for help.')
        exit(1)

    run(args.video_files)
