from tkinter.filedialog import askdirectory, askopenfilename
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

def download_mp3_from_playlist(url: str=None, output_path: str=None):
    playlist = Playlist(url)
    for index, video in enumerate(playlist.videos, start=1):
        title = f"{index} {clean_string(video.title)}"
        download_mp3(video=video, output_path=output_path, mp3_filename=title + ".mp3")

def url_type(url):
    if url.startswith("https://www.youtube.com/playlist?list="):
        return "playlist"
    elif url.startswith("https://www.youtube.com/watch?v="):
        return "video"
    else:
        raise ValueError("Invalid url.")

def clean_url(url, video_type):
    if video_type == "playlist":
        return url
    elif video_type == "video":
        return url[:url.find("&")] if "&" in url else url
    else:
        raise ValueError("Invalid url.")

def clean_string(string):
    return "".join([char for char in string if char in ALLOWED_CHARS])

def trim_mp3(input_path, output_path, start, end):
    subprocess.run([FFMPEG_PREFIX,
                    "-y",
                    "-i",
                    input_path,
                    "-ss",
                    start,
                    "-t",
                    end,
                    output_path + (".mp3" if not output_path.endswith(".mp3") else "")],
                    shell=True)
    return None

def main():
    while True:
        print("Welcome to YouTube to mp3 converter!")
        print("This program will download a video or playlist from YouTube and convert it to mp3.")
        print("You can also trim the mp3 file to a specific time range.")
        print("Make your choice below:")
        print("1. Download a video or playlist")
        print("2. Trim an mp3 file")
        choice = input("Enter your choice: ")
        if choice == "1":
            target = input("Enter video url or playlist url: ")
            video_type = url_type(target)
            print(f"Current url type: {video_type}")
            print(f"Correct type? (y/n)")
            correct = input()
            while correct == "n":
                target = input("Enter video url or playlist url: ")
                video_type = url_type(target)
                print(f"Current url type: {video_type}")
                print(f"Correct type? (y/n)")
                correct = input()
            url = clean_url(target, video_type)
            print(f"Current url: {url}")
            print(f"Choose output directory:")
            output = askdirectory() + "/"
            print(f"Current output directory: {output}")
            choice = input(f"Do you want to change the output directory? (y/n): ")
            while choice == "y":
                output = askdirectory() + "/"
                print(f"Current output directory: {output}")
                choice = input(f"Do you want to change the output directory? (y/n): ")
            filename = input("Enter filename (without extension, mp3 by default): ")
            if video_type == "playlist":
                download_mp3_from_playlist(url, output_path=output)
            elif video_type == "video":
                download_mp3(url, output_path=output, mp3_filename=filename+".mp3")
            else:
                raise ValueError("Invalid url.")
        elif choice == "2":
            print("Choose input file:")
            input_path = askopenfilename()
            print(f"Current input file: {input_path}")
            choice = input("Do you want to change the input file? (y/n): ")
            while choice == "y":
                input_path = askopenfilename()
                print(f"Current input file: {input_path}")
                choice = input("Do you want to change the input file? (y/n): ")
            print(f"Choose output directory:")
            output_path = askdirectory() + "/"
            output_name = input("Enter output filename (without extension, mp3 by default): ")
            output_path += output_name
            print(f"Current output directory: {output_path}")
            choice = input(f"Do you want to change the output directory? (y/n): ")
            while choice == "y":
                output_path = askdirectory() + "/"
                output_name = input("Enter output filename (without extension, mp3 by default): ")
                output_path += output_name
                print(f"Current output directory: {output_path}")
                choice = input(f"Do you want to change the output directory? (y/n): ")
            start = input("Enter start time (hh:mm:ss.ms, leave blank if start=0): ")
            if start == "":
                start = "0"
            end = input("Enter end time (hh:mm:ss.ms): ")
            trim_mp3(input_path, output_path, start, end)
        else:
            raise ValueError("Invalid choice.")

if __name__ == "__main__":
    main()