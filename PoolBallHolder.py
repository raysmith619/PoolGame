# PoolBallHolder.py
# Table class
# Includes Selection, Removing balls
#
from PoolTable import *
from HPoolBall import *        

class PoolBallHolder:
    """Pool Table Operation and View"""
    aimingTagName = "tag_aiming"

    def __init__(self,
                cvs,          # Canvas widget required
                height = None,
                length = None,
                ballRadius = None,
                trace = 0,
                ):
        self.cvs = cvs
        self.length = length
        self.height = height
        self.ballRadius = ballRadius
        self.balls = []     # Balls in holder
        self.trace = trace
        self.ballSep = .1       # Ball separation
        self.eventProc = PoolBallHolderEvent(self)


    def clearTable(self):
        """ Clear holder to empty
        """
        self.clearBalls()
 
        
    #
    # select ball
    # Do we want to keep the same class or make a new one?
    def selectBall(self,
        ball
        ):
        if ball == None:
            return
        self.selectedBall = ball
        if self.trace & 8:
            number = ball.number
            print "selectBall " + str(number)

        
    def unselectBall(self):
    
        if self.trace & 8:
            if self.selectedBall != None:
                number = self.selectedBall
                print "unselectBall " + str(number)
            else:
                print "unselectBall None"
        
        self.selectedBall = None

    def setBallInUse(self,
                    number,
                    inUse=True):
        """Set ball as used
        Returns: ball number, None if no ball found
        """
        if number == None:
            number = self.numberAvailable()
        if number == None:
            return None         # Not or none available
        
        ball = self.getBall(number)
        if ball == None:
            raise RuntimeError("Shouldn't get here - unexpected getBall return")
        ball.setInUse(inUse)
        
        
    def clearBalls(self):
        """ delete balls from table
        Erase ball drawings
        """
        for ball in self.balls:
            ball.erase()
        self.balls = []
        
        
    def clearInUse(self):
        """ clear in use for all balls
        """
        for ball in self.balls:
            ball.setInUse(inUse=False)


    def reset(self):
        self.tableType = self.table.tableType
        self.gameType = self.table.gameType
        self.setBalls()
            
        
    #
    # Select / Create ball if possible
    # Aim if toAim is True
    def selectBall(self,     # Returns ball else None
        ball
        ):
        pass
        return ball


    def setup(self):
        """ Setup holder for play
        """
        self.eventProc.setup()
###        self.setBalls()


    def getBall(self,
                number):
        for ball in self.balls:
            if number == ball.number:
                return ball
        return None                # not found
        
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
    

    
    def rackposition_set (
        self,
        x,
        y,
        theta,
        ):
        """ Setup function for racking
        """
        if theta == None:
            theta = atan2(0,1)      # Left to right
    
        if y == None:    
            y = self.height/2
        if x == None:
            x = self.radius
            
        self.rp_theta = theta
        self.rp_x = x
        self.rp_y = y

    
    def setBalls(self,
        ):
        """ Add balls positioned in line, left to right
            Using rackposition is a bit of a cluge, but its there
            set all balls to "not in use"
        """
        self.clearInUse()
        if self.table.gameType == PoolTable.gameBilliards:
            self.setBallsBilliards()
            return
                    # Calculate size of balls to fit in length and hight
        if self.table.gameType == PoolTable.game8Ball:
            nball = 15+1          # Including cue ball
        elif self.table.gameType == PoolTable.game9Ball:
            nball = 9+1
        else:
            raise Exception("Unsupported game type:{}".format(self.table.gameType))
        
        ball_room = self.length / nball
        ballsize = ball_room - self.ballSep
        if ballsize > self.height - 2*self.ballSep:
            ballsize = self.height - 2*self.ballSep
        ballsize -= 1.0        # Adjust smaller
        self.ballRadius = ballsize/2
        self.clearTable()   # Start with clear table
        y = self.height / 2 + 3*self.ballSep + .75
        for n in range(0, nball):
            x = 2*self.ballSep + ball_room/2 + n * ball_room + .5
            number = n
            ball = HPoolBall(x=x,
                            y=y,
                            radius=self.ballRadius,
                            number=number,
                            table=self,     # Reference to table
                            )
            ball.draw()
            self.balls.append(ball)

    
    def setBallsBilliards(self,
        ):
        """ Add balls positioned in line, left to right
        """
                    # Calculate size of balls to fit in length and hight
        nball = 3
        ball_room = self.height - 3*self.ballSep
        ballsize = ball_room - self.ballSep
        if ballsize > self.height - 2*self.ballSep:
            ballsize = self.height - 2*self.ballSep
        ballsize -= 1.0        # Adjust smaller
        self.ballRadius = ballsize/2
        self.clearTable()   # Start with clear table
        y = self.height / 2 + 3*self.ballSep + .75
        for n in range(0, nball):
            x = 2*self.ballSep + ball_room/2 + n * ball_room + .5
            number = n
            ball = HPoolBall(x=x,
                            y=y,
                            radius=self.ballRadius,
                            number=number,
                            table=self,     # Reference to table
                            )
            ball.draw()
            self.balls.append(ball)


    """
    Setup ball holder
    """
    def setGame(self,
                    gameType,
                    tableType = PoolBall.POOL):
        self.gameType = gameType
        self.tableType = tableType
        self.clearBalls()
        if gameType == PoolTable.game8Ball:
            self.setGame8Ball()
        elif gameType == PoolTable.game9Ball:
            self.setGame9Ball()
        elif gameType == PoolTable.gameBilliards:
            self.setGameBilliards()
        else:
            raise Exception("Non-supported gameType: {}".format(gameType))


    def setGame8Ball(self):
        self.setBalls()
        
    def setGame9Ball(self):
        self.setBalls()
        
    def setGameBilliards(self):
        self.setBalls()
        

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
        ymax = self.height - r
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
    # select available (unused) ball
    def numberAvailable(self):     # Returns: available ball number (0 cue ball), None if none available
        balls = self.balls
        for ball in balls:
            if not ball.inUse:
                return ball.number
            
        return None                # No numbers not in use

    #
    # pick ball and place it on table
    # Note we don't have a single canvas so we will jump ball to closest point
    # on table
    # 
    def pickNewBall(self,     # Returns ball else None
        x,
        y
        ):
        ball = self.insideBall(x,y)
            
        if ball == None:
            return None
        
        if ball.inUse:
            return None
                        # Find closest point on table
        table = self.table
        number = ball.number
        table_x = x
        table_y = table.width - table.ballRadius - .5
        table_ball = table.createSelectBall(table_x, table_y,
                               number = number)        # ??? What if we don't fit
        if table_ball != None:
            self.setBallInUse(number)     # Mark it
        
    def tableEventLocPix(self,
        event
        ):
        xraw = event.x
        yraw = event.y
        cvs = self.cvs
        x_pix = cvs.canvasx(xraw)
        y_pix = cvs.canvasy(yraw)
        return (x_pix,y_pix)


        
        # Scale to pixel value from internal real units
    def scaleFromPix (self,       # Returns: len in cm
           pixlen,
           ):
        return self.table.scaleFromPix(pixlen)
   
   
    # Scale to pixel value from internal real units
    def scaleToPix (self,       # Returns: len in pixels
           reallen,
           ):
       return self.table.scaleToPix(reallen)
    
        


