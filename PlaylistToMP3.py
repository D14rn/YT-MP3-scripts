if __name__ == "__main__":
    from pytube import Playlist
    from moviepy.editor import *
    import os

    cwd = os.getcwd()
    downloadPath = cwd + "/Downloads/"

    playlist = Playlist(input("Enter a YouTube playlist: "))

    for video in playlist.videos:
        try:
            title = video.title.replace("*", "")
            if os.path.exists(downloadPath + title + ".mp3"):
                print(f"Download for {title} failed. File already exists")
            else:
                out_file = video.streams.get_by_itag(18).download(output_path=downloadPath)
                print(f"Download for {title} completed successfully.")
                try:
                    video_part = VideoFileClip(downloadPath + title + ".mp4")
                    audio_part = video_part.audio
                    audio_part.write_audiofile(downloadPath + title + ".mp3")
                    print(f"{title} was converted successfully.")
                    video_part.close()
                except Exception as e:
                    print(e)
                    print(f"Conversion for {title} failed.")
        except:
            print(f"Download for {title} failed.")

    for file in os.listdir(downloadPath):
        if file.endswith(".mp4"):
            os.remove(downloadPath + file)
