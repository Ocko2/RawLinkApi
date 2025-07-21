from flask import Flask, request
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/extract')
def extract():
    video_url = request.args.get('url')
    if not video_url:
        return "Missing 'url' parameter", 400

    ydl_opts = {
        'format': 'bestaudio+bestaudio/best',
        'quiet': True,
        'skip_download': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)

    formats = info.get('formats', [])

    video_link = None
    audio_link = None

    video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') == 'none']
    if video_formats:
        video_formats.sort(key=lambda x: x.get('height') or 0, reverse=True)
        video_link = video_formats[0]['url']

    audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
    if audio_formats:
        audio_formats.sort(key=lambda x: x.get('abr') or 0, reverse=True)
        audio_link = audio_formats[0]['url']

    if not video_link or not audio_link:
        return "Could not find separate video or audio streams.", 400

    return f"Video link:\n{video_link}\n\nAudio link:\n{audio_link}"

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
