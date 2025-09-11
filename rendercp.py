import lib
import sys
import probe
import time
import makecp2

def corerct_checkpoint_marker(x,y,z,dx,dy,dz,selector):
    A  = round(dx * 100)
    B  = round(dy * 100)
    C  = round(dz * 100)
    D = round(- 10000 * (A * x + B * y + C * z))
    lib.execute(f'scoreboard players set {selector} W {D}')

def main():
    index = probe.index_from_name(sys.argv[1])
    cut_index = probe.probe_cutscene_index(index)
    tp_command = probe.probe_tp_command(index)
    lib.execute(f"tp @s {tp_command}")
    cp = 0
    time.sleep(1)
    while cp != 301:
        base_selector = f"@e[tag=CPM,scores={{TRACK={cut_index},OLDCP={cp}}},limit=1]"

        if not lib.is_entity(base_selector):
            break  # no entities left
        # if cp == 1:
        #     dx = int(lib.get_score(base_selector, "X")) / 100
        #     dy = int(lib.get_score(base_selector, "Y")) / 100
        #     dz = int(lib.get_score(base_selector, "Z")) / 100
        #     x = float(lib.get_double(base_selector, "Pos[0]"))
        #     y = float(lib.get_double(base_selector, "Pos[1]"))
        #     z = float(lib.get_double(base_selector, "Pos[2]"))
        
        # if cp == 101:
        #     if dx == int(lib.get_score(base_selector, "X")) / 100 and \
        #     dy == int(lib.get_score(base_selector, "Y")) / 100 and \
        #     dz == int(lib.get_score(base_selector, "Z")) / 100 and \
        #     x == float(lib.get_double(base_selector, "Pos[0]")) and \
        #     y == float(lib.get_double(base_selector, "Pos[1]")) and \
        #     z == float(lib.get_double(base_selector, "Pos[2]")):
        #         break


        def process(sel):
            lib.execute(f"tp @s {sel}")
            dx = int(lib.get_score(sel, "X")) / 100
            dy = int(lib.get_score(sel, "Y")) / 100
            dz = int(lib.get_score(sel, "Z")) / 100
            x = float(lib.get_double(sel, "Pos[0]"))
            y = float(lib.get_double(sel, "Pos[1]"))
            z = float(lib.get_double(sel, "Pos[2]"))
            path_val = lib.get_score(sel, "PATH")

            # choose color
            color = "lime"
            if path_val == "1":
                color = "red"
            elif path_val == "2":
                color = "blue"

            # make entities
            corerct_checkpoint_marker(x,y,z,dx,dy,dz,sel)
            makecp2.create_line_entity(x, y, z, dx, dy, dz, 1, f"{color}_wool")
            makecp2.create_plane_entity(x, y, z, dx, dy, dz, width=10, height=10, block=f"{color}_stained_glass")

        # process the "first" entity
        process(base_selector)

        # check for the sibling path if needed
        path = lib.get_score(base_selector, "PATH")
        if path == "1":
            other = f"@e[tag=CPM,scores={{TRACK={cut_index},OLDCP={cp},PATH=2}},limit=1]"
            # if lib.is_entity(other):
            process(other)
        elif path == "2":
            other = f"@e[tag=CPM,scores={{TRACK={cut_index},OLDCP={cp},PATH=1}},limit=1]"
            # if lib.is_entity(other):
            process(other)

        # advance to next cp
        cp = int(lib.get_score(base_selector, "CP"))
        time.sleep(1)


if __name__ == "__main__":
    main()