import yt_dlp

def download_video():
    print('*******Welcome to YouTube Video Downloader*******')
    print('-----------------------------------')    
    url = input("Enter YouTube URL: ")

    ydl_opts = {
        'format': 'bv*+ba/best',
        'merge_output_format': 'mp4',
        'outtmpl': '%(title)s.%(ext)s',
        'http_headers': {'User-Agent': 'Mozilla/5.0'},
        'force_client': 'android',
        'nocheckcertificate': True
    }

    try:
        print("Downloading... please wait.")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Done! Your video is ready.")

    except Exception as e:
        print("Error:", e)

download_video()
