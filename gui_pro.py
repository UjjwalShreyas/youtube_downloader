import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import threading

# ---------------------------------------
# DARK THEME
# ---------------------------------------
def set_dark_theme(window):
    window.configure(bg="#1e1e1e")
    style = ttk.Style(window)
    style.theme_use("clam")

    style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Arial", 11))
    style.configure("TButton", background="#333333", foreground="white", font=("Arial", 11), padding=6)
    style.map("TButton", background=[("active", "#444444")])

    style.configure("TCombobox",
                    fieldbackground="#333333",
                    background="#333333",
                    foreground="white")
    style.map("TCombobox", fieldbackground=[("readonly", "#333333")])

# ---------------------------------------
# START DOWNLOAD IN SEPARATE THREAD
# ---------------------------------------
def start_download_thread():
    thread = threading.Thread(target=start_download)
    thread.start()

# ---------------------------------------
# DOWNLOAD FUNCTION
# ---------------------------------------
def start_download():
    url = url_entry.get().strip()
    res = resolution_var.get().strip()
    folder = folder_var.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    if not folder:
        messagebox.showerror("Error", "Please choose a download folder.")
        return

    status_label.config(text="Starting download...", foreground="#00b7ff")
    progress_bar["value"] = 0
    window.update_idletasks()

    # Progress hook from yt-dlp
    def progress_hook(d):
        if d["status"] == "downloading":
            try:
                percent = d["_percent_str"].replace("%", "")
                progress_bar["value"] = float(percent)
            except:
                pass

        elif d["status"] == "finished":
            progress_bar["value"] = 100
            status_label.config(text="Merging audio & video...", foreground="#ffaa00")
            window.update_idletasks()

    # Format handling
    base_format = (
        f"bestvideo[height<={res}]+bestaudio/best"
        if res != "Highest"
        else "best[protocol=m3u8]/bv*+ba/best"
    )

    # FULL FIX: ffmpeg path correctly provided
    ydl_opts = {
        "format": base_format,
        "merge_output_format": "mp4",
        "outtmpl": folder + "/%(title)s.%(ext)s",
        "http_headers": {"User-Agent": "Mozilla/5.0"},
        "progress_hooks": [progress_hook],
        "ffmpeg_location": r"C:/Users/ujjwa/Downloads/New folder/ffmpeg-master-latest-win64-gpl/bin"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        status_label.config(text="Download Complete!", foreground="#00ff6a")
        messagebox.showinfo("Success", "Video downloaded successfully!")

    except Exception as e:
        status_label.config(text="Error occurred!", foreground="#ff5555")
        messagebox.showerror("Error", str(e))

# ---------------------------------------
# CHOOSE FOLDER
# ---------------------------------------
def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

# ---------------------------------------
# GUI SETUP
# ---------------------------------------
window = tk.Tk()
window.title("YouTube Downloader PRO")
window.geometry("500x360")
window.resizable(False, False)

set_dark_theme(window)

# Title
title_label = ttk.Label(window, text="YouTube Downloader PRO", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# URL Input
url_frame = tk.Frame(window, bg="#1e1e1e")
url_frame.pack(pady=5)
ttk.Label(url_frame, text="YouTube URL:").pack(side=tk.LEFT)
url_entry = ttk.Entry(url_frame, width=40)
url_entry.pack(side=tk.LEFT, padx=5)

# Resolution Selector
res_frame = tk.Frame(window, bg="#1e1e1e")
res_frame.pack(pady=5)
ttk.Label(res_frame, text="Resolution:").pack(side=tk.LEFT)

resolution_var = tk.StringVar()
resolution_dropdown = ttk.Combobox(
    res_frame,
    textvariable=resolution_var,
    values=["Highest", "144", "240", "360", "480", "720", "1080"],
    width=10,
    state="readonly"
)
resolution_dropdown.current(0)
resolution_dropdown.pack(side=tk.LEFT, padx=5)

# Folder Selector
folder_frame = tk.Frame(window, bg="#1e1e1e")
folder_frame.pack(pady=8)
ttk.Label(folder_frame, text="Save To:").pack(side=tk.LEFT)
folder_var = tk.StringVar()
folder_entry = ttk.Entry(folder_frame, textvariable=folder_var, width=32)
folder_entry.pack(side=tk.LEFT, padx=5)
ttk.Button(folder_frame, text="Browse", command=choose_folder).pack(side=tk.LEFT)

# Download Button
download_btn = ttk.Button(window, text="Download", command=start_download_thread)
download_btn.pack(pady=15)

# Progress Bar
progress_bar = ttk.Progressbar(window, length=350)
progress_bar.pack(pady=10)

# Status Label
status_label = ttk.Label(window, text="", font=("Arial", 12))
status_label.pack()

window.mainloop()
