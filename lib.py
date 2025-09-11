import pyperclip
import time
import re
import minescript as m
import amulet_nbt
# import amulet_nbt as nbt
QUEUES_REGISTERED = False
def register_event_queues():
    echo("Registering lib")
    global EVENT_QUEUE
    global QUEUES_REGISTERED
    if not QUEUES_REGISTERED:
        EVENT_QUEUE = m.EventQueue()
        EVENT_QUEUE.register_chat_listener()
        EVENT_QUEUE.register_outgoing_chat_interceptor(pattern=".*")
        QUEUES_REGISTERED = True

def unregister_event_queues():
    echo("Unregistering lib")
    global QUEUES_REGISTERED
    if QUEUES_REGISTERED:
        global EVENT_QUEUE
        EVENT_QUEUE.unregister_all()
        del EVENT_QUEUE
        QUEUES_REGISTERED = False

F3C_PATTERN = re.compile(
    r"^/execute in minecraft:overworld run tp @s (-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)"
)

F3I_PATTERN = re.compile(
    r"^/setblock (-?\d+) (-?\d+) (-?\d+) (.*)$"
)
BLOCKSTRING_PATTERN = re.compile(
    r"^\s*([a-zA-Z0-9:_-]*)(\[.*?\])?(\{.*\})?\s*$"
)

def get_coords_from_clipboard(block = True):
    """Wait until clipboard has a valid F3+C string, then return (x, y, z, yaw, pitch)."""
    last = pyperclip.paste() if block else None
    while block or last is None:
        clip = pyperclip.paste()
        if clip != last:
            last = clip
            match = F3C_PATTERN.search(clip)
            print("testing")
            if match:
                print("match")
                x, y, z, yaw, pitch = map(float, match.groups())
                return (x, y, z, yaw, pitch)
        time.sleep(0.05)
    return None, None, None, None, None

def get_block_coords(filter=lambda x:True):
    """Wait until clipboard has a valid F3+I string, then return (x, y, z, blockstring)."""
    last = pyperclip.paste()
    while True:
        clip = pyperclip.paste()
        if clip != last:
            last = clip
            match = F3I_PATTERN.search(clip)
            if match:
                x, y, z, block = int(match.group(1)),int(match.group(2)),int(match.group(3)),match.group(4)
                if filter(block):
                    return (x, y, z, block)
        time.sleep(0.05)

def get_blockstring_components(blockstring:str) -> tuple[str, str, str]:
    x = BLOCKSTRING_PATTERN.match(blockstring)
    return x.group(1), x.group(2), x.group(3)

def wait_for_chat_message(pattern):
    register_event_queues()
    regex = re.compile(pattern)
    while True:
        try:
            event = EVENT_QUEUE.get(block=True)
            if event.type == m.EventType.OUTGOING_CHAT_INTERCEPT and regex.match(event.message):
                return event.message
        except m.queue.Empty:
            pass

def execute(x: str):
    if len(x) < 256:
        m.execute(x)
    else:
        time.sleep(1)
        m.execute("item replace entity 48panda weapon.mainhand with minecraft:command_block")
        m.execute("item replace entity 48panda weapon.offhand with minecraft:stone_button")
        m.echo("Place a command block and paste your clipboard into it and run it. Type 'done' when finished and ran.")
        pyperclip.copy(x)
        wait_for_chat_message("done")

def execute_get_result(cmd: str, filter, replace_nl = False):
    register_event_queues()
    m.execute(cmd)
    while True:
        event = EVENT_QUEUE.get()
        if event.type == m.EventType.CHAT:
            # m.echo("GOT", event.message)
            if not replace_nl:
                if filter(event.message):
                    return event.message
            else:
                if filter(event.message.replace("\n","")):
                    return event.message.replace("\n","")
        

STRING_GET_RE = re.compile("""^.*?has the following block data: ["'](.*)["']$""")

def get_command(x,y,z, filter):
    s = execute_get_result(f"data get block {x} {y} {z} Command", lambda s:STRING_GET_RE.match(s) and filter(STRING_GET_RE.match(s).group(1)))
    return STRING_GET_RE.match(s).group(1)

SCORE_RE = re.compile("""^.*? has (-?[0-9]+) \\[.*\\]$""")

def get_score(selector, scoreboard):
    s = execute_get_result(f"scoreboard players get {selector} {scoreboard}", lambda s:SCORE_RE.match(s) or s.startswith("Can't get value of"))
    return SCORE_RE.match(s).group(1) if SCORE_RE.match(s) else None

GET_POS = re.compile("""^.*? has the following entity data: (-?[0-9.]+)d$""")

def get_double(selector, path):
    s = execute_get_result(f"data get entity {selector} {path}", lambda s:GET_POS.match(s))
    return GET_POS.match(s).group(1)

def is_entity(selector):
    return test(f"execute if entity {selector}")
def count_entity(selector):
    execute_get_result(f"execute if entity {selector}", lambda x: x.startswith("Test"))

def test(cmd):
    return "failed" not in execute_get_result(cmd, lambda x: x.startswith("Test"))

def is_track(index):
    return test(f"execute if block {170+index*2} -60 -25 command_block")

GET_INT_RE = re.compile("^.* has the following contents: ([0-9]+)$")

def get_new_cut_id():
    s = execute_get_result("data get storage var NextCutId", GET_INT_RE.match)
    id=int(GET_INT_RE.match(s).group(1))
    execute(f"data modify storage var NextCutId set value {id+1}")
    return id

def echo(*msg):
    cmd = f"""tellraw @s {{"text":"{" ".join(map(str, msg)).replace("\"","\\\"")}","color":"green"}}"""
    if len(cmd) > 250:
        m.echo(*msg)
    else:
        m.execute(cmd)

NBT_REGEX = re.compile("^.*? has the following entity data: (.*)$")

def get_entity_nbt(selector: str, path: str | None = None) -> amulet_nbt.AnyNBT:
    if path is None:
        return amulet_nbt.from_snbt(NBT_REGEX.match(execute_get_result(f"data get entity {selector}", NBT_REGEX.match)).group(1))
    else:
        return amulet_nbt.from_snbt(NBT_REGEX.match(execute_get_result(f"data get entity {selector} {path}", NBT_REGEX.match)).group(1))