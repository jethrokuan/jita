import csv
import os
from argparse import ArgumentParser

from jita.scrapers.youtube import search as youtube_search
from jita.scrapers.youtube import download as youtube_download
from jita.scrapers.ug import get_tab_url_from_search, get_tab
from jita.fingerprinter.fingerprint import fingerprint_file
from jita.db import *

parser = ArgumentParser("Scrape YT and UG for items.")
parser.add_argument("file", help="Input CSV file.")

args = parser.parse_args()

with open(args.file) as f:
    reader = csv.reader(f)
    for artist, title in reader:
        song_path = f'songs/{artist}-{title}.opus'
        if not os.path.exists(song_path):
            options = {
            'format': 'bestaudio/best',
                'outtmpl': f'songs/{artist}-{title}.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'opus',
                }],
                'noplaylist':'True'}
            video_url = youtube_search(f"{artist} - {title}")
            youtube_download(video_url, options=options)
        
        fingerprints, song_id = fingerprint_file(song_path)
            
        tab_url = get_tab_url_from_search(f"{artist} {title}")
        tab = get_tab(tab_url)
        tab.update({"song_id": song_id})

        with engine.begin() as connection:
            connection.execute(songs_table.insert(),
                               {"id": song_id,
                                "artist": artist,
                                "title": title,
                                "hashes": len(list(fingerprints))})
            connection.execute(fingerprints_table.insert(),
                               [{"song_id": song_id,
                                 "hash": h,
                                 "offset": int(o)} for h, o in fingerprints])
            connection.execute(tabs_table.insert(), tab)
            
            
