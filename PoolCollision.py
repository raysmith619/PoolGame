#!/usr/bin/env python

import time
from math import *
from random import *
from copy import *

PI = 3.141592653589
ballNumberMax = 20          # Maximum nunmber of balls
stick_to_xmax = 0  # 1 - stick to xmax if hit
stick_to_ymax = 0  # 1 - stick to ymax if hit
tracecollisions = []

###################################################################
# Support Functions
###################################################################

def n (      # Returns: short formatted number
    n,
    ndig,
    ):
    ndig = 1 if ndig == None else ndig
    fmt = "%." + ndig + "f"
    str = fmt % n;
    return str

# List collision history
def list_hist():
    
    global tracecollisions
    
    start_running(0)
    print("\nCollision History")
    for h in tracecollisions:
        r_b = h['_ball']
        r_b2 = h['_ball2']
        time = n(h['__time'],3)
        sep = n(h['__sep'],3)
        vx1 = n(r_b['_vx'])
        print(time, sep, " (r_b['_number'])  vx=" + vx1,
        " vy=" + n(r_b['_vy']),
        " (r_b2['_number']) v2x=" . n(r_b2['_vx']),
        " v2y=" . n(r_b2['_vy']))

        print("                   ",
        "vN=" + n(h['_vN']) + " vT=" + n(h['_vT']),
        "     v2N=" + n(h['_v2N']) + " v2T=" + n(h['_v2T']))

        print("                   "
        + "vN_A=" + n(h['_vN_A']) + " vT_A=" + n(h['_vT_A'])
        + "    v2N_A=" + n(h['_v2N_A']) + " v2T_A=" + n(h['_v2T_A']))


        r_A = h['_ball_A']
        r_A2 = h['_ball2_A']
        print(" " * 19,
        "vx=" . n(r_A['_vx']),
        + " vy=" . n(r_A['_vy'])
        + " (r_A2['_vy']) v2x=" . n(r_A2['_vx'])
        + " v2y=" . n(r_A2['_vy']))


#######################################################################################################
# Geometry support functions
#######################################################################################################

# Do coordiante rotation
def xyrot (         # Returns: (x', y')
    thetaRot,  # Rotation in x,y coord
    x,         # x value  in "
    y,         # y value
        ):

    r = sqrt(x*x + y*y)
    xp = r*cos(thetaRot)
    yp = -r*sin(thetaRot)
    return (xp,yp)

# Add two vectors
def vsum (         # Returns: (x,y) vector sum
    x1,       # Vector1 x component               
    y1,       # Vector1 y component
    x2,       # Vector2 x component
    y2,       # Vector2 y component
    ):

    return (x1+x2, y1+y2)
# Add two vectors in theta, R coordinates
def vRsum (         # Returns: (x,y) vector sum
    theta1,   # Vector1 theta component               
    r1,       # Vector1 r component
    theta2,    # Vector2 theta component
    r2,       # Vector2 r component
    ):

    x1 = r1*cos(theta1)
    y1 = r1*sin(theta1)
    x2 = r2*cos(theta2)
    y2 = r2*sin(theta2)
    return (x1+x2, y1+y2)
# Add vectors first in theta, R coordinates, second in x,y
def vRsumxy (         # Returns: (x,y) vector sum
    theta1,   # Vector1 theta component               
    r1,       # Vector1 r component
    x2,       # Vector2 x component
    y2,       # Vector2 y component
    ):

    x1 = r1*cos(theta1)
    y1 = r1*sin(theta1)
    return (x1+x2, y1+y2)


