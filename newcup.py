import time
import re
import pyperclip
import minescript as m
import sys

import wire

x = 171
y = -60
z = 15
WIREINDEX = 0

while "command_block" in m.getblock(x, y, z):
    x += 10
    WIREINDEX += 4
x -= 2
z += 4

for dx in range(8):
    for dy in range(4):
        m.execute(f"setblock {x+dx} {y+dy} {z} terracotta")

x += 2

for dx in range(4):
    m.execute(f"setblock {x+dx} {y+2} {z} redstone_lamp")
    m.execute(f"setblock {x+dx} {y+1} {z+1} minecraft:polished_blackstone_button[face=wall,facing=south,powered=false]")
    m.execute(f"setblock {x+dx} {y} {z-1} oak_planks")
    m.execute(f"setblock {x+dx} {y-1} {z-2} oak_planks")
    m.execute(f"setblock {x+dx} {y} {z-3} oak_planks")
    m.execute(f"setblock {x+dx} {y+1} {z-2} oak_planks")
    m.execute(f"setblock {x+dx} {y+1} {z-4} oak_planks")
    m.execute(f"setblock {x+dx} {y+2} {z-3} oak_planks")
    m.execute(f"setblock {x+dx} {y+1} {z-1} minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    m.execute(f"setblock {x+dx} {y+2} {z-2} minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    m.execute(f"setblock {x+dx} {y+1} {z-3} minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    m.execute(f"setblock {x+dx} {y+2} {z-4} minecraft:repeater[delay=1,facing=south,locked=false,powered=false]")
    m.execute(f"setblock {x+dx} {y} {z-2} redstone_wire")
    m.execute(f"setblock {x+dx} {y} {z-4} minecraft:command_block[conditional=false,facing=north]")
    m.execute(f'data modify block {x+dx} {y} {z-4} Command set value "setblock ~ ~2 ~3 minecraft:redstone_block"')
    m.execute(f"setblock {x+dx} {y+2} {z-5} red_wool")
    wire.place_block(x+dx,y+2,z-5,WIREINDEX+dx)
m.execute(f"setblock {x+4} {y-1} {z-2} minecraft:command_block[conditional=false,facing=north]")
m.execute(f"data modify block {x+4} {y-1} {z-2} Command value \"fill 180 -60 -10 194 -60 -10 redstone_block\"")

wire.place_block(x,y+2, z-6, WIREINDEX)
wire.place_block(x,y+3, z-7, WIREINDEX)
wire.place_block(x+1,y+1, z-6, WIREINDEX+1)
m.execute(f"setblock {x+1} {y+2} {z-6} redstone_wire")
wire.place_block(x+1,y+3, z-6, WIREINDEX+1)
wire.place_block(x+1,y+3, z-7, WIREINDEX+1)
wire.place_block(x+2,y+2, z-6, WIREINDEX+2)
wire.place_block(x+3,y+1, z-6, WIREINDEX+3)
m.execute(f"setblock {x+3} {y+2} {z-6} redstone_wire")
wire.place_block(x+3,y+3, z-6, WIREINDEX+3)
m.execute(f"setblock {x} {y+3} {z-5} redstone_wire")
m.execute(f"setblock {x} {y+3} {z-6} redstone_wire")
m.execute(f"setblock {x+2} {y+3} {z-5} redstone_wire")
m.execute(f"setblock {x+2} {y+3} {z-6} redstone_wire")
wire.place_block(x+4,y+1, z-6, WIREINDEX+3)
wire.place_block(x+4,y+1, z-7, WIREINDEX+3)
m.execute(f"setblock {x+4} {y+2} {z-6} redstone_wire")
m.execute(f"setblock {x+4} {y+2} {z-7} redstone_wire")
wire.place_block(x+1,y+1, z-7, WIREINDEX+3)
m.execute(f"setblock {x+1} {y+2} {z-7} redstone_wire")
wire.place_block(x+1,y+1, z-7, WIREINDEX+1)
wire.place_block(x,y+1, z-7, WIREINDEX+1)
m.execute(f"setblock {x} {y+2} {z-7} redstone_wire")
wire.place_block(x,y+3, z-7, WIREINDEX+1)
wire.place_block(x-1,y+2, z-6, WIREINDEX)
m.execute(f"setblock {x-1} {y+3} {z-6} redstone_wire")
wire.place_block(x-2,y+2, z-6, WIREINDEX)
m.execute(f"setblock {x-2} {y+3} {z-6} redstone_wire")
wire.place_block(x-2,y+2, z-7, WIREINDEX)
m.execute(f"setblock {x-2} {y+3} {z-7} redstone_wire")
wire.place_block(x-2,y+2, z-8, WIREINDEX)
m.execute(f"setblock {x-2} {y+3} {z-8} redstone_wire")
wire.place_block(x,y+1, z-8, WIREINDEX+1)
m.execute(f"setblock {x} {y+2} {z-8} redstone_wire")
wire.place_block(x+2,y+2, z-7, WIREINDEX+2)
m.execute(f"setblock {x+2} {y+3} {z-7} redstone_wire")
wire.place_block(x+2,y+2, z-8, WIREINDEX+2)
m.execute(f"setblock {x+2} {y+3} {z-8} redstone_wire")
wire.place_block(x+4,y+1, z-7, WIREINDEX+3)
m.execute(f"setblock {x+4} {y+2} {z-7} redstone_wire")
wire.place_block(x+4,y+1, z-8, WIREINDEX+3)
m.execute(f"setblock {x+4} {y+2} {z-8} redstone_wire")