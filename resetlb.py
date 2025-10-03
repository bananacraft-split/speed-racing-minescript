import lib
import probe
import sys

cut_index = probe.cutscene_index_from_name(sys.argv[1])

if cut_index is not None:
    print(cut_index)
    lib.execute(f"execute as @e[type=minecraft:text_display,tag=lbs,scores={{TIME=..100000,TRACK={cut_index}}}] run function speedracing:zzzprivate/leaderboard/delete_leaderboard_slow")
    lib.execute(f"execute as @e[type=minecraft:text_display,tag=lbf,scores={{TIME=..100000,TRACK={cut_index}}}] run function speedracing:zzzprivate/leaderboard/delete_leaderboard_fast")