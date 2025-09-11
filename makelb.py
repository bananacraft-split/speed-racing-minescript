import sys
import lib
import minescript as m
import probe

def get_lb_xz(x,z):
    if m.player_position()[2] > z:
        return x + 0.5, z + 0.1
    return x + 0.5, z + 0.9
def get_lb_rot(x,z):
    if m.player_position()[2] > z:
        return (0,0)
    return (180,0)


def make_leaderboard(INDEX, x, y, z, name):
    x,z = get_lb_xz(x,z)
    y = -58
    rot = get_lb_rot(x,z)
    lib.execute(f"""summon text_display {x:.1f} {y+0.3:.1f} {z:.1f} {{text:'"{name.replace("'","\'")}"',Tags:["new","lbd","LB"],Rotation:[{rot[0]}f,{rot[1]}f],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.7f,1.7f,1.7f]}}}}""")
    lib.execute(f"""summon text_display {x:.1f} {y:.1f} {z:.1f} {{text:'"End of leaderboard"',Tags:["new","lb","LB"],Rotation:[{rot[0]}f,{rot[1]}f]}}""")
    lib.execute(f"scoreboard players set @e[tag=new,type=text_display] TRACK {INDEX}")
    lib.execute("scoreboard players set @e[tag=new,type=text_display,tag=lb] TIME 1000000")
    lib.execute("scoreboard players set @e[tag=new,type=text_display,tag=lb] ID -1")
    lib.execute(f"""summon marker {x:.1f} {y:.1f} {z:.1f} {{Tags:["new","lb","LB"],Rotation:[{rot[0]}f,{rot[1]}f]}}""")
    lib.execute(f"scoreboard players set @e[tag=new,type=marker] TRACK {INDEX}")
    lib.execute("tag @e[tag=new] remove new")

if __name__ == "__main__":
    NAME = sys.argv[1]
    i = probe.cutscene_index_from_name(NAME)

    x,y,z, _ = lib.get_block_coords()
    make_leaderboard(i,x,y,z,probe.name_from_name(NAME))