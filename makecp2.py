import pyperclip
import data
import lib
import math
import minescript as m
import time

COLORS = ["red", "orange", "yellow", "lime", "light_blue", "pink", "purple"]

# Convert yaw/pitch to forward vector
def get_forward(pitch: float, yaw: float):
    yaw_rad = math.radians(-yaw)
    pitch_rad = math.radians(pitch)
    print(yaw_rad, pitch_rad)
    dx = math.cos(pitch_rad) * math.sin(yaw_rad)
    dy = -math.sin(pitch_rad)
    dz = math.cos(pitch_rad) * math.cos(yaw_rad)
    return (dx, dy, dz)

def make_checkpoint_marker(x, y, z, dx, dy, dz, CP, OLDCP, cutscene_index,path=None):
    lib.execute(f'summon marker {x:.2f} {y:.2f} {z:.2f} {{Tags:["CPM","newcpm"]}}')
    A  = round(dx * 100)
    B  = round(dy * 100)
    C  = round(dz * 100)
    D = round(- 10000 * (A * x + B * y + C * z))
    lib.execute(f'scoreboard players set @e[tag=CPM,tag=newcpm] X {A}')
    lib.execute(f'scoreboard players set @e[tag=CPM,tag=newcpm] Y {B}')
    lib.execute(f'scoreboard players set @e[tag=CPM,tag=newcpm] Z {C}')
    lib.execute(f'scoreboard players set @e[tag=CPM,tag=newcpm] W {D}')
    lib.execute(f'scoreboard players set @e[tag=CPM,tag=newcpm] TRACK {cutscene_index}')
    lib.execute(f'scoreboard players set @e[tag=CPM,tag=newcpm] CP {CP}')
    lib.execute(f'scoreboard players set @e[tag=CPM,tag=newcpm] OLDCP {OLDCP}')
    if path is not None: 
        lib.execute(f'scoreboard players set @e[tag=CPM,tag=newcpm] PATH {path}')
    lib.execute("tag @e[tag=CPM,tag=newcpm] remove newcpm")

def make_checkpoint_markers_3_lap(checkpoints: list[tuple[float, float, float, float, float, float]], cutscene_index):
    for i, v in enumerate(checkpoints):
        LAST_CP = i + 1 == len(checkpoints)
        x,y,z,dx,dy,dz = v
        lib.execute(f"tp @s {x:.2f} {y:.2f} {z:.2f}")
        make_checkpoint_marker(x,y,z,dx,dy,dz,101 if LAST_CP else i + 2, i + 1, cutscene_index)
        make_checkpoint_marker(x,y,z,dx,dy,dz,201 if LAST_CP else i + 102, i + 101, cutscene_index)
        make_checkpoint_marker(x,y,z,dx,dy,dz,301 if LAST_CP else i + 202, i + 201, cutscene_index)
        if LAST_CP:
            make_checkpoint_marker(x,y,z,dx,dy,dz,1, 0, cutscene_index)

def make_checkpoint_markers_3_lap_with_split(checkpoints: list[tuple[float, float, float, float, float, float]], cutscene_index):
    for i, v in enumerate(checkpoints):
        LAST_CP = i + 1 == len(checkpoints)
        IS_SPLIT = len(v) > 1
        for path, cp in enumerate(v):
            x,y,z,dx,dy,dz = cp
            lib.execute(f"tp @s {x:.2f} {y:.2f} {z:.2f}")
            make_checkpoint_marker(x,y,z,dx,dy,dz,101 if LAST_CP else i + 2, i + 1, cutscene_index, path=path+1 if IS_SPLIT else None)
            make_checkpoint_marker(x,y,z,dx,dy,dz,201 if LAST_CP else i + 102, i + 101, cutscene_index, path=path+1 if IS_SPLIT else None)
            make_checkpoint_marker(x,y,z,dx,dy,dz,301 if LAST_CP else i + 202, i + 201, cutscene_index, path=path+1 if IS_SPLIT else None)
            if LAST_CP:
                make_checkpoint_marker(x,y,z,dx,dy,dz,1, 0, cutscene_index)

def make_checkpoint_markers_1_lap(checkpoints: list[list[tuple[float, float, float, float, float, float]]], cutscene_index):
    assert len(checkpoints) == 3
    for LAPNUM, lap_checkpoints in enumerate(checkpoints):
        for i, v in enumerate(lap_checkpoints):
            LAST_CP = i + 1 == len(lap_checkpoints)
            x,y,z,dx,dy,dz = v
            lib.execute(f"tp @s {x:.2f} {y:.2f} {z:.2f}")
            time.sleep(0.5)
            if LAPNUM == 0:
                make_checkpoint_marker(x,y,z,dx,dy,dz,LAPNUM * 100 + 101 if LAST_CP else i + LAPNUM * 100 + 1, i + LAPNUM * 100 + 0, cutscene_index)
            else:
                make_checkpoint_marker(x,y,z,dx,dy,dz,LAPNUM * 100 + 101 if LAST_CP else i + LAPNUM * 100 + 2, i + LAPNUM * 100 + 1, cutscene_index)

        
