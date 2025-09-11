import time
import minescript as m
import sys
import lib

# Regex to detect F3+C coordinates with yaw and pitch

def quadratic_bezier_5d(p0, p1, p2, n_points=20):
    """Generate points along a quadratic Bézier curve, interpolating yaw and pitch too."""
    points = []
    print(p0, p1, p2)
    for i in range(n_points):
        t = i / (n_points - 1)
        x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        z = (1-t)**2 * p0[2] + 2*(1-t)*t * p1[2] + t**2 * p2[2]
        yaw = (1-t)**2 * p0[3] + 2*(1-t)*t * p1[3] + t**2 * p2[3]
        pitch = (1-t)**2 * p0[4] + 2*(1-t)*t * p1[4] + t**2 * p2[4]
        points.append((x, y, z, yaw, pitch))
    return points

def summon_along_curve(points, cutscene_id, start_index=1):
    """Summon armor stands along the curve, setting CUT and TRACK scores."""
    for idx, (x, y, z, yaw, pitch) in enumerate(points, start=start_index):
        # Summon armor stand
        cmd = (
            f'summon armor_stand {x:.3f} {y:.3f} {z:.3f} '
            f'{{NoGravity:1b,Invisible:1b,Marker:1b,Rotation:[{yaw:.2f}f,{pitch:.2f}f],Tags:["GKT"]}}'
        )
        m.execute(cmd)
        # Set CUT scoreboard for nearest armor stand at this position
        m.execute(
            f'execute positioned {x:.3f} {y:.3f} {z:.3f} run '
            f'scoreboard players set @e[tag=GKT,limit=1,sort=nearest] CUT {idx}'
        )
        # Set TRACK scoreboard
        m.execute(
            f'execute positioned {x:.3f} {y:.3f} {z:.3f} run '
            f'scoreboard players set @e[tag=GKT,limit=1,sort=nearest] TRACK {cutscene_id}'
        )

def make_cutscene(cutscene_id, tp_command):
    lib.echo("Waiting for 12 F3+C copies (four splines)...")
    pts = []
    for i in range(12):
        if i == 9:
            m.execute(f"gamemode spectator")
            m.execute(f"title @s times 10 200 10")
            m.execute('title @s title {"text":"Don\'t touch your mouse","color":"red"}')
            time.sleep(5)
            m.execute("portal debug accelerate 0")
            m.execute(f"tp @s {tp_command}")
            m.execute(f"tp @s ^ ^ ^-5 ~ ~30")
            m.execute(f"tp @s ^ ^ ^-5 ~ ~30")
            time.sleep(1)
            pt = *m.player_position(), *m.player_orientation()
        elif i == 10:
            m.execute(f"tp @s {tp_command}")
            m.execute(f"tp @s ^ ^ ^-5 ~ -20")
            time.sleep(1)
            pt = *m.player_position(), *m.player_orientation()
        elif i == 11:
            m.execute(f"tp @s {tp_command}")
            time.sleep(1)
            pt = *m.player_position(), *m.player_orientation()
            time.sleep(0.3)
        else:
            lib.echo(f"Copy point {i+1}/12 with F3+C")
            pt = lib.get_coords_from_clipboard()
        pts.append(pt)
        lib.echo(f"Got point: {pt}")

    all_points = []
    for i in range(0, 12, 3):
        spline_points = quadratic_bezier_5d(pts[i], pts[i+1], pts[i+2], n_points=50)
        all_points.append(spline_points)
    lib.echo(f"Summoning {sum(len(s) for s in all_points)} armor stands along splines...")
    start_index = 1
    for spline_points in all_points:
        summon_along_curve(spline_points, cutscene_id, start_index=start_index)
        start_index += len(spline_points)
    return pts
