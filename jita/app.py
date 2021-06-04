from itertools import groupby
from jita.db import *
from jita.fingerprinter.config import *
from jita.fingerprinter.fingerprint import fingerprint_file
from sqlalchemy import select
import io

from flask import render_template, request
from flask import Flask
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/read', methods=["POST"])
def read_audio():
    # TODO: prevent need to write to temporary file
    with open("temp.ogg", "wb") as f:
        f.write(request.data)
    hashes , _ = fingerprint_file("temp.ogg")
    matches, dedup_hashes = find_matches(list(hashes))
    result = align_matches(matches, dedup_hashes, len(hashes))
    print(result)
    return result

def find_matches(hashes):
    # Create a dictionary of hash => offset pairs for later lookups
    mapper = {}
    for hsh, offset in hashes:
        if hsh in mapper.keys():
            mapper[hsh].append(offset)
        else:
            mapper[hsh] = [offset]
    values = list(mapper.keys())
    batch_size = 1000
    results = []
    dedup_hashes = {}
    for i in range(0, len(values), batch_size):
        with engine.begin() as conn:
            matches = conn.execute(fingerprints_table.select().where(fingerprints_table.c.hash.in_(values[i: i + batch_size]))).all()
            for hsh, sid, offset in matches:
                if sid not in dedup_hashes.keys():
                    dedup_hashes[sid] = 1
                else:
                    dedup_hashes[sid] += 1
                #  we now evaluate all offset for each  hash matched
                for song_sampled_offset in mapper[hsh]:
                    results.append((sid, offset - song_sampled_offset))
    return results, dedup_hashes

def align_matches(matches, dedup_hashes, queried_hashes: int,
                  topn: int = 2):
        """
        Finds hash matches that align in time with other matches and finds
        consensus about which hashes are "true" signal from the audio.
        :param matches: matches from the database
        :param dedup_hashes: dictionary containing the hashes matched without duplicates for each song
        (key is the song id).
        :param queried_hashes: amount of hashes sent for matching against the db
        :param topn: number of results being returned back.
        :return: a list of dictionaries (based on topn) with match information.
        """
        # count offset occurrences per song and keep only the maximum ones.
        sorted_matches = sorted(matches, key=lambda m: (m[0], m[1]))
        counts = [(*key, len(list(group))) for key, group in groupby(sorted_matches, key=lambda m: (m[0], m[1]))]
        songs_matches = sorted(
            [max(list(group), key=lambda g: g[2]) for key, group in groupby(counts, key=lambda count: count[0])],
            key=lambda count: count[2], reverse=True
        )

        song_id = songs_matches[0][0]

        with engine.begin() as conn:
            song_id, artist, title = conn.execute(select([songs_table.c.id, songs_table.c.artist, songs_table.c.title]).where(songs_table.c.id == song_id)).one()
            tab = conn.execute(select([tabs_table.c.tab]).where(tabs_table.c.song_id == song_id)).one()[0]
            hashes_matched = dedup_hashes[song_id]

        return {
            "song_id": song_id,
            "artist": artist,
            "title": title,
            "tab": tab,
            "hashes_matched": hashes_matched,
            "input_confidence": round(hashes_matched / queried_hashes, 2)
        }

if __name__ == "__main__":
    app.run()
