# PoolTable.py
# Table class
# Includes positioning and movement of balls
#
import math

from PoolCollision import *
from PoolBall import *

#
# Generic functions
#

# print if new, else "."
print_text = ""
print_count = 0
def print_repeat(text):
    global print_text
    global print_count
    if text == print_text:
        print("%1s" % ".") ,
        print_count = 1
    else:
        print_text = text
        if print_count > 0:
            print ""
        print_count = 0
        print text


class PoolTable:
    """Pool Table Operation and View"""
    aimingTagName = "tag_aiming"
                        # Game type
    game8Ball = 1
    game9Ball = 2
    gameBilliards = 3
    gameBilliards3 = 4  # 3 cushian
    

    def __init__(self,
                cvs,          # Canvas widget required
                length = None,
                width = None,
                ballRadius = None,
                mdissloss = 0.,
                mbankloss = 0.,
                trace = 0,
                collision=None,
                timeBeg=time.time(),
                runPauseB = None,
                ballHolder = None,      # Optional ball holder
                tableType = PoolBall.POOL,
                gameType = game8Ball,
                scalePixelCm = 100.*2.54     # Scale: pixels per cm
                ):
        self.cvs = cvs
        self.timeBeg = timeBeg
        self.length = length
        self.width = width
        self.scalePixelCm = scalePixelCm
        self.ballRadius = ballRadius
        self.inSetup = 0
        self.isRunning = False
        self.wasPaused = False
        
        self.balls = []
        self.selectedBall = None  # No ball currentlty selected on this table
        self.trace = trace

        self.selectedBall = None  # No currently selected
        self.aimedBall = None       # No aimed ball
        self.ballHolder = ballHolder
        self.gameType = gameType   # Type game
        self.tableType = tableType  # Type of table
        
                        # For rack setting
        self.rp_theta = 0.0
        self.rp_x = 0.0
        self.rp_y = 0.0
        self.toAim = False
        self.aimedBall = None
        self.eventProc = PoolTableEvent(self)   # table event processor
        self.prevTime = 0.0                 # Set as never
        if runPauseB == None:
            runPauseB = False               # Default: paused
        self.runPauseB = runPauseB
        if collision == None:
            collision = PoolCollision(table=self)
        self.collision = collision
        self.mdissloss = mdissloss
        self.mbankloss = mbankloss
        
    def getCvs(self):
        return self.cvs

        def getLength(self):
            return self.length

        def getWidth(self):
            return self.width
        
        def getselectedBall(event):
            return self.selectedBall
    
    def clearTable(self):
        """ Clear table to empty
        """
        self.clearBalls()
        
    #
    # select ball
    def selectBall(self,
        ball
        ):
        if ball == None:
            return
        self.selectedBall = ball
        if self.trace & 8:
            number = ball.number
            print "selectBall " + str(number)

    
    #
    # table location of event
    def tableEventLoc(self,
        event
        ):
        return self.eventProc.tableEventLoc(event)

        
    def unselectBall(self):
    
        if self.trace & 8:
            if self.selectedBall != None:
                number = self.selectedBall
                print "unselectBall " + str(number)
            else:
                print "unselectBall None"
        
        self.selectedBall = None
       
    # Set velocity as delta x,y per .2oo sec
    def shootBall(self,
                aimed_ball,
                x,
                y
                ):
        if aimed_ball == None:
            return
        self.aimingRemove()         # Clear any previous aiming
        if self.trace & 8:
            print "shoot_ball_release: " + str(aimed_ball.getNumber())
     ###TBD work this out
        x0 = aimed_ball.x0
        y0 = aimed_ball.y0
        vx = (x-x0)*1.       # velocity mult 
        vy = (y-y0)*1.
        aimed_ball.vx = vx
        aimed_ball.vy = vy
        self.runPause(True)       # Start action


    def aimNext(self):
        """ Aim next selected object
            Similar to right-mouse-click
        """
        self.toAim = True

    def aimingRemove(self):
        """Remove aiming indicators and display
        """
        if self.aimedBall != None:
            self.aimedBall.aimClear()
            self.aimedBall = None

    def aimingUpdate(self,
                     x,
                     y):
        ball = self.aimedBall;
        if ball == None:
            return
        
        ball.aim(x,y)
    
    #
    # aim ball providing a arrow from ball to suggested target
    def aimBall(self,
        ball,
        x,
        y
        ):
        
        if self.aimedBall != None:
            self.aimingRemove()

        if ball == None:
            return              # No ball to aim
        
        if self.trace & 8:
            number = ball.getNumber()
            print "aimBall " + str(number)
        
        self.aimedBall = ball
        ball.aim(x,y)

    def billiards(self):
        """Set up Billiard table
        """
        empty_billiards()
        "TBD - populate table"

    def empty_billiards(self):
        """Set up empty Billiard table
        """
        tableType = PoolBall.BILLIARD
        self.setup()
        

    # Check if ball will fit at position
    def ballFits(self,
        x,          # position
        y,
        radius = None,   # Default use ball_radius
        ex = None,       # Except this ball
        ):

        if radius == None:
            radius = self.ballRadius
        ex_number = -1
        if ex != None:
            ex_number = ex.number       # Except this number
        for ball in self.balls:
            if ex != None:
                if ball.number == ex.number:
                    continue        # skip this ball in check
                
            x1 = ball.x
            y1 = ball.y
            radius1 = ball.radius
            d_sq = (x-x1)*(x-x1) + (y-y1)*(y-y1)
            rd_sq = (radius+radius1)*(radius+radius1)
            if d_sq < rd_sq:
                return False        # Too close to one ball
            
                                # Check for edges
        
        if x+radius >= self.length:
            return False
    
        if (x-radius <= 0):
            return False
        
        if y+radius >= self.width:
            return False
    
        if y-radius <= 0:
            return False
        
        return True

        
    def clearBalls(self):
        """ delete balls from table
        Erase ball drawings
        """
        for ball in self.balls:
            ball.erase()
        self.balls = []
        self.resetBallHolder()
    #
    # Select / Create ball if possible
    # Aim if toAim is True
    def createSelectBall(self,     # Returns ball else None
        x,
        y,
        number = None,              # Choose this ball number
        ):
        ball = self.insideBall(x,y)
            
        if ball == None:
            if self.ballFits(x,y):
                if number == None:
                    number = self.numberAvailable()
                if number == None:
                    return None     # None available
                ball = PoolBall(
                        number = number,
                        x = x,
                        y = y,
                        table = self,
                        )
                self.balls.append(ball)     # Add to table balls
                self.selectBall(ball)
                ball.draw()
                self.setBallInUse(number)   # already selected this ball
        self.selectBall(ball)
        
        if self.toAim:
            self.aimBall(ball, x, y)            # Aim selected ball
        return ball

        
    def deleteBall(self,
                   number,      # Ball number
                   ):
        """ delete ball from table
        Erase ball drawings
        """
        for i, ball in enumerate(self.balls):
            if ball.number == number:
                del self.balls[i]
                ball.erase()
                break
        return ball

    def setCollision(self,
                     collision):
        """Connect collision processing with table
        """
        self.collision = collision
        collision.trace = self.trace    # Force Table trace level on collision

    """
    Stop game, if in progress
    Setup table and ball holder
    """
    def setGame(self,
                    gameType,
                    tableType = None):
        self.gameType = gameType
        if tableType == None:
            if gameType == self.gameBilliards:
                tableType = PoolBall.BILLIARD
            else:
                tableType = PoolBall.POOL
                
        self.tableType = tableType
        self.setRunPauseB(0)
        self.clearBalls()
        if self.ballHolder:
            self.ballHolder.setGame(gameType, tableType)

    def setGame8Ball(self):
        self.setGame(self.game8Ball)
        
    def setGame9Ball(self):
        self.setGame(self.game9Ball)
        
    def setGameBilliards(self):
        self.setGame(self.gameBilliards)

    def setRunPauseB(self,
                     runPauseB):
        self.runPauseB = runPauseB


    def setBallInUse(self,
                     number,
                     inUse=True):
        if self.ballHolder == None:
            return                  # Ignore if no ball holder
        self.ballHolder.setBallInUse(number, inUse)


    def setBallHolder(self,
                     ballHolder):
        self.ballHolder = ballHolder
        ballHolder.table = self     # link back to us
        ballHolder.tableType = self.tableType   # Transfer table type
        
        
    def setup(self):
        """ Setup table for play
        """
        self.inSetup = False
        self.runPause(False)                   # Stop running    
