#!/usr/bin/python
# poolGame.py       19Feb2016
# 15-Aug-2016 crs remove ball feature
import sys
       
import argparse

import re
import time
from math import *
from random import *
from copy import *

import PoolTk           # 2.x / 3.x interface to Tk
from PoolTable import *
from PoolBall import *
from PoolBallHolder import *
from PoolWindow import *




# Internal values are kept in centimeters, grams, seconds
# velocity  = cm/sec
#
# User specifications default to cgs
# Suffixes
#   cm = cm, or cm/sec
#   in = inches (2.54 cm)
#   ft

time_passed = 0.0    # Time passed since beggining of show
time_prev = 0.0      # Time of previous display
clock_ticks = 0    # Elapsed time
item_number = 0     # Identifier on item e.g. ball
                        # Display screen size of table
                    # energy loss
mdissloss = 0.01     # Fraction of energy loss per cm travel
mbankloss = 0.125    # Fraction of energy loss per bank * cos angle

table_cond = ""   # table conditions: b - billiard, p - pool, 8 - 8ball, 9 - 9ball, e - empty r - running
table_type = '9'
table_game = ''     # table game, 8, 9
table_empty = False # True - table starts empty
table_run = False   # True - game starts running

width_in = "50in"
length_in = "100in"
vx0_in = "-2ft"                    # Current velocity
vy0_in = "5ft"
ball_radius_in = "1.125in"  # Radius
clock_tick = .03   # Clock tick time sec
ball_color = 'white'
display_tick = .03 # Display update tick
scale_pixel_in = 12.   # Pixels per inch


# Convert unit numbers to internal (cm)
def cvt_units(
    ustr,    # Value with optional unit
    ):
    res = re.match('^(.+)cm?', ustr)
    if (res != None):
        return float(res.group(1))
    
    res = re.match('^(.+)in?', ustr)
    if (res != None):
        return float(res.group(1)) * 2.54
    
    res = re.match('^(.+)ft?', ustr)
    if (res != None):
        return float(res.group(1)) * 2.54 * 12
    
    res = re.match('^(.+)m/', ustr)
    if (res != None):
        return float(res.group(1)) * 100
    
    res = re.match('^([\d.]+)', ustr)
    if (res != None):
        return float(res.group(1))         # Simple number
    
    raise Exception(ustr + " is not a valid unit length")



do_stripes = 1     # 1 - do stripes
set_ball = {}       # ball placement current state
setup_balls = []    # Staging area
trace = 0                  # Debugging trace level
                        # 0x01 - ball collision
                        # 0x02 - edge collision
                        # 0x04 - shoot ball
                        # 0x08 - mouse button events
                        # 0x10 - update display

tacecollisions = 0     # trace of collisions
table_color = 'green'
checkCollision = 0 # 1 - > check ball collision test run
Tr = 2.54          # Test radius
Tx0 = 40
Ty0 = 25.4
b1 = {
    '_number' : 1,
    '_x'  : Tx0,
    '_y' : Ty0,
    '_vx' : 10,
    '_vy' : 0,
    '_radius' : Tr
}
b2 = {
    '_number' : 2,
    '_x' : Ty0+2*Tr-.01,
    '_y' : Tx0,
    '_vx' : 0,
    '_vy' : 0,
    '_radius' : Tr,
}
r_b1 = b1       # Perl used reference
r_b2 = b2

icol = -1                  # Color index
ball_number = 0             # Runing ball number
ball_number_max = 15        # Maximum ball number, starting with 1, not including cue ball
select_ball_ball = None     # Selected ball if any
aimed_ball = None           # nonNone its a ball

aiming_tag = None           # Set if aiming
###colors = [ 'white', 'black', 'blue', 'brown', 'grey',]

saved_tables = []    # Saved table setups
setup_balls = []    # Initial balls setup
in_setup = 0   # 1 - in setup mode

###balls          # Balls in play
running = 1        # 0 - paused, no updates

parser = argparse.ArgumentParser()
parser.add_argument('--color=', dest='color', default=table_color)       #       =>  \$table_color,  # Table color
parser.add_argument('--display_tick=', dest='display_tick', default=display_tick)  # => \$display_tick, # Display tick
parser.add_argument('--width=', dest='width', default=width_in)       #       =>  \$width_in,     # table width
parser.add_argument('--length=', dest='length', default=length_in)       #      =>  \$length_in,    # table length
parser.add_argument('--mdistloss')
parser.add_argument('--mbankloss')
parser.add_argument('--vx=', dest='vx', default=vx0_in)           #          =>  \$vx0_in,
parser.add_argument('--vy=', dest='vy', default=vy0_in)            #          =>  \$vy0_in,
parser.add_argument('--radius=', dest='radius', default=ball_radius_in)       #      =>  \$ball_radius_in,
parser.add_argument('--scale_pix', dest='scale_pixel_in', default=scale_pixel_in)
parser.add_argument('--sx', dest='sx', default=stick_to_xmax)            #            =>  \$stick_to_xmax,
parser.add_argument('--sy', dest='sy', default=stick_to_ymax)            #            =>  \$stick_to_ymax,
parser.add_argument('--table=', dest='table', default=table_cond)

