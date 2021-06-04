import sys
from jita.app import find_matches, align_matches
from jita.fingerprinter.fingerprint import fingerprint_file

hashes , _ = fingerprint_file(sys.argv[1])
matches, dedup_hashes = find_matches(list(hashes))
results = align_matches(matches, dedup_hashes, len(hashes))
print(results)
