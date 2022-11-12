if __name__ == "__main__":
    from pytube import Playlist
    import os
    
    cwd = os.getcwd()
    downloadPath = cwd + "/Downloads"
    
    playlist = Playlist(input("Enter a YouTube playlist: "))

    for video in playlist.videos:
        try:
            title = video.title
            if os.path.exists(downloadPath + "/" + title + ".mp3"):
                print(f"Download for {title} failed. File already exists")
            else:
                out_file = video.streams.filter(only_audio=True).first().download(output_path=downloadPath)
                name, ext = os.path.splitext(out_file)
                new_file = name + ".mp3"
                os.rename(out_file, new_file)
                print(f"Download for {title} completed successfully.")
        except:
            print(f"Download for {title} failed.")
