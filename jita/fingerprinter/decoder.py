# from https://github.com/worldveil/dejavu/blob/master/dejavu/logic/decoder.py
import fnmatch
import os
from hashlib import sha1
from typing import List, Tuple

import numpy as np
from pydub import AudioSegment

import hashlib

def checksum(filename, hash_factory=hashlib.md5, chunk_num_blocks=1024):
    h = hash_factory()
    with open(filename,'rb') as f:
        while chunk := f.read(chunk_num_blocks * h.block_size):
            h.update(chunk)
    return h.hexdigest()

def read(segment: AudioSegment) -> Tuple[List[List[int]], int, str]:
    """
    Reads any file supported by pydub (ffmpeg) and returns the data contained
    within.

    Can be optionally limited to a certain amount of seconds from the start
    of the file by specifying the `limit` parameter. This is the amount of
    seconds from the start of the file.

    :param file_name: file to be read.
    :return: tuple list of (channels, sample_rate, content_file_hash).
    """
    # pydub does not support 24-bit wav files, use wavio when this occurs
    data = np.fromstring(segment.raw_data, np.int16)

    channels = []
    for chn in range(segment.channels):
        channels.append(data[chn::segment.channels])

    return channels, segment.frame_rate