def make_checkpoints_3_lap(cutscene_index):
    lib.unregister_event_queues()
    checkpoints: list[tuple[float, float, float, float, float, float]] = []
    print("waiting...")
    last_text = pyperclip.paste()
    event_queue = m.EventQueue()
    while True:
        event_queue.register_outgoing_chat_interceptor(pattern="undo|done|portal")
        try:
            event = event_queue.get(block=False)
            if event.message == "undo":
                if len(checkpoints):
                    x,y,z,dx,dy,dz = checkpoints.pop()
                    print(x,y,z,dx,dy,dz)
                    lib.execute(f"execute positioned {x:.2f} {y:.2f} {z:.2f} run kill @e[type=block_display,tag=CP,limit=2,distance=..2,sort=nearest]")
                    lib.echo("Undid last checkpoint")
            if event.message == "done":
                make_checkpoint_markers_3_lap(checkpoints, cutscene_index)
                lib.echo("Finished checkpoint creation")
                return
            if event.message == "portal":
                event_queue.unregister_all()
                del event_queue
                p1, d1, p2, d2 = data.get_portal_near_player()
                lib.echo("Created portal at ", p1, d1, p2, d2)
                create_line_entity(*p1,*d1,1,block="purple_wool")
                create_plane_entity(*p1,*d1,width=10,height=10,block="purple_stained_glass")
                checkpoints.append((*p1,*d1))
                create_line_entity(*p2,*d2,1,block="purple_wool")
                create_plane_entity(*p2,*d2,width=10,height=10,block="purple_stained_glass")
                checkpoints.append((*p2,*d2))
                lib.unregister_event_queues()
                event_queue = m.EventQueue()
        except m.queue.Empty:
            ...
        clipboard = pyperclip.paste()
        time.sleep(0.1)
        if clipboard != last_text:
            last_text = clipboard
            x, y, z, pitch, yaw = lib.get_coords_from_clipboard(block=False)
            if x is not None:
                y += 1.52
                dx, dy, dz = get_forward(yaw, pitch)
                create_line_entity(x,y,z,dx,dy,dz,1,block="lime_wool")
                create_plane_entity(x,y,z,dx,dy,dz,width=10,height=10,block="lime_stained_glass")
                checkpoints.append((x,y,z,dx,dy,dz))

def make_checkpoints_3_lap_with_split(cutscene_index):
    lib.unregister_event_queues()
    with m.EventQueue() as event_queue:
        checkpoints: list[list[tuple[float, float, float, float, float, float]]] = []
        event_queue.register_outgoing_chat_interceptor(pattern="undo|done|split|merge|secondpath")
        is_splitting: bool = False
        on_second_split: bool = False
        split_index: int = 0
        last_text = pyperclip.paste()
        while True:
            try:
                event = event_queue.get(block=False)
                if event.message == "undo":
                    if len(checkpoints):
                        if not on_second_split:
                            if len(checkpoints[-1]) > 1:
                                lib.echo("Cannot undo merge.")
                            else:
                                x,y,z,dx,dy,dz = checkpoints.pop()[0]
                                print(x,y,z,dx,dy,dz)
                                lib.execute(f"execute positioned {x:.2f} {y:.2f} {z:.2f} run kill @e[type=block_display,tag=CP,limit=2,distance=..2,sort=nearest]")
                                lib.echo("Undid last checkpoint")
                        else:
                            if len(checkpoints[split_index-1]) == 1:
                                lib.echo("Cannot switch back to first path.", checkpoints[split_index-1])
                            else:
                                split_index-=1
                                x,y,z,dx,dy,dz = checkpoints[split_index].pop()
                                print(x,y,z,dx,dy,dz)
                                lib.execute(f"execute positioned {x:.2f} {y:.2f} {z:.2f} run kill @e[type=block_display,tag=CP,limit=2,distance=..2,sort=nearest]")
                                lib.echo("Undid last checkpoint (Second path split)")
                if event.message == "done":
                    make_checkpoint_markers_3_lap_with_split(checkpoints, cutscene_index)
                    return
                if event.message == "split":
                    if is_splitting:
                        lib.echo("Can't split as you're already on a split path!")
                    else:
                        is_splitting = True
                        on_second_split = False
                        split_index = len(checkpoints)
                if event.message == "secondpath":
                    if not is_splitting:
                        lib.echo("Can't go to second path - not on split.")
                    elif on_second_split:
                        lib.echo("Can't go to second path - already there.")
                    else:
                        on_second_split = True
                if event.message == "merge":
                    if not is_splitting:
                        lib.echo("Can't merge - not on split.")
                    if not on_second_split:
                        lib.echo("Can't merge - not on second path.")
                    if len(checkpoints) != split_index:
                        lib.echo("Can't merge - Second path not complete.", len(checkpoints), split_index)
                    else:
                        is_splitting = False
                        on_second_split = False

            except m.queue.Empty:
                ...
            clipboard = pyperclip.paste()
            time.sleep(0.1)
            if clipboard != last_text:
                last_text = clipboard
                x, y, z, pitch, yaw = lib.get_coords_from_clipboard(block=False)
                if x is not None:
                    y += 1.52
                    dx, dy, dz = get_forward(yaw, pitch)
                    if not on_second_split:
                        checkpoints.append([(x,y,z,dx,dy,dz)])
                        create_line_entity(x,y,z,dx,dy,dz,block="red_wool" if is_splitting else "lime_wool",length=1)
                        create_plane_entity(x,y,z,dx,dy,dz,width=10,height=10,block="red_stained_glass" if is_splitting else "lime_stained_glass")
                        lib.echo("Created new plane")
                    else:
                        if len(checkpoints) <= split_index:
                            lib.echo("End of split path! please merge.")
                        else:
                            checkpoints[split_index].append((x,y,z,dx,dy,dz))
                            split_index += 1
                            create_line_entity(x,y,z,dx,dy,dz,block="blue_wool",length=1)
                            create_plane_entity(x,y,z,dx,dy,dz,width=10,height=10,block="blue_stained_glass")
                            lib.echo("Created new plane")


                    

