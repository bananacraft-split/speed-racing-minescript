import lib
import sys

TRACK = int(sys.argv[1])

def remove_track(index):
    if lib.is_track(index):
        x = 170 + index * 2
        lib.execute(f"fill {x} -58 -14 {x} -57 -19 air")
        lib.execute(f"fill {x} -56 -19 {x} -60 -67 air")

remove_track(TRACK)