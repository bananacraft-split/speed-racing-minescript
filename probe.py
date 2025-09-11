import lib
import re


TP_RE = re.compile(r"^tp @a\[tag=RaceStart\] (.*)$")
NAME_RE = re.compile(r"^title @a\[tag=RaceStart\] title \"(.*)\"$")
TIME_RE = re.compile("^time set (.*)$")
WEATHER_RE = re.compile("weather (.*) 1d")
GATE_RE = re.compile("^fill (-?[0-9]+ -?[0-9]+ -?[0-9]+ -?[0-9]+ -?[0-9]+ -?[0-9]+) (.*)$")
CUTSCENE_RE = re.compile("^scoreboard players set \\$TRACK VAR (.*)$")
MUSIC_RE = re.compile("^setblock.*redstone_block$")

def probe(index):
    x = 170 + index*2
    # x, index, tp_command, name, time_of_day, weather_type, gate_coords, b, music_command,
    #              cutscene_index
    tp_command=TP_RE.match(lib.get_command(x,-60,-25, TP_RE.match)).group(1)
    name=NAME_RE.match(lib.get_command(x,-60,-28, NAME_RE.match)).group(1)
    time_of_day = TIME_RE.match(lib.get_command(x, -59, -27, TIME_RE.match)).group(1)
    weather_type = WEATHER_RE.match(lib.get_command(x, -59, -26, WEATHER_RE.match)).group(1)
    gate_coords, b = GATE_RE.match(lib.get_command(x, -60, -33, GATE_RE.match)).groups()
    music_command = lib.get_command(x,-60,-67, MUSIC_RE.match)
    cutscene_index = CUTSCENE_RE.match(lib.get_command(x, -59, -28, CUTSCENE_RE.match)).group(1)
    return tp_command,name,time_of_day, weather_type, gate_coords, b, music_command, cutscene_index

def probe_name(index):
    return NAME_RE.match(lib.get_command(170 + index*2,-60,-28, NAME_RE.match)).group(1)
def probe_cutscene_index(index):
    return CUTSCENE_RE.match(lib.get_command(170 + index*2, -59, -28, CUTSCENE_RE.match)).group(1)
def probe_tp_command(index):
    return TP_RE.match(lib.get_command(170 + index*2,-60,-25, TP_RE.match)).group(1)

def cutscene_index_from_name(name: str) -> int | None:
    start_name = re.sub("[^a-z]","",name.lower())
    possible_tracks:"list[tuple[int, str]]" = []
    for i in range(50):
        if lib.is_track(i):
            name = probe_name(i)
            if re.sub("[^a-z]","",name.lower()).startswith(start_name):
                possible_tracks.append((probe_cutscene_index(i), name))
    if len(possible_tracks) == 0:
        lib.echo("No tracks with that name found")
    elif len(possible_tracks) > 1:
        lib.echo("Too many tracks start with that. Possible tracks:")
        for i,v in possible_tracks:
            lib.echo(v)
    else:
        return possible_tracks[0][0]
    return None

def index_from_name(name: str) -> int | None:
    start_name = re.sub("[^a-z]","",name.lower())
    possible_tracks:"list[tuple[int, str]]" = []
    for i in range(50):
        if lib.is_track(i):
            name = probe_name(i)
            if re.sub("[^a-z]","",name.lower()).startswith(start_name):
                possible_tracks.append((i, name))
    if len(possible_tracks) == 0:
        lib.echo("No tracks with that name found")
    elif len(possible_tracks) > 1:
        lib.echo("Too many tracks start with that. Possible tracks:")
        for i,v in possible_tracks:
            lib.echo(v)
    else:
        return possible_tracks[0][0]
    return None

def name_from_name(name: str) -> int | None:
    start_name = re.sub("[^a-z]","",name.lower())
    possible_tracks:"list[str]" = []
    for i in range(50):
        if lib.is_track(i):
            name = probe_name(i)
            if re.sub("[^a-z]","",name.lower()).startswith(start_name):
                possible_tracks.append(name)
    if len(possible_tracks) == 0:
        lib.echo("No tracks with that name found")
    elif len(possible_tracks) > 1:
        lib.echo("Too many tracks start with that. Possible tracks:")
        for i,v in possible_tracks:
            lib.echo(v)
    else:
        return possible_tracks[0]
    return None