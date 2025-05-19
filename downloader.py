import yt_dlp
import uuid
import os

RISKY_CHANNELS = ["t-series", "sony music", "zeemusic", "yash raj", "saregama"]
RISKY_LICENSES = ["standard youtube license"]

def check_video_safe(url):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            uploader = info.get("uploader", "").lower()
            license_info = info.get("license", "").lower()

            for risky in RISKY_CHANNELS:
                if risky in uploader:
                    return False, f"Uploader {uploader} is likely copyrighted"

            for risky in RISKY_LICENSES:
                if risky in license_info:
                    return False, f"License '{license_info}' is not safe"

            return True, "No known copyright risk"
    except Exception as e:
        return False, str(e)

def download_youtube_video(url):
    filename = f"{uuid.uuid4()}.mp4"
    options = {
        'format': 'best',
        'outtmpl': filename,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url)
        title = info.get("title", "No Title")
        description = info.get("description", "No Description")
    return filename, title, description
