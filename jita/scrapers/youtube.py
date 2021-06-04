from argparse import ArgumentParser
import requests
import json
from youtube_dl import YoutubeDL

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': 'songs/%(title)s-%(id)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'noplaylist':'True'}

def search(arg, options=YDL_OPTIONS):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]["id"]
    return f"https://www.youtube.com/watch?v={video}"

def download(url, options=YDL_OPTIONS):
    with YoutubeDL(options) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    parser = ArgumentParser("Extract Youtube Videos.")
    parser.add_argument("--search", help="Song name.", required=True)
    args = parser.parse_args()

    if args.search:
        video_url = search(args.search)
        download(video_url)
