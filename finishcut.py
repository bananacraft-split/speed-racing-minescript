import time
import re
import pyperclip
import minescript as m
import sys

m.execute("execute as @e[type=minecraft:armor_stand,tag=GKT] at @s run tp @s ~ ~20 ~")
m.execute("tag @e[tag=GKT] add SPLINE")
m.execute("tag @e[tag=GKT] remove GKT")
m.execute("execute as @e[type=minecraft:armor_stand,tag=SPLINE] at @s rotated as @s run summon marker ~ ~ ~ {Tags:[\"SPLINE\", \"newspl\"]}")
m.execute("execute as @e[type=minecraft:armor_stand,tag=SPLINE] at @s rotated as @s run tp @e[type=marker,tag=SPLINE,tag=newspl,limit=1,sort=nearest] ~ ~ ~ ~ ~")
m.execute("execute as @e[type=minecraft:armor_stand,tag=SPLINE] at @s run scoreboard players operation @e[type=marker,tag=SPLINE,tag=newspl,limit=1,sort=nearest] TRACK = @s TRACK")
m.execute("execute as @e[type=minecraft:armor_stand,tag=SPLINE] at @s run scoreboard players operation @e[type=marker,tag=SPLINE,tag=newspl,limit=1,sort=nearest] CUT = @s CUT")
m.execute("execute as @e[type=minecraft:armor_stand,tag=SPLINE] at @s run kill @s")