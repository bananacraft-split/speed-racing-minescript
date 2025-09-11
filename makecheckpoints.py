import time
import re
import pyperclip  # pip install pyperclip
import lib
import minescript as m
import sys

def get_coords(f1, f2):
        f1 = f1.split(",")
        f2 = f2.split(",")        # Calculate min coordinates
        x_min = min(int(f1[0]), int(f2[0]))
        y_min = min(int(f1[1]), int(f2[1]))
        z_min = min(int(f1[2]), int(f2[2]))

        # Calculate max coordinates
        x_max = max(int(f1[0]), int(f2[0]))
        y_max = max(int(f1[1]), int(f2[1]))
        z_max = max(int(f1[2]), int(f2[2]))

        # Differences
        dx = x_max - x_min
        dy = y_max - y_min
        dz = z_max - z_min

        return x_min, y_min, z_min, dx, dy, dz


def get_block_display_command(f1, f2, color="red"):
    x_min, y_min, z_min, dx, dy, dz = get_coords(f1, f2)
    return f'summon block_display {x_min}.0 {y_min}.0 {z_min}.0 {{block_state:{{Name:"minecraft:{color}_stained_glass"}},transformation:[{dx+1}f,0f,0f,0f,0f,{dy+1}f,0f,0f,0f,0f,{dz+1}f,0f,0f,0f,0f,1f],Tags:["CP"]}}'

def get_cp_update_command(f1, f2, a, b):
    x, y, z, dx, dy, dz = get_coords(f1, f2)
    return f'execute as @a[tag=RaceInProgress,scores={{CP={a}}},x={x},y={y},z={z},dx={dx},dy={dy},dz={dz}] run scoreboard players set @s CP {b}'
    # return f'summon block_display -28.0 -60.0 -20.0 {block_state:{Name:"minecraft:red_stained_glass",Properties:{}},transformation:{scale:[12f,10f,3f],translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]},Tags:["CP"]}'
#/summon block_display ~-0.5 ~-0.5 ~-0.5 {Passengers:[{id:"minecraft:block_display",block_state:{Name:"minecraft:red_stained_glass",Properties:{}},transformation:[12.0000f,0.0000f,0.0000f,0.0000f,0.0000f,10.0000f,0.0000f,0.0000f,0.0000f,0.0000f,1.0000f,0.0000f,0.0000f,0.0000f,0.0000f,1.0000f]}]}

def generate_commands(unique_fencegates, x, y, z):
    # Place the command block at the desired coordinates
    m.execute(
        f'/setblock {x} {y} {z} minecraft:command_block[conditional=false,facing=west]'
        '{Command:"kill @e[type=minecraft:block_display, tag=CP]"}'
    )
    m.execute(
        f"/setblock {x-1} {y} {z} minecraft:oak_button[face=wall,facing=west,powered=false]"
    )
    assert len(unique_fencegates) % 2 == 0
    for i in range(0, len(unique_fencegates), 2):
        I = i // 2
        FINISH_LINE = i == len(unique_fencegates) - 2
        f1 = unique_fencegates[i]
        f2 = unique_fencegates[i+1]
        bdc = get_block_display_command(f1, f2)
        m.execute(f'setblock {x+i//2} {y} {z-2} minecraft:command_block[conditional=false,facing=west]')
        m.execute(f"data modify block {x+i//2} {y} {z-2} Command set value '{bdc}'")

        for j in range(3):
            sbc = get_cp_update_command(f1, f2, I+1+j*100, I+2+j*100 if not FINISH_LINE else 101+j*100)
            m.execute(f'setblock {x+i//2} {y} {z+2+j} minecraft:repeating_command_block[conditional=false,facing=west]{{auto:1b}}')
            m.execute(f"data modify block {x+i//2} {y} {z+2+j} Command set value '{sbc}'")
    
    
    m.execute(
        f"/setblock {x-1} {y} {z-2} minecraft:oak_button[face=wall,facing=west,powered=false]"
    )
        
    m.execute(
        f"/fill {x} {y+1} {z-2} {x+len(unique_fencegates)//2} {y+1} {z-2} minecraft:redstone_wire"
    )

