import sys

from pydub import AudioSegment
from jita.app import find_matches, align_matches
from jita.fingerprinter.fingerprint import fingerprint_segment

segment = AudioSegment.from_file(sys.argv[1])
hashes = fingerprint_segment(segment)
matches, dedup_hashes = find_matches(list(hashes))
results = align_matches(matches, dedup_hashes, len(hashes))
print(results["title"], results["input_confidence"])
