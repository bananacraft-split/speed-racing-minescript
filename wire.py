import minescript as m

PAIRS = [('light_blue', 'brown'), ('red', 'yellow'), ('orange', 'white'), ('pink', 'black'),
          ('blue', 'light_gray'), ('lime', 'purple'), ('light_blue', 'green'), ('yellow', 'brown'),
            ('red', 'orange'), ('pink', 'white'), ('black', 'light_gray'), ('blue', 'purple'),
              ('lime', 'light_blue'), ('yellow', 'green'), ('orange', 'brown'), ('red', 'white'), ('pink', 'light_gray'), ('blue', 'black'), ('light_blue', 'purple'), ('lime', 'green'), ('orange', 'yellow'), ('white', 'brown'), ('red', 'light_gray'), ('blue', 'pink'), ('light_blue', 'black'), ('purple', 'green'), ('orange', 'lime'), ('yellow', 'white'), ('brown', 'light_gray'), ('red', 'pink'), ('light_blue', 'blue'), ('black', 'green'), ('orange', 'purple'), ('lime', 'white'), ('yellow', 'light_gray'), ('pink', 'brown'), ('red', 'blue'), ('orange', 'light_blue'), ('purple', 'black'), ('white', 'green'), ('yellow', 'lime'), ('blue', 'brown'), ('light_blue', 'pink'), ('orange', 'light_gray'), ('red', 'black'), ('purple', 'white'), ('yellow', 'blue'), ('brown', 'green'), ('lime', 'pink'), ('light_blue', 'light_gray'), ('orange', 'black'), ('red', 'purple'), ('blue', 'white'), ('pink', 'green'), ('lime', 'brown'), ('yellow', 'light_blue'), ('purple', 'light_gray'), ('orange', 'blue'), ('white', 'black'), ('red', 'green'), ('yellow', 'pink'), ('purple', 'brown'), ('lime', 'light_gray'), ('light_blue', 'white'), ('orange', 'green'), ('yellow', 'black'), ('purple', 'pink'), ('red', 'brown'), ('lime', 'blue'), ('white', 'light_gray'), ('orange', 'pink'), ('yellow', 'purple'), ('black', 'brown'), ('red', 'light_blue'), ('blue', 'green'), ('lime', 'black'), ('light_gray', 'green'), ('red', 'lime')]

def place_block(x,y,z,i):
    color = PAIRS[i % len(PAIRS)][(x+y+z)%2]
    m.execute(f"setblock {x} {y} {z} minecraft:{color}_wool")

def fill_block(x1,y1,z1,x2,y2,z2, i):
    for x in range(min(x1,x2), max(x1, x2) + 1):
        for y in range(min(y1,y2), max(y1, y2) + 1):
            for z in range(min(z1,z2), max(z1, z2) + 1):
                place_block(x,y,z,i)