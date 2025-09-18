from tkinter import *
from tkinter import filedialog, messagebox
from pytubefix import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import os

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

        # Get 1080p video stream (video only)
        video_stream = yt.streams.filter(res="1080p", mime_type="video/mp4").first()
        # Get best audio stream
        audio_stream = yt.streams.filter(only_audio=True, mime_type="audio/mp4").first()

        if not video_stream or not audio_stream:
            messagebox.showerror("Error", "1080p video or audio stream not available for this video")
            return

        # Download video and audio
        video_file = video_stream.download(output_path=save_path, filename="video.mp4")
        audio_file = audio_stream.download(output_path=save_path, filename="audio.mp4")

        # Merge video and audio using MoviePy
        video_clip = VideoFileClip(video_file)
        audio_clip = AudioFileClip(audio_file)
        final_clip = video_clip.set_audio(audio_clip)

        final_file = os.path.join(save_path, f"{yt.title}_1080p.mp4")
        final_clip.write_videofile(final_file, codec="libx264", audio_codec="aac")

        # Close clips
        video_clip.close()
        audio_clip.close()
        final_clip.close()

        messagebox.showinfo("Success", f"Downloaded in 1080p:\n{final_file}")

    except Exception as e:
        messagebox.showerror("Error", f"Download failed!\n{str(e)}")

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
