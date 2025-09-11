import lib
import makelb
import probe
import sys
import re

cut_index = probe.cutscene_index_from_name(sys.argv[1])

if cut_index is not None:
    lib.echo("Please press F3+I on the leaderboard destination")
    x,y,z,_=lib.get_block_coords()
    x,z=makelb.get_lb_xz(x,z)
    rot = makelb.get_lb_rot(x,z)
    lib.execute(f"execute as @e[tag=LB,scores={{TRACK={cut_index}}}] at @s run tp @s {x:.1f} ~ {z:.1f} {rot[0]} {rot[1]}")
