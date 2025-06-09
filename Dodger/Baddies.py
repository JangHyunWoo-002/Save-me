# Baddies.py
import pygame
import pygwidgets
import random
from Constants import *
from FallingObject import FallingOb # Import FallingObject

# Baddie class
class Baddie(FallingOb): # Inherit from FallingObject
    BADDIE_IMAGE_PATH = 'images/baddie.png' # Define image path here

    def __init__(self, window):
        super().__init__(window, Baddie.BADDIE_IMAGE_PATH) # Call parent constructor
        self.x = random.randrange(0, WINDOW_WIDTH - self.size) # Specific initial x

    def _set_initial(self):
        self.y = 0 - self.size # start above the window

    def _check_offscreen(self):
        return self.y > GAME_HEIGHT # Needs to be deleted

    def get_score(self):
        return POINTS_FOR_BADDIE_EVADED # Specific points for Baddie


# BaddieMgr class (no changes needed here as it manages FallingObjects)
class BaddieMgr():
    ADD_NEW_BADDIE_RATE = 8  # how often to add a new Baddie

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):  # called when starting a new game
        self.baddiesList = []
        self.nFramesTilNextBaddie = BaddieMgr.ADD_NEW_BADDIE_RATE

    def update(self):
        # Tell each Baddie to update itself
        # Count how many Baddies have fallen off the bottom.
        nBaddiesRemoved = 0
        baddiesListCopy = self.baddiesList.copy()
        for oBaddie in baddiesListCopy:
            deleteMe = oBaddie.update()
            if deleteMe:
                self.baddiesList.remove(oBaddie)
                nBaddiesRemoved = nBaddiesRemoved + 1

        # Check if it's time to add a new Baddie
        self.nFramesTilNextBaddie = self.nFramesTilNextBaddie - 1
        if self.nFramesTilNextBaddie == 0:
            oBaddie = Baddie(self.window)
            self.baddiesList.append(oBaddie)
            self.nFramesTilNextBaddie = BaddieMgr.ADD_NEW_BADDIE_RATE

        # Return that count of Baddies that were removed
        return nBaddiesRemoved

    def draw(self):
        for oBaddie in self.baddiesList:
            oBaddie.draw()

    def hasPlayerHitBaddie(self, playerRect):
        for oBaddie in self.baddiesList:
            if oBaddie.collide(playerRect):
                return True
        return False