import test_mp3_downloader
from tkinter.filedialog import askdirectory

def main():
    output = test_mp3_downloader.DEF_OUTPUT
    playlist = input("Enter playlist url: ")
    print(f"Current output directory: {output}")
    choice = input(f"Do you want to change the output directory? (y/n): ")
    if choice == "y":
        output = askdirectory() + "/"
    test_mp3_downloader.download_mp3_from_playlist(playlist, output)
    return None

if __name__ == "__main__":
    main()