class PoolBallHolderEvent:
    """Control pool table events such as mouse operations
    """
    def __init__(self,
                 holder,     # Associated holder
                 ):
        self.holder = holder
        self.trace = holder.trace    # Easy trace access
        self.cvs = holder.cvs        # Easy drawing access
     
    def setup(self):
        cvs = self.cvs
        cvs.bind("<Button-1>",
                self.holderButton1ClickEvent)
        cvs.bind("<Button-3>",
                 self.holderButton3ClickEvent)
        cvs.bind("<Motion>", self.holderMotionEvent)
        cvs.bind("<ButtonRelease>", self.holderButtonReleaseEvent)


    #
    # Left button click
    #    1. Selects ball if cursor is within ball
    #    2. Creates new ball if not within any ball

    def holderButton1ClickEvent(self,
        event
        ):
            
        (x,y) = self.holderEventLoc(event)
        if self.trace & 8:
            print "button1_click"
            length = self.holder.length
            height = self.holder.height
            lf = x/length
            wf = y/height
            print("x=%.2f(%.2fw), y=%.2f(%.2fw)" % (x, lf, y, wf))
            self.holder.nearEdge(x,y)
        ball = self.holder.insideBall(x,y)
                                        # If in use - pull the ball off the table
        if ball.inUse:
            number = ball.number
            self.holder.table.deleteBall(number)
            self.holder.setBallInUse(number, False);
        else:                       # if not in use place on table
            self.holder.pickNewBall(x,y)
    
        
        
    #
    # Right button click
    #   Aim ball
    #   1. Duplicate Left button click
    #   2. Setup aiming
    #      a. setup aiming arrow line which start aiming process
    #
    def holderButton3ClickEvent(self,
        event
        ):
        if self.trace & 8:
            print "button3_click"
        if self.holder.selectedBall != None:
            return          # Already selected
        
        (x,y) = self.holderEventLoc(event)
        ball = self.holder.createSelectBall(x,y)
        if ball != None:
            self.holder.aimBall(ball, x, y)
    
            
    # Button release
    #  1. if aiming ball shoot it
    #  2. if selected, unselect ball
    def holderButtonReleaseEvent(self,
        event
        ):
        
        "TBD no action for release event yet"
        return
    
        if self.trace & 8:
            print "release_event"
        if self.holder.selectedBall == None:
            print "selectedBall == None"
            return
        
        if self.holder.aimedBall != None:
            (x,y) = self.holderEventLoc(event)        
            self.holder.shootBall(self.holder.aimedBall, x, y)
            self.holder.aimingRemove()
            
        self.holder.unselectBall()
    
    
    
    #
    # holder location of event
    def holderEventLoc(self,
        event
        ):
        (x_pix, y_pix) = self.holderEventLocPix(event)
        x = self.holder.scaleFromPix(x_pix)
        y = self.holder.scaleFromPix(y_pix)
        return (x,y)
    
    #
    # holder location of event in canvas pixels
    def holderEventLocPix(self,
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
    def holderMotionEvent(self,
        event
        ):
        
        "TBD - no motion for ball holder"
        return
    
        (x,y) = self.holderEventLoc(event) 
        if self.trace & 8:
            print_repeat("motion_event")
            self.holder.nearEdge(x,y)
            
        if self.holder.selectedBall == None:
            return          # Noting to do
        if self.holder.aimedBall != None:
            self.holder.aimingUpdate(x,y)
        else:
            self.holder.placeBallMotionEvent(event)
    
         


