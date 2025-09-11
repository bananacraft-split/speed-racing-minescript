import math
import re
import lib
import minescript as m
import amulet_nbt

PORTAL_RE = re.compile(r"(\{.*dimensionTo.*\})")

def cross(a, b):
    return (a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0])

def quaternion_multiply(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return (
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    )

def quaternion_conjugate(q):
    w, x, y, z = q
    return (w, -x, -y, -z)

def rotate_vector_by_quaternion(v, q):
    vq = (0.0, v[0], v[1], v[2])
    q_conj = quaternion_conjugate(q)
    return quaternion_multiply(
        quaternion_multiply(q, vq),
        q_conj
    )[1:]

def get_portal_near_player():
    portal_id = lib.execute_get_result("portal view_portal_data", PORTAL_RE.match, replace_nl=True)    
    portal_id = PORTAL_RE.match(portal_id).group(1)
    nbt = amulet_nbt.from_snbt(portal_id)
    assert isinstance(nbt, amulet_nbt.CompoundTag)
    axisH = (nbt.get_double("axisHX").py_float, nbt.get_double("axisHY").py_float, nbt.get_double("axisHZ").py_float)
    axisW = (nbt.get_double("axisWX").py_float, nbt.get_double("axisWY").py_float, nbt.get_double("axisWZ").py_float)
    _0 = amulet_nbt.DoubleTag(0)
    _1 = amulet_nbt.DoubleTag(1)
    rotation_quaternion = (nbt.get_double("rotationA",_1).py_float,nbt.get_double("rotationB",_0).py_float,nbt.get_double("rotationC",_0).py_float,nbt.get_double("rotationD",_0).py_float)
    front_dir = cross(axisH, axisW)
    out_dir = rotate_vector_by_quaternion(front_dir, rotation_quaternion)
    startX = nbt.get_list("Pos").get_double(0).py_float
    startY = nbt.get_list("Pos").get_double(1).py_float
    startZ = nbt.get_list("Pos").get_double(2).py_float
    endX = nbt.get_double("destinationX").py_float
    endY = nbt.get_double("destinationY").py_float
    endZ = nbt.get_double("destinationZ").py_float
    midX = (startX + endX) / 2.0
    midY = (startY + endY) / 2.0
    midZ = (startZ + endZ) / 2.0# Direction vector (end - start)
    dx = endX - startX
    dy = endY - startY
    dz = endZ - startZ

    # Length (magnitude)
    length = math.sqrt(dx*dx + dy*dy + dz*dz)

    # Normalize to unit vector
    if length != 0:
        unitX = dx / length
        unitY = dy / length
        unitZ = dz / length
    else:
        unitX = unitZ = 0.0
        unitY = 1.0

    return (midX, midY, midZ), (unitX, unitY, unitZ), (endX, endY, endZ), out_dir


# m.echo(get_portal_near_player())
# print("HELLO WORLD")