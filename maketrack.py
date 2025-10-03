import lib
import makecp2
import makelb
import minescript as m
from enum import Enum
import time
import cutscene

import wire

class STAGE(Enum):
    FIRST_POLE_SELECT = 1
    SECOND_POLE_SELECT = 2
    GATE_BLOCK_SELECT = 3
    GATE_CONFIRM = 4
    CREATE_TP_LOCATION = 5
    CHOOSE_NAME = 6
    CONFIRM_NAME = 7
    CHOOSE_MUSIC_LOCATION = 8
    CONFIRM_MUSIC_LOCATION = 9
    CHOOSE_MUSIC = 10
    SET_TIME = 11
    CONFIRM_TIME = 12
    SET_WEATHER = 13
    CONFIRM_WEATHER = 14
    SET_CUP = 15
    SET_TRACK = 16
    CONFIRM_CUP_TRACK = 17
    CREATE_TRACK = 18
    CREATE_CUT = 19
    PLAY_CUT = 20
    CONFIRM_CUT = 21
    DELETE_CUT = 22
    SET_CHECK_SIZE = 23
    CHECK_INSTR = 24
    CHECK_MAKE = 25
    LB_MAKE = 26
    LB_CONFIRM = 27
NUM_STEPS = 26


def wrap_on_sign(text: str) -> list[str]:
    """
    Wraps text for a Minecraft sign.
    - Each sign has 4 lines.
    - Each line up to 15 characters.
    - Breaks long words if needed.
    Returns a list of up to 4 strings.
    """
    max_width = 15
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        # If the word itself is too long, break it into chunks
        while len(word) > max_width:
            if current_line:
                lines.append(current_line)
                current_line = ""
            lines.append(word[:max_width])
            word = word[max_width:]

        # Try to add the (possibly shortened) word to the current line
        if len(current_line) + len(word) + (1 if current_line else 0) <= max_width:
            current_line += (" " if current_line else "") + word
        else:
            lines.append(current_line)
            current_line = word

    # Add last line if not empty
    if current_line:
        lines.append(current_line)

    # Limit to 4 lines
    return lines[:4]

lib.echo("Track Creation started.")

step = STAGE.FIRST_POLE_SELECT

