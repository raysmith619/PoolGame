#!/usr/bin/env python

#
# Pool Ball object
# Encapsulate Abstract operation of a pool ball
#

from math import *
from Tkinter import *

from PoolTable import *
from PoolCollision import *


 
class PoolBall(object):
    """ Data and functions to support operation and view of a pool ball
    """
                                # Ball/table type
    POOL = 1
    BILLIARD = 2
    
    item_number = 0
    aimingTagName = "tag_aiming"
    markTagName = "tag_mark"
    prevCollisionBall = None
    
    PoolBallColors = [
        'white',        # 0 == cue ball
        'yellow',       # 1 == yellow
        'blue',
        'red',
        'purple',
        'orange',
        'green',
        'maroon',
        'black',
        'yellow',
        'blue',
        'red',
        'purple',
        'orange',
        'green',
        'maroon',
    ]
    BilliardBallColors = [
        'white',        # 0 == cue ball
        'yellow',       # 1 == yellow
        'red',
    ]
     
    def __init__(
        self,
        number = 0,     # Ball number REQUIRED 0 == cue ball
        color = None,
        x = 0.0,        # X position, in cm
        y = 0.0,        # Y position, in cm/sec
        vx = 0.0,       # X velocity, in cm/sec
        vy = 0.0,       # Y velocity in cm/sec
        radius = None,  # ball radius - ??? better than global
        table = None,
                        # spin ???
        ):
        self.number = number
        self.table = table
        self.tableType = table.tableType
        
        if color == None:
            color = self.ballColor(number)
        self.color = color
        self.x = x
        self.x0 = x
        self.y = y
        self.y0 = y
        self.vx = vx
        self.vy = vy
        self.isDrawn = False
        self.item_number = 0
        self.id = None
        self.table = table
        self.tableType = table.tableType
        self.trace = table.trace    # To simplify trace access
        self.cvs = table.cvs        # To simplify display access
        self.radius = table.ballRadius
        self.doStripes = True
        self.isAiming = False
        self.aimingTag = None
        
    def getColor(self):
        return self.color
    def getNumber(self):
        return self.number
    def getRadius(self):
        return self.radius
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getVx(self):
        return self.vx
    def getVy(self,):
        return self.vy
    def getCvs(self):
        return self.table.cvs()

    def update(self):
        """Update ball state
        """

 
         

    def ballSep(self,
        ball,
        ):
    ### Calculate ball separation from edge of other ball
    ###
        x = self.x
        y = self.y
        r = self.radius
        x2 = ball.x
        y2 = ball.y
        r2 = ball.radius
    
        dx = x2-x
        dy = y2-y
        sep = sqrt(dx*dx+dy*dy) - r - r2
        return sep


    def inside(self,
               x,
               y):
        """ Determine if point is inside ball
        """
        ballx = self.x
        bally = self.y
        radius = self.radius
        radius_sq = radius*radius
        dist_sq = (ballx-x)*(ballx-x)+(bally-y)*(bally-y)
        if dist_sq < radius_sq:
            return True
        
        return False
        
    def moveTo(
        self,
        x,
        y,
        vx = 0.0,
        vy = 0.0,
        ):
        """ Move ball to place
            Default velocity is 0,0
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        
    
    def draw(
        self,
        ):
        """Draw ball with current attributes
        Create graphic if none, else move to location
        """
        id = self.id
        if not self.isDrawn:
            id = self.createBall()
        if id == None:
            return None             # Can't create
        
        x = self.x
        y = self.y
        x0 = self.x0
        y0 = self.y0

                            # Skip drawing if unchanged
###        if self.isDrawn and x == x0 and y == y0:
###            return self
        
###        xdelta = self.scaleToPix(x-x0)
###        ydelta = self.scaleToPix(y-y0)

        x0_pix = self.scaleToPix(x0)
        x_pix = self.scaleToPix(x)
        y0_pix = self.scaleToPix(y0)
        y_pix = self.scaleToPix(y)

        xdelta = x_pix - x0_pix
        ydelta = y_pix - y0_pix
        cvs = self.cvs
        cvs.move(id, xdelta, ydelta)
        self.x0 = x
        self.y0 = y
        self.isDrawn = True    # Flag as drawn
        return self

    #
    # Mark with circle
    def markPosition(self):
        r = self.radius
        x = self.x
        y = self.y
        cvs = self.cvs
        cvs.create_oval(
            self.scaleToPix(x-r),
            self.scaleToPix(y-r),
            self.scaleToPix(x+r),
            self.scaleToPix(y+r),
#            fill = "purple",
            dash = (3,5),
            tags = PoolBall.markTagName,
            )
        self.prevCollisionBall = self

    #
    # Remove previous mark
    def unmarkPosition(self):
        r = self.radius
        x = self.x
        y = self.y
        cvs = self.cvs
        tag = PoolBall.markTagName
        cvs.delete(tag)

        

# Aim ball, Drawing aiming attributes
    def aim(self,
                    x,
                    y):
        """Drawing aiming attributes
        """
        x0 = self.x
        y0 = self.y
        x0_pix = self.scaleToPix(x0)
        y0_pix = self.scaleToPix(y0)
        x_pix = self.scaleToPix(x)
        y_pix = self.scaleToPix(y)
        r = self.radius
        r_pix = self.scaleToPix(r)
        
        tag = PoolBall.aimingTagName
        self.isAiming = True            # Flag as aiming
                                        # erase any previous aiming
        if self.aimingTag != None:
            self.cvs.delete(self.aimingTag)
            
        self.aimingTag = tag                # Markig as aiming
        cvs = self.cvs
        cvs.create_line(x0_pix, y0_pix,
                         x_pix,
                         y_pix,
                         arrow= 'last',
                         tag = tag 
                         )
        cvs.create_oval(
                     x_pix-r_pix,
                     y_pix-r_pix,
                     x_pix+r_pix,
                     y_pix+r_pix,
                     tag = tag
                     )


    # Clear any aiming attributes
    def aimClear(self):
        if self.aimingTag != None:
            self.cvs.delete(self.aimingTag)
        self.isAiming = False

   #
    # color ball by number
    def ballColor(self,     # Returns: ball collor
        number,         # Ball number
        ):
        if self.tableType == PoolBall.BILLIARD:
                if number < 0 or number >= len(PoolBall.BilliardBallColors):
                        number = 0
                return PoolBall.BilliardBallColors[number]
        else:
                if number < 0 or number >= len(PoolBall.PoolBallColors):
                        number = 0
                return PoolBall.PoolBallColors[number]
                
    
# Create ball and draw ball graphic
# 
    def createBall(        # Returns: graphic id/flag else None if can't create
        self,
        ):
        """ Create and draw ball graphic
        """
        number = self.number
        color = self.color
        r = self.radius
        PoolBall.item_number+=1          # TBD - need singleton
        self.item_number = PoolBall.item_number
        item_tag = "item_" + str(self.item_number)
        x = self.x
        y = self.y
        cvs = self.cvs
        underline = 0
        if number == 6 or number == 9:
            underline = 1
        rNumCirc = r*.4      # Number circle
        rNumSize = self.scaleToPix(rNumCirc)*1.2

        cvs.create_oval(
            self.scaleToPix(x-r),
            self.scaleToPix(y-r),
            self.scaleToPix(x+r),
            self.scaleToPix(y+r),
            fill = color,
            tags = item_tag,
                     )
        if number > 8:
            color_outer = "white"
            x0 = x-r
            y0 = y-r
            x1 = x+r
            y1 = y+r
            x0_pix = self.scaleToPix(x0)
            y0_pix = self.scaleToPix(y0)
            x1_pix = self.scaleToPix(x1)
            y1_pix = self.scaleToPix(y1)
            cvs.create_oval(
                 x0_pix,
                 y0_pix,
                 x1_pix,
                 y1_pix,
                 fill = color_outer,
                 tags = item_tag,
                 )

            if (self.doStripes):
                                   # Striped balls
                thdeg = 35
                th = thdeg/360.*2*pi
                (p1x, p1y) = vRsumxy(th,r,x,y)
                (p2x, p2y) = vRsumxy(PI-th,r,x,y)
                (p3x, p3y) = vRsumxy(PI+th,r,x,y)
                (p4x, p4y) = vRsumxy(-th,r,x,y)
                p1x_pix = self.scaleToPix(p1x)
                p1y_pix = self.scaleToPix(p1y)
                p2x_pix = self.scaleToPix(p2x)
                p2y_pix = self.scaleToPix(p2y)
                p3x_pix = self.scaleToPix(p3x)
                p3y_pix = self.scaleToPix(p3y)
                p4x_pix = self.scaleToPix(p4x)
                p4y_pix = self.scaleToPix(p4y)
                """ adjust rectangle                
                sadj = 1
                if (p1x < x):
                    p1x_pix += sadj
                else:
                    p1x_pix -= sadj
                    
                if (p1y < y):
                    p1y_pix += sadj
                else:
                    p2y_pix -= sadj
                    
                if (p2x < x):
                    p2x_pix += sadj
                else:
                    p2x_pix -= sadj
                    
                if (p2y < y):
                    p2y_pix += sadj
                else:
                    p2y_pix -= sadj
                    
                if (p3x < x):
                    p3x_pix += sadj
                else:
                    p3x_pix -= sadj
                    
                if (p3y < y):
                    p3y_pix += sadj
                else:
                    p3y_pix -= sadj
    
                if (p4x < x):
                    p4x_pix += sadj
                else:
                    p4x_pix -= sadj
    
                if (p4y < x):
                    p4y_pix += sadj
                else:
                    p4y_pix -= sadj
                """                    
                cvs.create_rectangle(
                      p2x_pix+1,
                      p2y_pix+2,
                      p4x_pix-1,
                      p4y_pix-1,
                      fill = color,
                      outline = color,
                      tags = item_tag
                        )
                    
                cvs.create_arc(       # left side
                      x0_pix+1,
                      y0_pix,
                      x1_pix,
                      y1_pix,
                      fill = color,
                      outline = color,
                      tags = item_tag,
                      style = CHORD,
                      start = -thdeg-180.,
                      extent = 2*thdeg
                        )
                    
                cvs.create_arc(       # right side
                      x0_pix,
                      y0_pix,
                      x1_pix-1,
                      y1_pix,
                      fill = color,
                      outline = color,
                      tags = item_tag,
                      style = CHORD,
                      start = -thdeg,
                      extent = 2*thdeg
                        )
                
        if self.tableType == PoolBall.POOL and number != 0:
            cvs.create_oval(
            self.scaleToPix(x-rNumCirc),
            self.scaleToPix(y-rNumCirc),
            self.scaleToPix(x+rNumCirc),
            self.scaleToPix(y+rNumCirc),
            fill = 'white',
            tags = item_tag)


            cvs.create_text(
                self.scaleToPix(x),
                self.scaleToPix(y),
                text = str(self.number),
        ###            weight = 'bold',
        ###            size = rNumSize,
        ###            underline = underline,
                fill = 'black',
                tags = item_tag
                )

        self.id = item_tag     # Use tag
        return item_tag
    
        
        
    def erase(self):
        if self.isDrawn:
            id = self.id
            cvs = self.cvs
            cvs.delete(id)
            self.isDrawn = False
            self.id = None


 
        
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