def generate_commands_1lap(unique_fencegates_laps, x, y, z):
    # Place the command block at the desired coordinates
    m.execute(
        f'/setblock {x} {y} {z} minecraft:command_block[conditional=false,facing=west]'
        '{Command:"kill @e[type=minecraft:block_display, tag=CP]"}'
    )
    m.execute(
        f"/setblock {x-1} {y} {z} minecraft:oak_button[face=wall,facing=west,powered=false]"
    )
    index = 0
    for lapnum, unique_fencegates in enumerate(unique_fencegates_laps):
        assert len(unique_fencegates) % 2 == 0
        for i in range(0, len(unique_fencegates), 2):
            I = i // 2
            FINISH_LINE = i == len(unique_fencegates) - 2
            f1 = unique_fencegates[i]
            f2 = unique_fencegates[i+1]
            bdc = get_block_display_command(f1, f2)
            m.execute(f'setblock {x+index} {y} {z-2} minecraft:command_block[conditional=false,facing=west]')
            m.execute(f"data modify block {x+index} {y} {z-2} Command set value '{bdc}'")

            sbc = get_cp_update_command(f1, f2, I+1+lapnum*100, I+2+lapnum*100 if not FINISH_LINE else 101+lapnum*100)
            m.execute(f'setblock {x+index} {y} {z+2} minecraft:repeating_command_block[conditional=false,facing=west]{{auto:1b}}')
            m.execute(f"data modify block {x+index} {y} {z+2} Command set value '{sbc}'")
            index += 1
    
    
    m.execute(
        f"/setblock {x-1} {y} {z-2} minecraft:oak_button[face=wall,facing=west,powered=false]"
    )
        
    m.execute(
        f"/fill {x} {y+1} {z-2} {x+index-1} {y+1} {z-2} minecraft:redstone_wire"
    )


def make_3_lap_course():
    last_text = pyperclip.paste()
    fencegate_pattern = re.compile(
        r"^/setblock (-?\d+) (-?\d+) (-?\d+) (.*)$"
    )
    diamond_pattern = re.compile(
        r"^/setblock (-?\d+) (-?\d+) (-?\d+) minecraft:diamond_block$"
    )

    unique_fencegates = []  # store unique fence gate coordinates

    lib.echo("Listening for F3+I presses")
    with m.EventQueue() as event_queue:
        event_queue.register_outgoing_chat_interceptor(pattern="undo")
        while True:
            try:
                event = event_queue.get(block=False)
                if len(unique_fencegates) > 0:
                    if len(unique_fencegates) % 2 == 1:
                        x,y,z=unique_fencegates.pop().split(",")
                        m.execute(f"execute positioned {x} {y} {z} run kill @e[type=minecraft:block_display,tag=CP,limit=1,sort=nearest]")
                    else:
                        x,y,z=unique_fencegates.pop().split(",")
                        unique_fencegates.pop()
                        m.execute(f"execute positioned {x} {y} {z} run kill @e[type=minecraft:block_display,tag=CP,limit=1,sort=nearest]")
            except m.queue.Empty:
                ...# m.echo("EMPTY")
            clipboard = pyperclip.paste()
            if clipboard != last_text:
                last_text = clipboard

                # Check for open fence gates
                fg_match = fencegate_pattern.search(clipboard)
                if fg_match:
                    x, y, z, block = fg_match.groups()
                    if "diamond" not in block:
                        coord_str = f"{x},{y},{z}"
                        if coord_str not in unique_fencegates:
                            unique_fencegates.append(coord_str)
                            print(f"New open fence gate detected: {coord_str}")
                            if (len(unique_fencegates) % 2 == 0):
                                cmd = get_block_display_command(unique_fencegates[-1], unique_fencegates[-2], "lime")
                                x,y,z=unique_fencegates[-2].split(",")
                                print(f"execute positioned {x} {y} {z} run kill @e[type=minecraft:block_display,tag=CP,limit=1,sort=nearest]")
                                m.execute(f"execute positioned {x} {y} {z} run kill @e[type=minecraft:block_display,tag=CP,limit=1,sort=nearest]")
                                m.execute(cmd)
                            else:
                                cmd = get_block_display_command(coord_str, coord_str, "yellow")
                                m.execute(cmd)

                # Check for diamond block
                diamond_match = diamond_pattern.search(clipboard)
                if diamond_match:
                    print("Diamond block detected!")
                    generate_commands(unique_fencegates, int(diamond_match.group(1)), int(diamond_match.group(2)), int(diamond_match.group(3)))
                    break  # stop the listener

            time.sleep(0.02)  # poll 10 times per second
        m.echo("ENDLOOP")