class PoolCollision:
############################################################################
# Process Collisions
###########################################################################
    def __init__(self,
                 trace = 0,
                 table=None,
                 balls = [],
###                ballNumberMax = PoolCollision.ballNumberMax
                ):
        self.trace = trace          # Set  voa PoolTable.setCollision
        self.table = table
        self.balls = balls
        self.ballNumberMax = ballNumberMax
        self.prevCollisionBall = None
        
    def updateVelocities (self,
                          balls = None):      # Default to all
        """
        Update velocity of all balls
        Simple at first, then looking for interactions
        """
        if balls == None:
            balls = self.table.balls
                
        for ball in balls:
            ball.ballCollh = [False] * (self.ballNumberMax + 1) # Clear interaction flags
                
        for ball in balls:
            self.collisionEdge(ball)        # Ck for and adjust for edge colisions
            self.collisionBalls(ball)       # Ck for and adjust     for ball collisions
        return balls                        # Returns list of balls
        
    # Update position of balls based on current velocities
    # Leave collision checks for update_velocities
    def updatePositions (self,
        update_time,            # Time since last update
        balls = None
        ):
        if balls == None:
            balls = self.table.balls
        
        for ball in balls:
                                # Update energy
            mdissloss = self.table.mdissloss
            if mdissloss != 0.0:
                vx = ball.vx
                vy = ball.vy
                vsq = vx**2 + vy**2
                v = sqrt(vsq)
                vsq2 = vsq * (1.0 - mdissloss)
                v2 = sqrt(vsq2)
                vx2 = 0.
                vy2 = 0.
                if v > .0001 and v2 > .0001:
                    vx2 = vx * v2/v
                    vy2 = vy * v2/v
                ball.vx = vx2
                ball.vy = vy2
                
            dx = update_time*ball.vx
            ball.x += dx
    
            dy = update_time*ball.vy
            ball.y += dy
        return balls
    
        
    # Update balls
    def updateBalls(self,
        update_time,            # Time since last update
        balls = None
        ):
        if balls == None:
            balls = self.table.balls
        self.updateVelocities(balls=balls)
        self.updatePositions(update_time,balls=balls)
   
            
    def collisionBall(self,
        ball,
        ball2,
        ):
        """
        Check for collision with one other ball,
        updating velocity if appropriate
        """
        ballNumber = ball.number
        ball2Number = ball2.number
        ballCollh = ball.ballCollh
    
        if ballCollh[ball2Number-1]:
            return                     # Already interacted
    
        ball2.ballCollh[ballNumber-1] = True   # Record we have delt with this ball
    
        x = ball.x
        y = ball.y
        r = ball.radius     # Assuming equal
        vx = ball.vx
        vy = ball.vy
        vMag = sqrt(vx*vx + vy*vy)
    
        x2 = ball2.x
        y2 = ball2.y
        r2 = ball2.radius
        v2x = ball2.vx
        v2y = ball2.vy
        v2Mag = sqrt(v2x*v2x + v2y*v2y)
    
        dx = x-x2
        dy = y-y2
        dsepsq = dx*dx + dy*dy
        sep = ball.ballSep(ball2)
    
        if (sep >= 0):
            return               # No collision
    
    
        locTheta = atan2(y2-y, x2-x)
        tanTheta = locTheta + PI/2
        loc2Theta = atan2(y-y2, x-x2)  # Going from ball 2
        tan2Theta = loc2Theta + PI/2
    
        if (self.trace & 0x01):
            print("vx,vy = (", vx, vy, "), v2x,v2y = (", v2x, v2y, ")")
            print("x,y = (", x, y, "),", x2, y2, " = (", x2, y2, "), sep =", sep)
        # Adjustment to avoid overlap
            # Backoff fastest moving ball amount of separation
        if (sep < 0):
            msep = -sep         # Absolute separation
            msep += 1e-5              # Small fudge
        if (vMag >= v2Mag):
            if (x < x2):
                ball.x  -= abs(cos(locTheta)*msep)
            else:
                ball.x  += abs(cos(locTheta)*msep)
            if (y < y2):
                ball.y -= abs(sin(locTheta)*msep)
            ball.y += abs(sin(locTheta)*msep)
        else:
            if (x2 < x):
                ball2.x  -= abs(cos(loc2Theta)*msep)
            else:
                ball2.x  += abs(cos(loc2Theta)*msep)
            if (y2 < y):
                ball2.y -= abs(sin(loc2Theta)*msep)
            else:
                ball2.y += abs(sin(loc2Theta)*msep)
                    
        sep_A = ball.ballSep(ball2)
        if (self.trace & 0x01):
            print("After backoff: sep=", sep_A,)
    # TBD           " x1,y1:(", ball.x, ball.y,
    #            " x2,y2:(", ball2.x, ball2.y
    
            if (sep_A < 0):
                print("We're overlapping by ", sep_A)
                print("cos(", loc2Theta, cos(loc2Theta), )
                print("sin(\loc2Theta):", sin(loc2Theta))
        if (self.trace & 1):
            print("Collision ball.number=ball2.number")
                            # Do ball pair, updating then and keeping
                            # record in each ball indicating the pair has been
                            # delt with
                            # Calculate line of centers
                            # center to center point normalized
                            # sine of center to center
    
    
    
    
    
        loc = r*2
        vTheta = atan2(vy, vx)
        locVTheta = locTheta - vTheta    # Angle v to loc
        (vN, vT) = xyrot(locVTheta, vx, vy)
        if (self.trace & 0x01):
            print("vTheta=vTheta, locTheta=locTheta, locVTheta=locVTheta")
    
        print("vN=",vN, "vT=",vT)
                                                # Ball 2
        v2Theta = atan2(v2y, v2x)
        locV2Theta = locTheta - v2Theta    # Angle v to loc(ball 1)
    
        if (self.trace & 0x01):
            print("loc2Theta=loc2Theta, v2Theta=v2Theta, locV2Theta=locV2Theta, v2Mag=v2Mag")
        (v2N, v2T) = xyrot(locV2Theta, v2x, v2y)
    
                                                # v1AN = v2N, v2AT = v1T
        vN_A = v2N
        vT_A = vT
        v2N_A = vN
        v2T_A = v2T
    
        if (self.trace & 0x01):
            print("vN  =vN,   vT  = vT,  v2N = v2N,   v2T = v2T")
            print("vN_A=vN_A, vT_A=vT_A, v2N_A=v2N_A, v2T_A = v2T_A")
                                                # Add new components
                                                # To get resulting 
        (vx_A, vy_A) = vRsum(locTheta, vN_A, tanTheta, vT_A)
    
        (v2x_A, v2y_A) = vRsum(locTheta, v2N_A, tanTheta, v2T_A)
    
        t = {}
        if (self.trace):
            t['sep'] = sep
            t['time'] = time.time
            t['ball'] = ball        # Can't do deepcopy
            t['ball2'] = ball2      # Can't do deepcopy
            t['vN'] = vN
            t['vT'] = vT
            t['v2N'] = v2N
            t['v2T'] = v2T
            t['vN_A'] = vN_A
            t['vT_A'] = vT_A
            t['v2N_A'] = v2N_A
            t['v2T_A'] = v2T_A
        ball.vx = vx_A
        ball.vy = vy_A
        ball.ballCollh[ball2Number-1] = True   # Record we have
                                                # delt with this ball
    
        ball2.vx = v2x_A
        ball2.vy = v2y_A
                                                # delt with this ball
        if (self.trace):
            t['ball_A'] = ball      # Can't do deepcopy
            t['ball2_A'] = ball     # Can't do deepcopy
            tracecollisions.append(t)
        if (self.trace & 0x01):
            print("vx,vy[after] = (vx_A,vy_A), v2x,v2y = (v2x_A,v2y_A)")
        if (self.trace & 0x01):
            print("Ball collision updated")
    
    
    # Check for collision with all other balls,
    def collisionBalls(self,
        ball,
        balls = None
        ):
        if balls == None:
            balls = self.table.balls
        
        for ball2 in balls:
            id = 0
            id2 = 0
            if ball.id != None:
                id = ball.id
            if ball2.id != None:
                id2 = ball2.id
            if id and id2 and id != id2:
                self.collisionBall(ball, ball2)
    
    
    # Check for collision with all other balls,
    def collisionEdge(self,
        ball,
        ):
        
        x = ball.x
        y = ball.y
        vx = ball.vx
        vy = ball.vy
        r = ball.radius
    
        xmax = self.table.length - r
        xmin = r
        ymax = self.table.width - r
        ymin = r
    
        col_xmax = False
        col_xmin = False
        col_ymax = False
        col_ymin = False
        
        if x > xmax:
            if vx > 0:
                vx = -vx
                col_xmax = True
                if stick_to_xmax:
                    vx = 0
                x = xmax
    
        if (x < xmin):
            if vx < 0:
                col_xmin = True
                vx = -vx
            x = xmin
    
        if y >= ymax:
            if vy > 0:
                col_ymax = True
                vy = -vy
            if stick_to_ymax:
                vy = 0
            y = ymax
    
        if y <= ymin:
            if vy < 0:
                col_ymin = True
                vy = -vy
            y = ymin
    
                                                                # Update ball state
        ball.x = x
        ball.y = y
        ball.vx = vx
        ball.vy = vy
        if self.trace & 0x10:
            if col_xmin or col_xmax or col_ymin or col_ymax:
                ##self.bankLoss(ball)TBD
                if self.prevCollisionBall != None:
                    self.prevCollisionBall.unmarkPosition()
                    
                ball.markPosition()
                self.prevCollisionBall = ball
                time_rel = time.time() - self.table.timeBeg
                time_rel_str = "%.2f" % time_rel
                print("")
                if col_xmin:
                    print("col_xmin: t=" + time_rel_str + " x=" + str(x/r) + "r")
                if col_xmax:
                    print("col_xmax: t=" + time_rel_str + "  x=" + str((self.table.length-x)/r) + "r")
                print("collision edge: ball" + str(ball.number)
                + " x=" + str(ball.x) +  " vx=" + str(ball.vx)
                + " y=" , str(ball.y) +  " vy=" + str(ball.vy)
                )
                print("")



