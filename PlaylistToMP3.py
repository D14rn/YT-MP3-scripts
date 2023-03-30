if __name__ == "__main__":
    from pytube import Playlist
    from moviepy.editor import *
    import os

    cwd = os.getcwd()
    downloadPath = cwd + "/Downloads/"

    playlist = Playlist(input("Enter a YouTube playlist: "))
    i = 1
    
    for video in playlist.videos:
        try:
            title = ""
            title += str(i)
            title += " "
            for char in video.title:
                if char.isalnum():
                    title += char
            if os.path.exists(downloadPath + title + ".mp3"):
                print(f"Download for {title} failed. File already exists.")
            elif os.path.exists(downloadPath + video.title + ".mp3"):
                print(f"Download for {video.title} failed. File already exists.")
            else:
                out_file = video.streams.get_by_itag(18).download(output_path=downloadPath)
                print(f"Download for {title} completed successfully.")
                try:
                    video_part = VideoFileClip(out_file)
                    audio_part = video_part.audio
                    out_path = downloadPath + title + ".mp3"
                    audio_part.write_audiofile(out_path)
                    print(f"{title} was converted successfully.")
                    video_part.close()
                except:
                    print(f"Conversion for {title} failed.")
        except:
            print(f"Download for {title} failed.")
        i += 1

    for file in os.listdir(downloadPath):
        if file.endswith(".mp4"):
            os.remove(downloadPath + file)