def make_1_lap_course():
    last_text = pyperclip.paste()
    fencegate_pattern = re.compile(
        r"^/setblock (-?\d+) (-?\d+) (-?\d+) (.*)$"
    )
    diamond_pattern = re.compile(
        r"^/setblock (-?\d+) (-?\d+) (-?\d+) minecraft:diamond_block$"
    )

    unique_fencegates = [[]]  # store unique fence gate coordinates

    lib.echo("Listening for F3+I presses")
    with m.EventQueue() as event_queue:
        event_queue.register_outgoing_chat_interceptor(pattern="undo|newlap")
        while True:
            try:
                event = event_queue.get(block=False)
                if event.message == "undo":
                    if len(unique_fencegates[-1]) > 0:
                        if len(unique_fencegates[-1]) % 2 == 1:
                            x,y,z=unique_fencegates[-1].pop().split(",")
                            m.execute(f"execute positioned {x} {y} {z} run kill @e[type=minecraft:block_display,tag=CP,limit=1,sort=nearest]")
                            lib.echo("Undid last half-checkpoint")
                        else:
                            x,y,z=unique_fencegates[-1].pop().split(",")
                            unique_fencegates[-1].pop()
                            m.execute(f"execute positioned {x} {y} {z} run kill @e[type=minecraft:block_display,tag=CP,limit=1,sort=nearest]")
                            lib.echo("Undid last checkpoint")
                    elif len(unique_fencegates[-1]) == 0 and len(unique_fencegates) > 1:
                        unique_fencegates.pop()
                        lib.echo("Undid newlap")
                else:
                    # New lap
                    lib.echo("Moving to next lap.")
                    unique_fencegates.append([])
            except m.queue.Empty:
                ...
            clipboard = pyperclip.paste()
            if clipboard != last_text:
                last_text = clipboard

                # Check for open fence gates
                fg_match = fencegate_pattern.search(clipboard)
                if fg_match:
                    x, y, z, block = fg_match.groups()
                    if "diamond" not in block:
                        coord_str = f"{x},{y},{z}"
                        if coord_str not in unique_fencegates[-1]:
                            unique_fencegates[-1].append(coord_str)
                            print(f"New open fence gate detected: {coord_str}")
                            if (len(unique_fencegates[-1]) % 2 == 0):
                                cmd = get_block_display_command(unique_fencegates[-1][-1], unique_fencegates[-1][-2], "lime")
                                x,y,z=unique_fencegates[-1][-2].split(",")
                                print(f"execute positioned {x} {y} {z} run kill @e[type=minecraft:block_display,tag=CP,limit=1,sort=nearest]")
                                m.execute(f"execute positioned {x} {y} {z} run kill @e[type=minecraft:block_display,tag=CP,limit=1,sort=nearest]")
                                m.execute(cmd)
                            else:
                                cmd = get_block_display_command(coord_str, coord_str, "yellow")
                                m.execute(cmd)

                # Check for diamond block
                diamond_match = diamond_pattern.search(clipboard)
                if diamond_match:
                    print("Diamond block detected!")
                    generate_commands_1lap(unique_fencegates, int(diamond_match.group(1)), int(diamond_match.group(2)), int(diamond_match.group(3)))
                    break  # stop the listener

            time.sleep(0.02)  # poll 10 times per second
        m.echo("ENDLOOP")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        make_1_lap_course()
    else:
        make_3_lap_course()