def create_track(index, tp_command, name, time_of_day, weather_type, gate_coords, b, music_command,
                 cutscene_index):
    x = 170 + index*2
    if "command_block" in m.getblock(x, -60, -25):
        lib.echo("Track in use. Choose another track.")
        return False
    wire.fill_block(x, -58, -14, x, -58, -65, index)
    lib.execute(f"fill {x} -57 -14 {x} -57 -65 redstone_wire")
    lib.execute(f"setblock {x} -57 -14 minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    wire.place_block(x, -56, -20, index)
    lib.execute(f"setblock {x} -56 -19 minecraft:oak_wall_sign[facing=south,waterlogged=false]")
    for i,v in enumerate(wrap_on_sign(name)):
        lib.execute(f"data modify block {x} -56 -19 front_text.messages[{i}] set value '{{\"text\":\"{v}\"}}'")
    lib.execute(f"setblock {x} -60 -22 minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    lib.execute(f"setblock {x} -58 -23 minecraft:sticky_piston[extended=false,facing=down]")
    lib.execute(f"setblock {x} -60 -24 minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    wire.place_block(x, -59, -23, index)
    lib.execute(f"setblock {x} -57 -30 minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    lib.execute(f"setblock {x} -60 -30 minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    lib.execute(f"setblock {x} -58 -31 minecraft:sticky_piston[extended=false,facing=down]")
    lib.execute(f"setblock {x} -60 -32 minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    wire.place_block(x, -59, -31, index)
    lib.execute(f"setblock {x} -60 -40 minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    lib.execute(f"setblock {x} -58 -41 minecraft:sticky_piston[extended=false,facing=down]")
    lib.execute(f"setblock {x} -60 -42 minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    lib.execute(f"setblock {x} -57 -46 minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    wire.place_block(x, -59, -41, index)
    lib.execute(f"setblock {x} -60 -52 minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    lib.execute(f"setblock {x} -58 -53 minecraft:sticky_piston[extended=false,facing=down]")
    lib.execute(f"setblock {x} -60 -54 minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    wire.place_block(x, -59, -53, index)
    lib.execute(f"setblock {x} -57 -61 minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    lib.execute(f"setblock {x} -60 -64 minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    lib.execute(f"setblock {x} -58 -65 minecraft:sticky_piston[extended=false,facing=down]")
    lib.execute(f"setblock {x} -60 -66 minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    wire.place_block(x, -59, -65, index)

    lib.execute(f"setblock {x} -58 -15 minecraft:command_block[conditional=false,facing=north]{{TrackOutput:0b,auto:0b}}")
    lib.execute(f"data modify block {x} -58 -15 Command set value \"tellraw @a \\\"Track Selected: {name}\\\"\"")

    lib.execute(f"setblock {x} -60 -25 minecraft:command_block[conditional=false,facing=north]{{TrackOutput:0b,auto:0b}}")
    lib.execute(f"data modify block {x} -60 -25 Command set value \"tp @a[tag=RaceStart] {tp_command}\"")
    lib.execute(f"setblock {x} -60 -26 minecraft:chain_command_block[conditional=false,facing=north]{{TrackOutput:0b,auto:1b}}")
    lib.execute(f"data modify block {x} -60 -26 Command set value \"execute as @a[scores={{TRACK={cutscene_index}}}] run scoreboard players set @s TRACK 0\"")
    lib.execute(f"setblock {x} -60 -27 minecraft:chain_command_block[conditional=false,facing=north]{{TrackOutput:0b,auto:1b}}")
    lib.execute(f"data modify block {x} -60 -27 Command set value \"execute as @a[tag=RaceStart] run scoreboard players set @s TRACK {cutscene_index}\"")
    lib.execute(f"setblock {x} -60 -28 minecraft:chain_command_block[conditional=false,facing=up]{{TrackOutput:0b,auto:1b}}")
    lib.execute(f"data modify block {x} -60 -28 Command set value \"title @a[tag=RaceStart] title \\\"{name}\\\"\"")
    lib.execute(f"setblock {x} -59 -28 minecraft:chain_command_block[conditional=false,facing=south]{{TrackOutput:0b,auto:1b}}")
    lib.execute(f"data modify block {x} -59 -28 Command set value \"scoreboard players set $TRACK VAR {cutscene_index}\"")
    lib.execute(f"setblock {x} -59 -27 minecraft:chain_command_block[conditional=false,facing=south]{{TrackOutput:0b,auto:1b}}")
    lib.execute(f"data modify block {x} -59 -27 Command set value \"time set {time_of_day}\"")
    lib.execute(f"setblock {x} -59 -26 minecraft:chain_command_block[conditional=false,facing=south]{{TrackOutput:0b,auto:1b}}")
    lib.execute(f"data modify block {x} -59 -26 Command set value \"weather {weather_type} 1d\"")

    lib.execute(f"setblock {x} -60 -43 minecraft:command_block[conditional=false,facing=up]{{TrackOutput:0b,auto:0b}}")
    lib.execute(f"data modify block {x} -60 -43 Command set value \"tp @a[tag=RaceStart] {tp_command}\"")

    lib.execute(f"setblock {x} -60 -33 minecraft:command_block[conditional=false,facing=up]{{TrackOutput:0b,auto:0b}}")
    lib.execute(f"data modify block {x} -60 -33 Command set value \"fill {gate_coords} {b}\"")

    lib.execute(f"setblock {x} -60 -55 minecraft:command_block[conditional=false,facing=up]{{TrackOutput:0b,auto:0b}}")
    lib.execute(f"data modify block {x} -60 -55 Command set value \"fill {gate_coords} air\"")

    lib.execute(f"setblock {x} -60 -67 minecraft:command_block[conditional=false,facing=up]{{TrackOutput:0b,auto:0b}}")
    lib.execute(f"data modify block {x} -60 -67 Command set value \"{music_command}\"")
    return True

if __name__ == "__main__":
    while True:
        lib.echo(f"Step {step.value}/{NUM_STEPS}")
        match step:
            case STAGE.FIRST_POLE_SELECT:
                lib.echo("Press F3+I whilst looking at the left-hand finish line pole at eye level.")
                x1,y1,z1,_ = lib.get_block_coords()
                step = STAGE.SECOND_POLE_SELECT
            case STAGE.SECOND_POLE_SELECT:
                lib.echo("Press F3+I whilst looking at the right-hand finish line pole at eye level.")
                x2,y2,z2,_ = lib.get_block_coords()
                if y1 != y2:
                    lib.echo("ERROR. Finish line gate must be one block high")
                    step = STAGE.FIRST_POLE_SELECT
                    continue
                if x1 != x2 and z1 != z2:
                    lib.echo("ERROR. Finish line gate must be a straight line")
                    step = STAGE.FIRST_POLE_SELECT
                    continue
                if x1 == x2 and z1 == z2:
                    lib.echo("ERROR. The two selected blocks cannot be the same")
                    step = STAGE.FIRST_POLE_SELECT
                    continue
                if x1 == x2:
                    if abs(z1 - z2) < 2:
                        lib.echo("ERROR. Gate too small")
                        step = STAGE.FIRST_POLE_SELECT
                        continue
                    if z1 > z2:
                        gate_coords = f"{x1} {y1} {z1 - 1} {x1} {y1} {z2 + 1}"
                    else:
                        gate_coords = f"{x1} {y1} {z1 + 1} {x1} {y1} {z2 - 1}"
                if z1 == z2:
                    if abs(x1 - x2) < 2:
                        lib.echo("ERROR. Gate too small")
                        step = STAGE.FIRST_POLE_SELECT
                        continue
                    if x1 > x2:
                        gate_coords = f"{x1 - 1} {y1} {z1} {x2 + 1} {y1} {z1}"
                    else:
                        gate_coords = f"{x1 + 1} {y1} {z1} {x2 - 1} {y1} {z1}"
                assert gate_coords
                step = STAGE.GATE_BLOCK_SELECT
            case STAGE.GATE_BLOCK_SELECT:
                lib.echo("Press F3+I whilst looking at the block you would like the finish line to be made of.")
                _,_,_,b = lib.get_block_coords()
                lib.echo(b)
                step = STAGE.GATE_CONFIRM
            case STAGE.GATE_CONFIRM:
                lib.execute(f"fill {gate_coords} {b}")
                lib.echo("Is this the start line gate you want? Type yes or no.")
                if lib.wait_for_chat_message("(yes|no)") == "yes":
                    step = STAGE.CREATE_TP_LOCATION
                else:
                    step = STAGE.FIRST_POLE_SELECT
                lib.execute(f"fill {gate_coords} air")
            case STAGE.CREATE_TP_LOCATION:
                lib.echo("Creating spawn location....")
                dx = z1 - z2
                dz = x2 - x1
                assert dx == 0 or dz == 0
                L = abs(dx + dz)
                X = (x1+x2)/2 + 3 * dx/L + 0.5
                Z = (z1+z2)/2 + 3 * dz/L + 0.5
                lib.echo(dx, dz)
                if dx == 0 and dz < 0:
                    dir = 0
                if dx < 0 and dz == 0:
                    dir = -90
                if dx == 0 and dz > 0:
                    dir = 180
                if dx > 0 and dz == 0:
                    dir = 90
                tp_command =f"{X:.2f} {y1 - 0.8} {Z:.2f} {dir} 0"
                tp_x = f"{X:.2f}d"
                tp_y = f"{y1-0.8}d"
                tp_z = f"{Z:.2f}d"
                tp_yaw = f"{dir}d"
                tp_pitch = "0d"
                lib.echo(tp_command)
                lib.execute("tp @s "+tp_command)
                step = STAGE.CHOOSE_NAME
            case STAGE.CHOOSE_NAME:
                lib.echo("Type the name of the track into chat.")
                name = lib.wait_for_chat_message(".*").strip()
                if "\"" in name or "\\" in name:
                    lib.echo("Invalid character found.")
                else:
                    step = STAGE.CONFIRM_NAME
            case STAGE.CONFIRM_NAME:
                lib.echo(f"The name of the track is \"{name}\". Type yes/no to confirm.")
                if lib.wait_for_chat_message("(yes|no)") == "yes":
                    step = STAGE.CHOOSE_MUSIC_LOCATION
                else:
                    step = STAGE.CHOOSE_NAME
            case STAGE.CHOOSE_MUSIC_LOCATION:
                lib.echo(f"Choose where the music machine should be. Press F3+I on the block on the floor where you want it to be.")
                mx, my, mz, _ = lib.get_block_coords()
                m.execute(f'setblock {mx} {my} {mz} minecraft:jukebox')
                m.execute(f'setblock {mx} {my+1} {mz} minecraft:chest')
                step = STAGE.CONFIRM_MUSIC_LOCATION
            case STAGE.CONFIRM_MUSIC_LOCATION:
                lib.echo(f"Are you happy with the location of the music machine? Type yes/no to confirm.")
                if lib.wait_for_chat_message("(yes|no)") == "yes":
                    step = STAGE.CHOOSE_MUSIC
                else:
                    step = STAGE.CHOOSE_MUSIC_LOCATION
                    m.execute(f'setblock {mx} {my} {mz} air')
                    m.execute(f'setblock {mx} {my+1} {mz} air')
                time.sleep(0.5)
            case STAGE.CHOOSE_MUSIC:
                lib.echo(f"Please hold the music disc to use for this track in your MAIN HAND. Type 'done when finished'.")
                lib.wait_for_chat_message("done")
                m.execute(f"data modify block {mx} {my+1} {mz} Items append from storage minecraft:options StartMusic")
                m.execute(f"item replace block {mx} {my+1} {mz} container.1 from entity @s weapon.mainhand")
                step=STAGE.SET_TIME
            case STAGE.SET_TIME:
                lib.echo("Set the time to the time you want it to be. Type 'done' when finished")
                lib.wait_for_chat_message("done")
                time_of_day = m.world_info().day_ticks
                step = STAGE.CONFIRM_TIME
            case STAGE.CONFIRM_TIME:
                lib.echo(f"The time for the track is \"{time_of_day}\". Type yes/no to confirm.")
                if lib.wait_for_chat_message("(yes|no)") == "yes":
                    step = STAGE.SET_WEATHER
                else:
                    step = STAGE.SET_TIME
            case STAGE.SET_WEATHER:
                lib.echo("Would you like the weather to be 'clear', 'rain', or 'thunder'?")
                weather_type = lib.wait_for_chat_message("clear|rain|thunder")
                step = STAGE.CONFIRM_WEATHER
            case STAGE.CONFIRM_WEATHER:
                lib.echo(f"The weather for the track is \"{weather_type}\". Type yes/no to confirm.")
                if lib.wait_for_chat_message("(yes|no)") == "yes":
                    step = STAGE.SET_CUP
                else:
                    step = STAGE.SET_WEATHER
            case STAGE.SET_CUP:
                lib.echo(f"Which cup would you like this to be in? Type a number. 1 is dirt cup.")
                cup = int(lib.wait_for_chat_message("[1-9][0-9]*"))
                step = STAGE.SET_TRACK
            case STAGE.SET_TRACK:
                lib.echo(f"Which track would you like this to be in? Type a number. 1-4")
                track = int(lib.wait_for_chat_message("[1234]"))
                step = STAGE.CONFIRM_CUP_TRACK
            case STAGE.CONFIRM_CUP_TRACK:
                lib.echo(f"Selected: Cup {cup} Track {track}. Type yes/no to confirm.")
                if lib.wait_for_chat_message("(yes|no)") == "yes":
                    step = STAGE.CREATE_TRACK
                else:
                    step = STAGE.SET_CUP
            case STAGE.CREATE_TRACK:
                cutscene_id = lib.get_new_cut_id()
                m.execute("data modify storage tracks TrackData append value {new:1b}")
                if weather_type == "clear":
                    lib.execute("data modify storage tracks TrackData[{new:1b}].Weather.Clear set value 1b")
                if weather_type == "rain":
                    lib.execute("data modify storage tracks TrackData[{new:1b}].Weather.Rain set value 1b")
                if weather_type == "thunder":
                    lib.execute("data modify storage tracks TrackData[{new:1b}].Weather.Thunder set value 1b")
                lib.execute("data modify storage tracks TrackData[{new:1b}].StartPos.x set value " + tp_x+"d")
                lib.execute("data modify storage tracks TrackData[{new:1b}].StartPos.y set value " + tp_y+"d")
                lib.execute("data modify storage tracks TrackData[{new:1b}].StartPos.z set value " + tp_z+"d")
                lib.execute("data modify storage tracks TrackData[{new:1b}].StartPos.yaw set value " + tp_yaw+"f")
                lib.execute("data modify storage tracks TrackData[{new:1b}].StartPos.pitch set value " + tp_pitch+"f")
                lib.execute("data modify storage tracks TrackData[{new:1b}].DayTime set value " + str(time_of_day))
                lib.execute("data modify storage tracks TrackData[{new:1b}].Gate.Destroy set value " + f'"fill {gate_coords} air"')
                lib.execute("data modify storage tracks TrackData[{new:1b}].Gate.Make set value " + f'"fill {gate_coords} {b.replace("\\","\\\\").replace("\"","\\\"")}"')
                lib.execute("data modify storage tracks TrackData[{new:1b}].id set value " + str(cutscene_id))
                lib.execute("data modify storage tracks TrackData[{new:1b}].Name set value " + "\"" + name + "\"")
                lib.execute("data modify storage tracks TrackData[{new:1b}].Music.x set value " + str(mx))
                lib.execute("data modify storage tracks TrackData[{new:1b}].Music.y set value " + str(my))
                lib.execute("data modify storage tracks TrackData[{new:1b}].Music.z set value " + str(mz))
                lib.execute("data remove storage tracks TrackData[{new:1b}].new")
                # created = create_track(
                #     index, tp_command, name, time_of_day, weather_type,
                #     gate_coords, b, music_command, cutscene_id
                # )
                time.sleep(3)
                step = STAGE.CREATE_CUT
                lib.execute(f"tp @s {tp_command}")
            case STAGE.CREATE_CUT:
                pts = cutscene.make_cutscene(cutscene_id, tp_command)
                step = STAGE.PLAY_CUT
            case STAGE.PLAY_CUT:
                lib.execute("tag @s add CutTest")
                lib.execute(f"scoreboard players set $TRACK VAR {cutscene_id}")
                lib.execute(f"scoreboard players set $CUT2 VAR 0")
                time.sleep(12)
                lib.execute("tag @s remove CutTest")
                time.sleep(1)
                lib.echo("Is this cutscene good? Type yes/no to confirm.")
                if lib.wait_for_chat_message("(yes|no)") == "yes":
                    step = STAGE.CONFIRM_CUT
                else:
                    step = STAGE.DELETE_CUT
            case STAGE.DELETE_CUT:
                for i in pts:
                    lib.execute(f"tp @s {" ".join(map(str, i))}")
                    time.sleep(1)
                    lib.execute(f"kill @e[tag=GKT]")
                    time.sleep(0.2)
                step = STAGE.CREATE_CUT
                m.execute(f"gamemode creative")
            case STAGE.CONFIRM_CUT:
                for i in pts:
                    lib.execute(f"tp @s {" ".join(map(str, i))}")
                    time.sleep(1)
                    lib.execute(f"\\finishcut")
                    time.sleep(0.2)
                lib.echo("Finished cutscene!")
                m.execute(f"gamemode creative")
                step = STAGE.SET_CHECK_SIZE
            case STAGE.SET_CHECK_SIZE:
                lib.echo("Would you like this to be a 1 lap track or a 3 lap track? (e.g. Tracks such as Savannah Sprint and Problematic Processing are 1 lap tracks, most others are 3 laps.)")
                num_laps = lib.wait_for_chat_message("[13]")
                step = STAGE.CHECK_INSTR
            case STAGE.CHECK_INSTR:
                if num_laps == "3":
                    lib.echo("Use F3+I to select two blocks to make the checkpoints between. Start at the first checkpoint after the start line and work around the track in the order players will traverse.")
                    lib.echo("Ensure that no shortcuts can skip any checpoint area, and that each checkpoint covers the whole track and is at least 3 blocks deep. Faliure to do this may result in some laps not counting.")
                    lib.echo("The last checkpoint you do will be the finish.")
                    lib.echo("When you're done, go to an area outside the track and F3+I on a diamond block to create the command blocks needed.")
                    lib.echo("NOTE: For larger tracks you may need to forceload the chunks containing the command blocks for it to work properly.")
                    lib.echo("Typing undo will undo your last action.")
                    step = STAGE.CHECK_MAKE
                elif num_laps == "1":
                    lib.echo("Use F3+I to select two blocks to make the checkpoints between. Start at the first checkpoint after the start line and work around the track in the order players will traverse.")
                    lib.echo("Ensure that no shortcuts can skip any checpoint area, and that each checkpoint covers the whole track and is at least 3 blocks deep. Faliure to do this may result in some laps not counting.")
                    lib.echo("To mark a new lap, type \"newlap\" into chat AFTER marking the finish line for that lap.")
                    lib.echo("When you're done, go to an area outside the track and F3+I on a diamond block to create the command blocks needed.")
                    lib.echo("NOTE: For larger tracks you may need to forceload the chunks containing the command blocks for it to work properly.")
                    lib.echo("Typing \"undo\" into chat will undo your last action.")
                    step = STAGE.CHECK_MAKE
                else:
                    step = STAGE.SET_CHECK_SIZE
            case STAGE.CHECK_MAKE:
                if num_laps == "3":
                    makecp2.make_checkpoints_3_lap(cutscene_id)
                    step = STAGE.LB_MAKE
                if num_laps == "1":
                    makecp2.make_checkpoints_1_lap(cutscene_id)
                    step = STAGE.LB_MAKE
            case STAGE.LB_MAKE:
                time.sleep(2)
                lib.execute("execute in minecraft:overworld run tp @s 198.49 -60.00 28.79 -1170.49 16.60")
                lib.echo("Use F3+I to select the block you want the leaderboard to be on.")
                lib.echo("DO NOT SELECT THE WALL SELECT THE FLOOR IN FRONT OF THE WALL.")
                x,y,z,_ = lib.get_block_coords()
                makelb.make_leaderboard(cutscene_id,x,y,z,name)
                lib.echo("You have successfully created a track! Just link up the wires and you're good to go!")
                break