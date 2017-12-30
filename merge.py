import os
import shutil


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
