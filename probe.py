import lib
import re


TP_RE = re.compile(r"^tp @a\[tag=RaceStart\] (.*)$")
NAME_RE = re.compile(r"^title @a\[tag=RaceStart\] title \"(.*)\"$")
TIME_RE = re.compile("^time set (.*)$")
WEATHER_RE = re.compile("weather (.*) 1d")
GATE_RE = re.compile("^fill (-?[0-9]+ -?[0-9]+ -?[0-9]+ -?[0-9]+ -?[0-9]+ -?[0-9]+) (.*)$")
CUTSCENE_RE = re.compile("^scoreboard players set \\$TRACK VAR (.*)$")
MUSIC_RE = re.compile("^setblock.*redstone_block$")

# def probe(index):
#     x = 170 + index*2
#     # x, index, tp_command, name, time_of_day, weather_type, gate_coords, b, music_command,
#     #              cutscene_index
#     tp_command=TP_RE.match(lib.get_command(x,-60,-25, TP_RE.match)).group(1)
#     name=NAME_RE.match(lib.get_command(x,-60,-28, NAME_RE.match)).group(1)
#     time_of_day = TIME_RE.match(lib.get_command(x, -59, -27, TIME_RE.match)).group(1)
#     weather_type = WEATHER_RE.match(lib.get_command(x, -59, -26, WEATHER_RE.match)).group(1)
#     gate_coords, b = GATE_RE.match(lib.get_command(x, -60, -33, GATE_RE.match)).groups()
#     music_command = lib.get_command(x,-60,-67, MUSIC_RE.match)
#     cutscene_index = CUTSCENE_RE.match(lib.get_command(x, -59, -28, CUTSCENE_RE.match)).group(1)
#     return tp_command,name,time_of_day, weather_type, gate_coords, b, music_command, cutscene_index

def probe_name(index):
    nbt = lib.get_storage_nbt("tracks", f"TrackData[{index}].Name")
    return nbt.py_str if nbt is not None else None
def probe_cutscene_index(index):
    return lib.get_storage_nbt("tracks", f"TrackData[{index}].id").py_int
def probe_tp_command(index):
    nbt = lib.get_storage_nbt("tracks", f"TrackData[{index}].StartPos")
    return f"{nbt.get_double("x").py_float} {nbt.get_double("y").py_float} {nbt.get_double("z").py_float} {nbt.get_float("yaw").py_float} {nbt.get_float("pitch").py_float}"

def cutscene_index_from_name(name: str) -> int | None:
    return probe_cutscene_index(index_from_name(name))

def index_from_name(name: str) -> int | None:
    start_name = re.sub("[^a-z]","",name.lower())
    possible_tracks:"list[tuple[int, str]]" = []
    i = 0
    while True:
            name = probe_name(i)
            if name is None:
                break
            if re.sub("[^a-z]","",name.lower()).startswith(start_name):
                possible_tracks.append((i, name))
            i += 1
    if len(possible_tracks) == 0:
        lib.echo("No tracks with that name found")
    elif len(possible_tracks) > 1:
        lib.echo("Too many tracks start with that. Possible tracks:")
        for i,v in possible_tracks:
            lib.echo(v)
    else:
        return possible_tracks[0][0]
    return None

def name_from_name(name: str) -> str | None:
    return probe_name(index_from_name(name))