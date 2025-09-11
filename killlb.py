import lib
import sys
import probe


cut_index = probe.cutscene_index_from_name(sys.argv[1])

if cut_index is not None:
    lib.execute(f"kill @e[tag=LB,scores={{TRACK={cut_index}}}]")