parser.add_argument('--tick=', dest='tick', default=clock_tick)         #        =>  \$clock_tick,
parser.add_argument('--trace=', dest='trace', default=int(trace))        #       =>  \$trace,
parser.add_argument('--xcheck', dest='xcheck', default=checkCollision)        #        =>  \$checkCollision,
parser.add_argument('--x1=', dest='x1', default=b1)           #          =>  \%b1,                      
parser.add_argument('--x2=', dest='x2', default=b2)           #              =>  \%b2,


args = parser.parse_args()             # or die "Illegal options"

scale_pixel_in = args.scale_pixel_in
scale_pixel_cm = scale_pixel_in / 2.54  # To support cm

table_color = args.color
table_cond = args.table
for char in table_cond:
    if 'b' == char:
        table_type = 'b'
    elif 'p' == char:
        table_type = 'p'
    elif 'r' == char:
        table_run = True
    elif 'e' == char:
        table_empty = True
    elif '8' == char:
        table_game = '8'
    elif '9' == char:
        table_game = '9'
    else:
        raise Exception("table char {} in {}is unrecognized".format(char, table_cond))
    
width_in = args.width
length_in = args.length
vx0_in = args.vx
vy0_in = args.vy
ball_radius_in = args.radius
ball_radius = cvt_units(ball_radius_in)
width = cvt_units(width_in)
length = cvt_units(length_in)
vx0 = cvt_units(vx0_in)
vy0 = cvt_units(vy0_in)
ball_radius = cvt_units(ball_radius_in)
stick_to_xmax = args.sx
stick_to_ymax = args.sy
clock_tick = args.tick
table_type = args.table
trace = int(args.trace)
checkCollision = args.xcheck

if args.mdistloss != None:
    mdistloss = args.mdistloss
if args.mbankloss != None:
    mbankloss = args.mbankloss


b1 = args.x1
b2 = args.x2
print("setup_start_ b config - setup None")
setup_start_b = None

            
    

# List saved tables
# Make users choice, the current (resetable) table
get_table_var = None
get_table_om = None
get_table_choice_count = 0
def get_table ():
    
    global saved_tables
    global top_rf
    
    
    if (len(saved_tables) == 0):
        return
    start_running(0)               # Stop action
    tables_list = []
    
    for r_table in saved_tables:
        table_label = ""
        for r_ball in r_table:
            table_label += " " if table_label == "" else ""
            table_label += str(r_ball['_number'])
        tables_list.append(r_table)
    get_table_choice_count = 0            # Ignore first call
    get_table_om = OptionMenu(controls_fr,
        text = "get table",
        variable = get_table_var,
        options = tables_list,
        command = get_table_choice,
            )
    get_table_om.pack()
    get_table_om.focusCurrent()

def get_table_choice ():
    
    global get_table_choice_count
    global setup_balls
    global get_table_om
    
    get_table_choice_count+=1
    if (get_table_choice_count == 1):   # Ignore first call
        return
    if (trace):
        print("get_table_choice")
        setup_balls = get_table_var
    if get_table_om.exists():
        get_table_om.destroy()
    reset_play() 

def n (      # Returns: short formatted number
    n,
    ndig,
    ):
    ndig = 1 if ndig == None else ndig
    fmt = "%." + ndig + "f"
    str = fmt % n;
    return str


# Generate random color
def random_color():
    mincolor = 10              # Minimum component
    rr = randint(0,256)
    rr = mincolor if rr < mincolor else rr

    gg = randint(0,256)
    gg = mincolor if gg < mincolor else gg

    bb = randint(0,256)
    bb= mincolor if bb < mincolor else bb

    rgbcolor = bb + 256*(gg+256*rr)
    color = "#%06X" % rgbcolor
    return color

        # 8 ball rack button
def rack_8ball ():
    global tA
    tA.rack8ball(None, None, None)
        # 8 ball rack button

def empty_8ball ():
    global tA
    tA.empty_8ball()
    
# 9 ball rack button
def rack_9ball ():
    global tA
    tA.rack9ball(None, None, None)
    
# Setup Billiards
def billiards ():
    global tA
    tA.billiards()
    
# Setup empty Billiards
def empty_billiards ():
    global tA
    tA.empty_billiards()


        # Aim Next Buttton
def aim_next ():
    global tA
    tA.aimNext()
 
        
