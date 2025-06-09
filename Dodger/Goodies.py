# Goodies.py
import pygame
import pygwidgets
import random
from Constants import *
from FallingObject import FallingOb # Import FallingObject

class Goodie(FallingOb): # Inherit from FallingObject
    GOODIE_IMAGE_PATH = 'images/goodie.png' # Define image path here
    RIGHT = 'right'
    LEFT = 'left'

    def __init__(self, window):
        super().__init__(window, Goodie.GOODIE_IMAGE_PATH) # Call parent constructor
        self.y = random.randrange(0, GAME_HEIGHT - self.size) # Specific initial y

        self.direction = random.choice([Goodie.LEFT, Goodie.RIGHT])
        if self.direction == Goodie.LEFT:  # start on right side of the window
            self.x = WINDOW_WIDTH
            self.speed = - random.randrange(FallingOb.MIN_SPEED, # Use FallingObject's speed constants
                                                            FallingOb.MAX_SPEED + 1)
            self.minLeft = - self.size
        else:  # start on left side of the window
            self.x = 0 - self.size
            self.speed = random.randrange(FallingOb.MIN_SPEED, # Use FallingObject's speed constants
                                                          FallingOb.MAX_SPEED + 1)

    def _initial_position(self):
        # Position is set in __init__ based on direction
        pass

    def update(self):
        self.x = self.x + self.speed # Goodies move horizontally
        self.image.setLoc((self.x, self.y))
        return self._check_offscreen()

    def _check_offscreen(self):
        if self.direction == Goodie.LEFT:
            return self.x < self.minLeft  # needs to be deleted
        else:
            return self.x > WINDOW_WIDTH # needs to be deleted

    def get_score(self):
        return POINTS_FOR_GOODIE # Specific points for Goodie


class GoodieMgr():
    GOODIE_RATE_LO = 90
    GOODIE_RATE_HI = 111

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):  # Called when starting a new game
        self.goodiesList = []
        self.nFramesTilNextGoodie = GoodieMgr.GOODIE_RATE_HI

    def update(self, thePlayerRect):
        # Tell each Goodie to update itself.
        # If a Goodie goes off an edge, remove it
        # Count up all Goodies that contact the player and remove them.
        nGoodiesHit = 0
        goodiesListCopy = self.goodiesList.copy()
        for oGoodie in goodiesListCopy:
            deleteMe = oGoodie.update()
            if deleteMe:
                self.goodiesList.remove(oGoodie)  # remove this Goodie

            elif oGoodie.collide(thePlayerRect):
                self.goodiesList.remove(oGoodie)  # remove this Goodie
                nGoodiesHit = nGoodiesHit + 1
        
        # If the correct amount of frames have passed,
        # add a new Goodie (and reset the counter)
        self.nFramesTilNextGoodie = self.nFramesTilNextGoodie - 1
        if self.nFramesTilNextGoodie == 0:
            oGoodie = Goodie(self.window)
            self.goodiesList.append(oGoodie)
            self.nFramesTilNextGoodie = random.randrange(
                                                            GoodieMgr.GOODIE_RATE_LO,
                                                            GoodieMgr.GOODIE_RATE_HI)

        return nGoodiesHit  # return number of Goodies that contacted player

    def draw(self):
        for oGoodie in self.goodiesList:
            oGoodie.draw()