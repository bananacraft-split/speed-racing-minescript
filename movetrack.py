import lib
import minescript as m
import re
from maketrack import create_track
import sys
import time

import probe

if __name__ == "__main__":
    INDEX_FROM = probe.index_from_name(sys.argv[1])
    INDEX_TO = int(sys.argv[2]) * 4 + int(sys.argv[3]) - 5
    if lib.is_track(INDEX_FROM):
        if not lib.is_track(INDEX_TO):
            settings = probe.probe(INDEX_FROM)
            create_track(INDEX_TO, *settings)
            time.sleep(3)
            if lib.is_track(INDEX_TO):
                m.execute(f"\\removetrack {INDEX_FROM}")