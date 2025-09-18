# YouTube 1080p Video Downloader (Python GUI)

A simple Python GUI application to download YouTube videos in 1080p using pytubefix and MoviePy.

## Features
- Download 1080p video + audio separately and merge them.
- Simple GUI using Tkinter.
- Select download folder.
- Handles missing streams gracefully.

## Installation
1. Clone the repo.
2. Create a virtual environment and activate it.
3. Install dependencies:
4. Make sure `ffmpeg` is installed on your system.

## Usage
- Run `python video_downloader.py`. --- if you want a basic quality video downloaded on your system

- Run `python vid1080p.py`. --- if you want a 1080p high quality video downloaded on your system. It will take time and will make a few temporary files as it extracts video and audio separately and then merge them to give you the final video, but will download your video successfully.

- Run `python fast1080p.py`. --- if you want a high 1080p quality video downloaded on your system at a relatively faster rate. I have skipped the reincodingto make t=the download faster.

- Enter YouTube URL, select download folder, click **Download**.

HAPPY DOWNLOADING !!!!!!!

## License
MIT