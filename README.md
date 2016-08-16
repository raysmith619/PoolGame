Pool Game
A simple two dimensional version of pool / billiards writen in Python.
15-Aug-2016 crs remove ball feature

My initial project goals were:
  1. Practice using Python after many years using programming languages such as C, C++, and Perl.
  2. Demonstrate Python with a graphical user interface.
  3. Demonstrate Python with a simple object-oriented use.
  4. Demonstrate the simple "motion physics" of ball-to-ball and ball-to-edge collisions.
  5. Practice simple "game setup" without searching the Internet for more elaborate and
     probably better done examples of game play, display, or coding.

History
  1. Initially this program was done as an exercise in Perl, with little object orientation.
  2. After working, but before the introduction of the "Ball Holder", this program was
     translated, rather literally, into Python.
  3. The non-object oriented Python was translated into an object oriented version.
  4. The ball holder, in which balls not on the table are held, was then added.  The ball holder
     is a class derived from the pool table.  The holder ball is a class derived from the pool ball.
  5. 15-Aug-2016: Mouse clicking an in-use ball in the ball holder removes this ball from the table
                  and makes this ball available.
     
Limitations (To be added?)
  1. There are no pockets.
  2. There is no "friction" or energy loss.
  3. There is no ball rotation.

Features
  1. Reasonable ball view, including stripes.
  2. Simple ball-to-ball and ball-to-edge collisions.
  3. Command line based, independent specification of table dimensions, ball size, game type.
  4. Games: 8-ball, 9-ball, billiards.
  5. Ball holder which contains balls, indicating in-use with "X" marking.
  6. Mouse selection, placement, and "shooting" of balls on table.  Mouse selection of balls from holder.
  7. Simple menu selection for:
          a."New Game":
            8-ball
            empty 8-ball
            9-ball
            empty 9-ball
            billiards
            empty billiards
          b. "Actions":
            "run"
            "pause"
            "Aim Next"
            
Requirements
  1. We run it on Python 2.7.  For 3.x "Tkinter" will have to be renamed "tkinter".
  2. Tkinter (Python interface to GUI Tcl/Tk), though not part of Python is maintained by ActiveState
  3. We are running under Microsoft Windows.  Previous versions have run under Linux.
     I should get around to testing...
     
Setup
  1. Copy all files to working directory.
  2. Run from working directory set class path to contain working directory.
  
Execution
  1. Default: Simulate 100" table with 9-ball rack, cue-ball in holder.  
     python poolGame.py
     Mouse-click cue-ball in holder to place it on the table
        OR
     Right-Mouse-click while at desired cue-ball table location.
     
     To "shoot" a ball, e.g. cue-ball, right-mouse-click the desired ball, and while remaining down,
     drag the mouse in the direction desired.  A "pointing-line" with arrow will indicate the direction.
     The speed of the ball, when the mouse button is released is proportional to the length of
     the pointing line.

  2. 8-ball rack with balls of 4" radii
     python poolGame.py --r 4in --table p8
  
  3. 9-ball rack with balls of 4" radii
    python poolGame.py --r 4in --table p9
    
  4. Billiards with 4" radii balls
     python poolGame.py --r 5in --table b
     
  5. Program help message
     python poolGame.py --h
     
     usage: poolGame.py [-h] [--color= COLOR] [--display_tick= DISPLAY_TICK]
                   [--width= WIDTH] [--length= LENGTH] [--mdistloss MDISTLOSS]
                   [--mbankloss MBANKLOSS] [--vx= VX] [--vy= VY]
                   [--radius= RADIUS] [--scale_pix SCALE_PIXEL_IN] [--sx SX]
                   [--sy SY] [--table= TABLE] [--tick= TICK] [--trace= TRACE]
                   [--xcheck XCHECK] [--x1= X1] [--x2= X2]

    optional arguments:
      -h, --help            show this help message and exit
      --color= COLOR
      --display_tick= DISPLAY_TICK
      --width= WIDTH        Table width in inches
      --length= LENGTH      Table length in inches
      --mdistloss MDISTLOSS NOT YET IMPLEMENTED
      --mbankloss MBANKLOSS NOT YET IMPLEMENTED
      --vx= VX
      --vy= VY
      --radius= RADIUS
      --scale_pix SCALE_PIXEL_IN        Scale pixels per inch
      ... plus a lot of extraneous options

Files
    HPoolBall.py        - Pool ball holder
                            HPoolBall provides ball in holder indicating if in-use
                            Supports selection of balls to be placed in action
                            HPoolBall is derived from PoolBall
    PoolBall.py         - Pool ball
                            Supports ball drawing
    PoolBallHolder.py   - Pool ball holder
                            Displays all balls, in action or not
    PoolCollision.py    - Billiard collision calculation
                            Separates ball motion physics from display
    poolGame.py         - Main game program
                            Accepts command line inputs and runs game
    PoolTable.py        - Table processing
                            Controls game table processing and display
                            Communicates with / Controls Ball holder
    
    PoolWindow.py       - Game main window, including menu processing
    
    README.md           - This program description file
    
