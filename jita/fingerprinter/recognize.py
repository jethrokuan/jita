from time import time
from typing import Dict

import jita.fingerprinter.decoder as decoder
from dejavu.base_classes.base_recognizer import BaseRecognizer
from jita.fingerprinter.settings import (ALIGN_TIME, FINGERPRINT_TIME, QUERY_TIME,
                                    RESULTS, TOTAL_TIME)

def recognize_file(self, filename: str) -> Dict[str, any]:
    channels, self.Fs, _ = decoder.read(filename, self.dejavu.limit)
    
    t = time()
    matches, fingerprint_time, query_time, align_time = self._recognize(*channels)
    t = time() - t

    results = {
        TOTAL_TIME: t,
        FINGERPRINT_TIME: fingerprint_time,
        QUERY_TIME: query_time,
        ALIGN_TIME: align_time,
        RESULTS: matches
    }

    return results
