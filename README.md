# Merger

Group audio and video records into folder (by moving or copying)
based on time they were recorded.

## Install

In order to install you need following:
* `Python 3`
* `mediainfo`
* `tqdm` library (optional for progress bar)

### Python 3

* Go to https://www.python.org/downloads/
* Download latest Python 3
* Install it

### Mediainfo

* Go to https://mediaarea.net/en/MediaInfo/Download
* Choose you OS
* Download `CLI` version for your architecture
* Install it

### tqdm (optional)

Tqdm is used to show progress bar in command line. It can be installed
from using `requirements.txt` or separately if you don't want testing
dependencies.

* Run command prompt or terminal
* Type `pip3 install tqdm` (in case it fails try `pip install tqdm`)

This dependency is used to get _Encoded date_ from records.

## Usage
    ``python3 main.py path/to/video/files path/to/audio/files path/to/output/dir``

Use `-h` for help.

### Config

In order to make life easier you can use `config.txt` file to set input
parameters.

* Make a copy of `config.txt.template`
* Name it `config.txt`
* Replace `<path\to\video_dir>`, `<path\to\audio_dir>` and `<path\to\output_dir>` with corresponding paths.


## Test

Create a virtual env and install all dependencies from `requirements.txt`.
To run tests just use `pytest`.