# Save the current state of the balls on the table
def save_table ():
    global saved_tables
    global setup_balls
    global saved_balls
    
                        # Choose depeding on state
    if in_setup:
        r_balls = setup_balls
    else:
        r_balls = balls
        
        saved_balls = []    # local copy

    for r_ball in r_balls:
        ball = deepcopy(r_ball)
        saved_balls.append(ball)
    saved_tables.append(saved_balls)
                     
# Start play
def start_play ():
    global setup_start_b
    
    in_setup = 0
    reset_play()                        # set table
                                    # Setup for setup
    print("setup_start_ b config")
    setup_start_b.config(text = "Setup",
        command = setup,
            )
    print("setup_start_ b config - after")
    start_running(1)


def run_game():
    tA.runPause(run=True)

def pause_game():
    tA.runPause(run=False)

# Start/continue running
def start_running (
    to_run = 1,   # 1 - run default:1
    ):
    global tA
    tA.runPause(run=to_run)

def time_passes():
    global time_passed
    global tA
    
    time_passed += clock_tick
    tA.update()
        
# Redraw balls with new locations
def update_display ():
    global trace
    if (trace & 0x10):
        print("update_display")
    draw_balls()

             




table_horizontal_pix = scale_pixel_cm * length    # Pool long side
table_vertical_pix = scale_pixel_cm * width       # Pool short side



pTk = PoolTk.PoolTk()
mw = pTk.Tk()       # From PoolTk
    
    
    
game_fr = pTk.Frame(mw)             # Contains table Plus Ball holder
game_fr.pack(side='top')
table_fr = pTk.Frame(mw)
table_fr.pack(side = 'top')
bh_fr = pTk.Frame(mw)
bh_fr.pack(side = 'top')
    
end_pgm = False     # Set if end of pgmk_8ball
def shutdown():
    global end_pgm
    end_pgm = True

app = PoolWindow(mw,
                 gameExit=shutdown,
                 games = [
                    ['8-ball', rack_8ball],
                    ['9-ball', rack_9ball],
                    ['empty-8ball', empty_8ball],
                    ['separator', None],
                    ['Billiards', billiards],
                    ['empty-billiards', empty_billiards],
                    ],
                 actions = [
                    ['run', start_running],
                    ['pause', pause_game],
                    ['separator', None],
                    ['Aim Next', aim_next],
                    ],
                )




# Right-Click sets velocity of ball at that place
def shoot_ball_callback(event):
    shoot_ball_event(event)



    

#############################################################################
        
cvs = PoolTk.tk.Canvas(table_fr, relief = 'sunken',
                    bd     = 2,
                    width  = table_horizontal_pix,
                    height = table_vertical_pix,
                      background = table_color)
cvs.pack()
tA = PoolTable(cvs,
           length=length,
           width=width,
           ballRadius=ball_radius,
           trace=trace,
           scalePixelCm = scale_pixel_cm,
            )   
tA.setCollision(PoolCollision(table=tA))      # Connect table and collision


########################################################################
# ball holder
#  below table along longest side
########################################################################
bh_height = 2*ball_radius
bh_height_pix = scale_pixel_cm * bh_height
bh_length = length
bh_length_pix = scale_pixel_cm * bh_length

cvs_bh = PoolTk.tk.Canvas(bh_fr, relief = 'sunken',
                    bd     = 2,
                    width  = bh_length_pix,
                    height = bh_height_pix,
                      background = 'gray')
cvs_bh.pack()
                     
bH = PoolBallHolder(cvs_bh,
                    height=bh_height,
                    length=bh_length,
                    trace=trace)
tA.setBallHolder(bH)                # Connect ball holder to table

# Setup balls by placement, shoot, etc.
# Subsequent to start will start
def setup ():
    tA.setup()
    bH.setup()
    
def clear_table():
    """Clear Table button function
    """
    tA.clearTable()

def reset():
    """Reset table and game
    """
    tA.setup()

#tA.setRunPauseB(run_pause_b);
tA.runPause(False)
#    mw.eval('::ttk::CancelRepeat')
#    print("Shutting down via iconify")
#    mw.iconify()

#    print("Exiting via exit(0)")
#    sys.exit(0)



                            # Setup initial conditions
mw.protocol("WM_DELETE_WINDOW", shutdown) # Shutdown
setup()

if table_type == 'b':
    if table_empty:
        empty_billiards()
    else:
        billiards()
else:
    if table_game == '8':
        if table_empty:
            empty_8ball()
        else:
            rack_8ball()
    else:
        if table_empty:
            empty_9ball()
        else:
            rack_9ball()
            

while 1:
    if end_pgm:
        break
    time1 = time.time()           # Time before loop
    time_passes()
    mw.update()
    time2 = time.time()
    time_elapsed = time2 - time1
    if time_elapsed < display_tick:
        time_sleep = display_tick - time_elapsed
        time.sleep(time_sleep)

print("After pgm loop")
print("Shutting down via destroy")
mw.destroy()
sys.exit(0)