###        self.clearTable()
        running = 0                   # Stop running
        self.eventProc.setup()
        
    def runPause(self,
                 run=None):
        """ Set motion to run or pause
        """
        if run == None:
            run = not self.isRunning
        if not run:
            self.wasPaused = True
            
        self.isRunning = run
    
        """Button not currently used    
        if self.isRunning:
            self.runPauseB.config(text = "Pause")
        else:
            self.runPauseB.config(text = "Run")
        """
        return self.isRunning


    def resetBallHolder(self):
        """Initialize ball holder as filled
        """
        if self.ballHolder == None:
            return                  # No holder - ignore
        
        self.ballHolder.reset()
        
        
    def running(self):
        """ Tells running/pause state
        """
        return self.isRunning
    

    def update(self):
        """ Update table periodically if running
        """
        new_time = time.time()

        if self.isRunning:
            if self.wasPaused or self.prevTime == 0.0:
                self.prevTime = new_time
                self.wasPaused = False
            update_time = new_time - self.prevTime
            self.prevTime = new_time            # track since now
            self.collision.updateBalls(update_time, self.balls)
            
        for ball in self.balls:
            ball.draw()
            
    #
    # Check if location is inside some ball,
    # returning that ball if one
    def insideBall(self,        # Returns ball if inside one, else None
        x,
        y,
        balls=None,
        ):
        if balls == None:
            balls = self.balls
            
        for ball in balls:
            ballx = ball.x
            bally = ball.y
            radius = ball.radius
            radius_sq = radius*radius
            dist_sq = (ballx-x)*(ballx-x)+(bally-y)*(bally-y)
            if dist_sq < radius_sq:
                return ball
    
        return None
    
    def draw(self):
        """ Draw table and contents
        """
        for ball in self.balls:
            ball.erase()

    
    def rackPosition_set (
        self,
        x,
        y,
        theta,
        ):

        """ Setup function for racking
        Default" keep from edge
        """
            
        if theta == None:
            theta = atan2(0,-1)
    
        if y == None:    
            y = self.width/2
        if x == None:
            x = self.length/4
        
        br = self.ballRadius
        h = 4*br*sqrt(3.)
        spot_clear = h + 3*br    # Clearing by one ball
        if x < spot_clear:
            x = spot_clear
            
        self.rp_theta = theta
        self.rp_x = x
        self.rp_y = y
    
    def empty_8ball(self,
        ):
        """ Cleared 8-ball table
        """
        self.setGame8Ball()   # Start with clear table
    
    def empty_9ball(self,
        ):
        """ Cleared 9-ball table
        """
        self.setGame9Ball()   # Start with clear table

    
    def rack8ball(self,
        x,                  # Head pin in inches
        y,
        theta,              # pointing towards base
                            # Default: right to left
        ):
        """ Add balls positioned for standard 8-ball initial setup
        """
        self.setGame8Ball()
        self.rackPosition_set(x,y,theta)
        self.balls = self.rackPosition([1,2,3,4,5],
                 [1, 
                  15,14,
                   4, 8, 5,
                  13,12, 7,11,
                   2,10, 6, 9, 3])    
    
    def rack9ball(
        self,
        x,                  # Head pin in inches
        y,
        theta,              # pointing towards base
                                 # Default: right to left
        ):
        """ Add balls positioned for standard 9-blll initial setup
        """
        self.setGame9Ball()
        self.rackPosition_set(x,y,theta)
        self.balls = self.rackPosition([1,2,3,2,1],
                     [1, 2,3, 4,9,5,
                      6,7, 8])


 
    def rackPosition (
        self,
        rowcounts,          # ref to Number in each row
        ballnumbers,        # ref to array of ball numbers
        ):
        """Position closest packed balls in a
        rack with symetricly placed balls
        """
        rowcounts = rowcounts
        if ballnumbers == None:
            ballnumbers = []
            nballs = 0
            for i in range(0, len(rowcounts)):
                nballs += rowcounts[i]
            for n in range(1,nballs+1):
                ballnumbers.append(n)
        balls = []
        r = []
        ballindex = 0
        for i in range(0, len(rowcounts)):
            if (i == 0):
                number = ballnumbers[ballindex]
                ball = PoolBall(x=self.rp_x, y=self.rp_y,
                    number=number,
                    table=self,     # Reference to table
                    )
                ballindex+=1
                r = ball.radius
                balls.append(ball)
                ball.draw()
                self.setBallInUse(number)
                continue
            rowcount = rowcounts[i]
            rowcount_prev = rowcounts[i-1]
            th = PI/6        # angular displacment of next row
            angdisp = -th if rowcount > rowcount_prev else th
    
            ball_edge = balls[len(balls)-rowcount_prev]
            x_ep = ball_edge.x
            y_ep = ball_edge.y
            (x_e,y_e) = vRsumxy(self.rp_theta+angdisp, 2.0*r, x_ep, y_ep)
            for j in range(0, rowcount):
                (x, y) = vRsumxy(self.rp_theta+PI/2, j*r*2, x_e, y_e)
                number = ballnumbers[ballindex]
                self.setBallInUse(number)
                ball = PoolBall(x=x, y=y,
                          number=number,
                          table=self
                          )
                ballindex+=1
                balls.append(ball)
                ball.draw()
        return balls

    def billiards(self):
        self.setGameBilliards()        
        head_x = self.length/4.
        head_y = self.width/2.
        self.createSelectBall(head_x, head_y, 2)        # Red

        foot_x = self.length * 3./4.
        foot_y = self.width/2.
        self.createSelectBall(foot_x, foot_y, 1)        # Yellow

        spot_x = foot_x
        spot_y = head_y - self.width * .16
        self.createSelectBall(spot_x, spot_y, 0)        # White
        self.unselectBall()
        
    def empty_billiards(self):
        self.setGameBilliards()

    # Check for close edge
    def nearEdge(self,
        x,
        y,
        r = None,
        ):
    
        if r == None:
            r = self.ballRadius
        xmax = self.length - r
        xmin = r
        ymax = self.width - r
        ymin = r
    
        col_xmax = False
        col_xmin = False
        col_ymax = False
        col_ymin = False
        
        if x+1.5*r > xmax:
            print("x=%.2f(%.2fr)" % (x,(x+r-xmax)/r))
    
        if x-1.5*r < xmin:
            print("x=%.2f(%.2fr)" % (x,(x-r-xmin)/r))
    
        if y+1.5*r >= ymax:
            print("y=%.2f(%.2fr)" % (y,(y+r-ymax)/r))
    
        if y-1.5*r <= ymin:
            print("y=%.2f(%.2fr)" % (y,(y-r-ymin)/r))
    
    #
    # select available ball
    # May be replaced with user selection
    def numberAvailable(self):     # Returns: available ball number (0 cue ball), None if none available
        if self.ballHolder == None:
            return None
        
        return self.ballHolder.numberAvailable()
        return None                # No unfound numbers
        
        
    # Adjust location
    def placeBallMotionEvent(self,       # Returns True if ball can fit here
        event,                           # Canvas
        ):


        ball = self.selectedBall
        if ball == None:
            return False

        (x,y) = self.eventProc.tableEventLoc(event)
        if not self.ballFits(x,y, ex=ball):
            return False
        ball.moveTo(x,y)
        return True
    
    
    
    # Set velocity as delta x,y per .2oo sec
    def placeBallReleaseEvent (
        event
        ):
        xraw = event.x
        yraw = event.y
    
        x_pix = cvs.canvasx(xraw)
        x = self.scaleFromPix(x_pix)
        y_pix = cvs.canvasy(yraw)
        y = self.scaleFromPix(y_pix)
        r_ball = set_ball['_r_ball']
        r_pix = self.scaleToPix(r_ball['_radius'])
    
        if not '_site_ball_id' in set_ball:
            return
        if not id in self.setBall:
            return
    
        x0_pix = self.scaleToPix(ball.x)
        y0_pix = self.scaleToPix(ball.y)
    
        cvs.move(setBall.id,
               x_pix-x0_pix,
               y_pix-y0_pix)
    
        if (not self.inSetup):
            self.running = 1       # Start action again


        
        
        # Scale to pixel value from internal real units
    def scaleFromPix (self,       # eturns: len in cm
           pixlen,
           ):
        return float(pixlen)/self.scalePixelCm
   
   
    # Scale to pixel value from internal real units
    def scaleToPix (self,       # Returns: len in pixels
           reallen,
           ):
       return int(reallen*self.scalePixelCm)
 