def make_checkpoints_1_lap(cutscene_index):
    lib.unregister_event_queues()
    with m.EventQueue() as event_queue:
        checkpoints: list[list[tuple[float, float, float, float, float, float]]] = [[]]
        event_queue.register_outgoing_chat_interceptor(pattern="undo|done|newlap")
        last_text = pyperclip.paste()
        while True:
            try:
                event = event_queue.get(block=False)
                if event.message == "undo":
                    if len(checkpoints[-1]):
                        x,y,z,dx,dy,dz = checkpoints[-1].pop()
                        print(x,y,z,dx,dy,dz)
                        lib.execute(f"execute positioned {x:.2f} {y:.2f} {z:.2f} run kill @e[type=block_display,tag=CP,limit=2,distance=..2,sort=nearest]")
                        lib.echo("Undid last checkpoint")
                    else:
                        if len(checkpoints):
                            checkpoints.pop()
                            lib.echo("Undid making a new lap")
                elif event.message == "done":
                    lib.echo("Done!")
                    make_checkpoint_markers_1_lap(checkpoints, cutscene_index)
                    return
                elif event.message == "newlap":
                    checkpoints.append([])
                    lib.echo("Starting new lap")
            except m.queue.Empty:
                ...
            clipboard = pyperclip.paste()
            time.sleep(0.1)
            if clipboard != last_text:
                last_text = clipboard
                x, y, z, pitch, yaw = lib.get_coords_from_clipboard(block=False)
                if x is not None:
                    y += 1.52
                    dx, dy, dz = get_forward(yaw, pitch)
                    create_line_entity(x,y,z,dx,dy,dz,1,block="lime_wool")
                    create_plane_entity(x,y,z,dx,dy,dz,width=10,height=10,block="lime_stained_glass")
                    checkpoints[-1].append((x,y,z,dx,dy,dz))
            
            

def main():
    import sys
    import probe
    index = probe.cutscene_index_from_name(sys.argv[1])
    if index:
        print("Using cutscene index", index)
        lib.unregister_event_queues()
        make_checkpoints_3_lap(index)

