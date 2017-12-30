import os
from unittest import TestCase

import shutil

import settings
from merge import merge_audio_video

TESTS_FOLDER_NAME = 'tests'
TEST_FOLDER_PATH = os.path.join(settings.BASE_PATH, TESTS_FOLDER_NAME)

TMP_DIR_NAME = 'myvideofiles'
TMP_DIR_PATH = os.path.join(TEST_FOLDER_PATH, TMP_DIR_NAME)


class FunctionalTest(TestCase):

    def setUp(self):
        os.mkdir(TMP_DIR_PATH)
        file_video = 'v'
        file_audio = 'a'

        for i in range(5):
            v = '%s%s' % (file_video, i)
            a = '%s%s' % (file_audio, i)
            path_video = os.path.join(TMP_DIR_PATH, v)
            path_audio = os.path.join(TMP_DIR_PATH, a)

            with open(path_video, 'w') as f:
                f.write('aa')

            with open(path_audio, 'w') as f:
                f.write('aa')

        self.combinations = {
            1: {
                'folder_name': 'scene1',
                'audio': 'a1',
                'video': 'v1'
            },
            2: {
                'folder_name': 'scene2',
                'audio': 'a2',
                'video': 'v2'
            },
            3: {
                'folder_name': 'scene3',
                'audio': 'a3',
                'video': 'v3'
            }
        }

    def tearDown(self):
        shutil.rmtree(TMP_DIR_PATH)

    def test_merge(self):
        merge_audio_video(self.combinations, TMP_DIR_PATH)

        for i, comb in self.combinations.items():
            folder_path = os.path.join(TMP_DIR_PATH, comb['folder_name'])
            audio_path = os.path.join(folder_path, comb['audio'])
            video_path = os.path.join(folder_path, comb['video'])

            self.assertTrue(os.path.isdir(folder_path))
            self.assertTrue(os.path.isfile(audio_path))
            self.assertTrue(os.path.isfile(video_path))
