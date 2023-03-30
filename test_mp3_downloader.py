from pytube import YouTube, Playlist
from os import remove
from os.path import exists
import subprocess

DEF_MP4_FILENAME = "default.mp4"
DEF_MP3_FILENAME = "default.mp3"
ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_()[] "

FFMPEG_PREFIX = "ffmpeg-win64-v4.2.2"

def download_mp3(url: str=None,
                video: str=None,
                mp4_filename: str=DEF_MP4_FILENAME,
                mp3_filename: str=DEF_MP3_FILENAME,
                output_path: str=None):
    if exists(output_path + mp3_filename):
        print(f"Download for {mp3_filename} failed. File already exists.")
        return None
    if url is not None:
        yt = YouTube(url)
    elif video is not None:
        yt = video
    else:
        raise ValueError("No url or video provided.")
    title = yt.title
    stream = yt.streams.get_by_itag(18) # Get mp4 stream
    if stream is None:
        print(f"No stream found for {title}, aborting...")
        return None
    stream.download(output_path=output_path, filename=mp4_filename)
    subprocess.run([FFMPEG_PREFIX, # Run ffmpeg (ffmpeg-win64-v4.2.2.exe) => binary from imageio-ffmpeg
                    "-y", # Overwrite existing file
                    "-i", # Input file
                    output_path + mp4_filename, # Input file path
                    "-vn", # Disable video
                    output_path + mp3_filename], # Output file path
                    shell=True) # Run in shell
    print(f"Download for {title} completed successfully.")
    remove(output_path + mp4_filename) # Remove initial mp4 file after conversion to mp3
    return None

def download_mp3_from_playlist(url=None, output_path=None):
    playlist = Playlist(url)
    for index, video in enumerate(playlist.videos, start=1):
        title = f"{index} {clean_string(video.title)}"
        download_mp3(video=video, output_path=output_path, mp3_filename=title + ".mp3")

def clean_string(string):
    return "".join([char for char in string if char in ALLOWED_CHARS])