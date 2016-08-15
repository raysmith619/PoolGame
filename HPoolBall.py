#!/usr/bin/env python

from PoolBall import *

#
# HPoolBall is a pool ball place holder the holder
# TBD - may go into its own file later
class HPoolBall(PoolBall):
    """Pool Ball place holder in the holder
    """
    inUseTagName = "tag_in_use"

    def __init__(self,
        number = 0,     # Ball number REQUIRED 0 == cue ball
        color = None,
        x = 0.0,        # X position, in cm
        y = 0.0,        # Y position, in cm/sec
        radius = None,  # ball radius - ??? better than global
        table = None,
        inUse = False,  # True => ball is in use, likely on the table
        ):
        PoolBall.__init__(self,
                          number=number,
                          color=color,
                          x=x,
                          y=y,
                          radius=radius,
                          table=table,
                         )
        self.inUse = inUse
        self.inUseTag = None


    # createLine - Canvas create_line in abstract dimentions
    # pixWidth - with in pixels
    # TBD to move to PoolBall or PoolTable...
    def createLine(self,
                   x0, y0, x1, y1,
                   tag = "createLine_DEFAULT_TAG",
                   pixWidth = 1,        # Pixel width
                  ):
            cvs = self.cvs
            x0_pix = self.scaleToPix(x0)
            y0_pix = self.scaleToPix(y0)
            x1_pix = self.scaleToPix(x1)
            y1_pix = self.scaleToPix(y1)
            cvs.create_line(x0_pix, y0_pix,
                         x1_pix,
                         y1_pix,
                         width = pixWidth,
                         tag = tag, 
                         )
    

            
    def draw(self):
        """ draw ball indicating inUse state
        Initially we will draw basic ball with annotations indicating use
        """
        super(HPoolBall, self).draw()        # draw basic ball
                                # Draw X through ball if in use
                                #   p1      p3
                                #     \     /
                                #      \   /
                                #        x
                                #       /  \
                                #      /    \
                                #    p4      p2
        if self.inUse:
            x = self.x
            y = self.y
            r = self.radius
            cvs = self.cvs
            tag = HPoolBall.inUseTagName + str(self.number)
            self.inUseTag = tag
            
            p1_x = x - r
            p1_y = y - r
            p2_x = x + r
            p2_y = y + r
            self.createLine(p1_x,p1_y,
                       p2_x,p2_y,
                       tag = tag,
                       pixWidth = 2,
                       )
            
            p3_x = x + r
            p3_y = y - r
            p4_x = x - r
            p4_y = y + r
            self.createLine(p3_x,p3_y,
                       p4_x,p4_y,
                       tag = tag,
                       pixWidth = 2,
                       )
            
            
    # Clear any in use attributes
    def inUseClear(self):
        if self.inUseTag != None:
            self.cvs.delete(self.inUseTag)
            self.inUseTag = None
        self.inUse = False
    
    def setInUse(self,
                 inUse):
        self.inUseClear()       # Clear previous setting
        self.inUse = inUse
        self.draw()