def create_line_entity(x: float, y: float, z: float, dx: float, dy: float, dz: float,
                       length: float = 10.0, block: str = "stone"):
    """
    Summon a single thin block_display entity at (x,y,z), stretched and rotated 
    to form a line pointing in direction (dx,dy,dz).

    Args:
        x, y, z (float): Starting coordinates.
        dx, dy, dz (float): Direction vector.
        length (float): Length of the line.
        block (str): Block type to display.
    """
    # Normalize direction vector
    mag = math.sqrt(dx*dx + dy*dy + dz*dz)
    if mag == 0:
        raise ValueError("Direction vector cannot be zero.")
    ux, uy, uz = dx/mag, dy/mag, dz/mag

    # Default forward vector (Z+)
    fx, fy, fz = 0, 0, 1

    # Dot and cross
    dot = fx*ux + fy*uy + fz*uz
    cx, cy, cz = fy*uz - fz*uy, fz*ux - fx*uz, fx*uy - fy*ux  # cross(f,u)

    # Handle parallel vectors
    if dot > 0.9999:  # almost same
        qx, qy, qz, qw = 0, 0, 0, 1
    elif dot < -0.9999:  # opposite
        # rotate 180° around X axis
        qx, qy, qz, qw = 1, 0, 0, 0
    else:
        angle = math.acos(dot)
        s = math.sin(angle/2)
        qx, qy, qz = cx * s / math.sqrt(cx*cx+cy*cy+cz*cz), cy * s / math.sqrt(cx*cx+cy*cy+cz*cz), cz * s / math.sqrt(cx*cx+cy*cy+cz*cz)
        qw = math.cos(angle/2)

    # NBT uses floats with "f" suffix
    q_str = f"[{qx:.3f}f,{qy:.3f}f,{qz:.3f}f,{qw:.3f}f]"

    cmd = (
        f'summon block_display {x:.2f} {y:.2f} {z:.2f} '
        f'{{block_state:{{Name:"{block}"}}, '
        f'transformation:{{translation:[0f,0f,0f], '
        f'left_rotation:{q_str}, '
        f'scale:[0.1f,0.1f,{length:.0f}f], '
        f'right_rotation:[0f,0f,0f,1f]}},Tags:["CP"]}}'
    )

    m.execute(cmd)

def create_plane_entity(x: float, y: float, z: float, dx: float, dy: float, dz: float,
                                       width: float = 5.0, height: float = 5.0, thickness: float = 0.1,
                                       block: str = "stone"):
    """
    Summon a thin block_display entity forming a plane perpendicular to (dx,dy,dz),
    with its center exactly at (x,y,z) in world coordinates.
    """
    # Normalize normal vector
    mag = math.sqrt(dx*dx + dy*dy + dz*dz)
    if mag == 0:
        raise ValueError("Normal vector cannot be zero.")
    nx, ny, nz = dx/mag, dy/mag, dz/mag

    # Default plane normal is Z+ (XY plane)
    fx, fy, fz = 0, 0, 1

    # Dot and cross
    dot = fx*nx + fy*ny + fz*nz
    cx, cy, cz = fy*nz - fz*ny, fz*nx - fx*nz, fx*ny - fy*nx  # cross(f, n)

    # Quaternion for rotation
    if dot > 0.9999:
        qx, qy, qz, qw = 0, 0, 0, 1
    elif dot < -0.9999:
        qx, qy, qz, qw = 1, 0, 0, 0
    else:
        angle = math.acos(dot)
        s = math.sin(angle/2)
        norm = math.sqrt(cx*cx + cy*cy + cz*cz)
        qx, qy, qz = cx*s/norm, cy*s/norm, cz*s/norm
        qw = math.cos(angle/2)

    # Convert quaternion to rotation matrix
    m00 = 1 - 2*qy*qy - 2*qz*qz
    m01 = 2*qx*qy - 2*qz*qw
    m02 = 2*qx*qz + 2*qy*qw
    m10 = 2*qx*qy + 2*qz*qw
    m11 = 1 - 2*qx*qx - 2*qz*qz
    m12 = 2*qy*qz - 2*qx*qw
    m20 = 2*qx*qz - 2*qy*qw
    m21 = 2*qy*qz + 2*qx*qw
    m22 = 1 - 2*qx*qx - 2*qy*qy

    # Local offset to center the plane (local X/Y axes)
    lx, ly, lz = -width/2, -height/2, 0.0

    # Rotate local offset by rotation matrix to get world offset
    tx = m00*lx + m01*ly + m02*lz
    ty = m10*lx + m11*ly + m12*lz
    tz = m20*lx + m21*ly + m22*lz

    q_str = f"[{qx:.3f}f,{qy:.3f}f,{qz:.3f}f,{qw:.3f}f]"

    cmd = (
        f'summon block_display {x:.2f} {y:.2f} {z:.2f} '
        f'{{block_state:{{Name:"{block}"}}, '
        f'transformation:{{translation:[{tx:.1}f,{ty:.1f}f,{tz:.1f}f], '
        f'left_rotation:{q_str}, '
        f'scale:[{width:.0f}f,{height:.0f}f,{thickness:.1f}f], '
        f'right_rotation:[0f,0f,0f,1f]}},Tags:["CP"]}}'
    )

    m.execute(cmd)

def plane_equation(x: float, y: float, z: float, dx: float, dy: float, dz: float):
    """
    Return the plane equation coefficients (a,b,c,d) for the plane
    passing through (x,y,z) with normal (dx,dy,dz)
    in the form ax + by + cz + d = 0
    """
    a, b, c = dx, dy, dz
    d = -(dx*x + dy*y + dz*z)
    return a, b, c, d

if __name__ == "__main__":
    main()