class PoolTableEvent:
    """Control pool table events such as mouse operations
    """
    def __init__(self,
                 table,     # Associated table
                 ):
        self.table = table
        self.trace = table.trace    # Easy trace access
        self.cvs = table.cvs        # Easy drawing access
        self.trace = table.trace    # Ease of access
        
    def getTable():
        return self.table

    def getLength():
        return self.table.getLength()

    def getWidth():
        return self.table.getWidth()
    
    def getCvs():
        return self.table.getCvs()
    
    def setup(self):
        cvs = self.cvs
        cvs.bind("<Button-1>",
                self.tableButton1ClickEvent)
        cvs.bind("<Button-3>",
                 self.tableButton3ClickEvent)
        cvs.bind("<Motion>", self.tableMotionEvent)
        cvs.bind("<ButtonRelease>", self.tableButtonReleaseEvent)


    #
    # Left button click
    #    1. Selects ball if cursor is within ball
    #    2. Creates new ball if not within any ball

    def tableButton1ClickEvent(self,
        event
        ):
            
        (x,y) = self.tableEventLoc(event)
        if self.trace & 8:
            print "button1_click"
            length = self.table.length
            width = self.table.width
            lf = x/length
            wf = y/width
            print("x=%.2f(%.2fw), y=%.2f(%.2fw)" % (x, lf, y, wf))
            self.table.nearEdge(x,y)
        self.table.createSelectBall(x,y)
    
        
        
    #
    # Right button click
    #   Aim ball
    #   1. Duplicate Left button click
    #   2. Setup aiming
    #      a. setup aiming arrow line which start aiming process
    #
    def tableButton3ClickEvent(self,
        event
        ):
        if self.trace & 8:
            print "button3_click"
        if self.table.selectedBall != None:
            return          # Already selected
        
        (x,y) = self.tableEventLoc(event)
        ball = self.table.createSelectBall(x,y)
        if ball != None:
            self.table.aimBall(ball, x, y)
    
            
    # Button release
    #  1. if aiming ball shoot it
    #  2. if selected, unselect ball
    def tableButtonReleaseEvent(self,
        event
        ):
        
        if self.trace & 8:
            print "release_event"
        if self.table.selectedBall == None:
            print "selectedBall == None"
            return
        
        if self.table.aimedBall != None:
            (x,y) = self.tableEventLoc(event)        
            self.table.shootBall(self.table.aimedBall, x, y)
            self.table.aimingRemove()
            
        self.table.unselectBall()
    
    
    
    #
    # table location of event
    def tableEventLoc(self,
        event
        ):
        (x_pix, y_pix) = self.tableEventLocPix(event)
        x = self.table.scaleFromPix(x_pix)
        y = self.table.scaleFromPix(y_pix)
        return (x,y)
    
    #
    # table location of event in canvas pixels
    def tableEventLocPix(self,
        event
        ):
        xraw = event.x
        yraw = event.y
        cvs = self.cvs
        x_pix = cvs.canvasx(xraw)
        y_pix = cvs.canvasy(yraw)
        return (x_pix,y_pix)
    
    
    #
    # Table motion event
    #   1. Move
    #      a. If aiming, move aiming sight to current location
    #           else move selected ball to current location
    #
    def tableMotionEvent(self,
        event
        ):
        
        (x,y) = self.tableEventLoc(event) 
        if self.trace & 8:
            print_repeat("motion_event")
            self.table.nearEdge(x,y)
            
        if self.table.selectedBall == None:
            return          # Noting to do
        if self.table.aimedBall != None:
            self.table.aimingUpdate(x,y)
        else:
            self.table.placeBallMotionEvent(event)
    
       


