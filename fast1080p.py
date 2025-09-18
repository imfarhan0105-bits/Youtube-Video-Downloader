from tkinter import *
from tkinter import filedialog, messagebox
from pytubefix import YouTube
import subprocess
import os
import re

# Helper to sanitize filenames
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

# Download and merge video/audio
def download():
    video_url = url_entry.get()
    save_path = path_label.cget("text")

    if not video_url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return
    if save_path == "Select path to download":
        messagebox.showerror("Error", "Please select a download folder")
        return

    try:
        yt = YouTube(video_url)

        # Try to get progressive 1080p stream (video + audio)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', res="1080p").first()

        if stream:
            final_file = os.path.join(save_path, f"{sanitize_filename(yt.title)}_1080p.mp4")
            stream.download(output_path=save_path, filename=final_file)
            messagebox.showinfo("Success", f"Downloaded:\n{final_file}")
            return

        # If progressive stream not available, download video-only + audio-only
        video_stream = yt.streams.filter(res="1080p", mime_type="video/mp4").first()
        audio_stream = yt.streams.filter(only_audio=True, mime_type="audio/mp4").first()

        if not video_stream or not audio_stream:
            messagebox.showerror("Error", "1080p video or audio stream not available for this video")
            return

        video_file = video_stream.download(output_path=save_path, filename="video.mp4")
        audio_file = audio_stream.download(output_path=save_path, filename="audio.mp4")
        final_file = os.path.join(save_path, f"{sanitize_filename(yt.title)}_1080p.mp4")

        # Merge with ffmpeg (fast, no re-encoding)
        subprocess.run([
            "ffmpeg", "-y", "-i", video_file, "-i", audio_file,
            "-c", "copy", final_file
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Remove temp files
        os.remove(video_file)
        os.remove(audio_file)

        messagebox.showinfo("Success", f"Downloaded in 1080p:\n{final_file}")

    except Exception as e:
        messagebox.showerror("Error", f"Download failed!\n{str(e)}")

# Select download folder
def get_path():
    path = filedialog.askdirectory()
    if path:
        path_label.config(text=path)

# GUI
root = Tk()
root.title('Video Downloader')
canvas = Canvas(root, width=400, height=300)
canvas.pack()

app_label = Label(root, text="Video Downloader", fg='blue', font=('Arial', 20))
canvas.create_window(200, 20, window=app_label)

url_label = Label(root, text="Enter video URL")
url_entry = Entry(root, width=40)
canvas.create_window(200, 80, window=url_label)
canvas.create_window(200, 100, window=url_entry)

path_label = Label(root, text="Select path to download")
path_button = Button(root, text="Select", command=get_path)
canvas.create_window(200, 150, window=path_label)
canvas.create_window(200, 170, window=path_button)

download_button = Button(root, text="Download", command=download, bg="green", fg="white")
canvas.create_window(200, 250, window=download_button)

root.mainloop()
