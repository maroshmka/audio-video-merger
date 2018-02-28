#!/bin/bash

# you will have executable app in dist folder
pyinstaller main.py --onefile --icon=app.ico --name audio_video_merger
