import errno
import os
import shutil

# For robustness, if tqdm not installed
try:
    from tqdm import tqdm
except Exception as e:
    def tqmd(iter, *args, **kwargs):
        return iter


def merge_audio_video(combinations, video_files_path):

    # todo - log bad paths
    for i, combination in combinations.items():
        folder_name = combination['folder_name']
        audio_name = combination['audio']
        video_name = combination['video']

        # create new folder
        new_folder = os.path.join(video_files_path, folder_name)
        os.mkdir(new_folder)

        # get old and new path
        audio_path = os.path.join(video_files_path, audio_name)
        video_path = os.path.join(video_files_path, video_name)
        new_audio_path = os.path.join(new_folder, audio_name)
        new_video_path = os.path.join(new_folder, video_name)

        # move/copy ? file
        shutil.move(audio_path, new_audio_path)
        shutil.move(video_path, new_video_path)


def makedirs_if_needed(filepath):
    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def move_files(dest_paths):
    """
    Move files to destination file locations
    and create new folders if needed.
    :param dest_paths: Dict of destination
                       file locations.
    :return: Nothing
    """
    for src_path, dest_path in tqdm(dest_paths.items(), desc='Moving', unit='file'):
        makedirs_if_needed(dest_path)
        shutil.move(src_path, dest_path)


def copy_files(dest_paths):
    """
    Copy files to destination file locations
    and create new folders if needed.
    :param dest_paths: Dict of destination
                       file locations.
    :return: Nothing
    """
    for src_path, dest_path in tqdm(dest_paths.items(), desc='Copying', unit='file'):
        makedirs_if_needed(dest_path)
        shutil.copy(src_path, dest_path)
