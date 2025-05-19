from fastapi import FastAPI, Request
from downloader import check_video_safe, download_youtube_video
from youtube_uploader import upload_to_youtube

app = FastAPI()

@app.post("/upload")
async def upload_video(request: Request):
    data = await request.json()
    youtube_url = data.get("url")
    if not youtube_url:
        return {"status": "error", "message": "No URL provided"}

    is_safe, reason = check_video_safe(youtube_url)
    if not is_safe:
        return {"status": "rejected", "message": f"Skipped due to copyright risk: {reason}"}

    video_path, title, description = download_youtube_video(youtube_url)
    upload_result = upload_to_youtube(video_path, title, description)

    return {"status": "success", "message": upload_result}
