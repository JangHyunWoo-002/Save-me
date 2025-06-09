# FallingObject.py
import pygame
import pygwidgets
import random
from abc import ABC, abstractmethod  # Import ABC and abstractmethod
from Constants import *

class FallingOb(ABC): # Inherit from ABC to make it an abstract class
    MIN_SIZE = 10
    MAX_SIZE = 40
    MIN_SPEED = 1
    MAX_SPEED = 8

    def __init__(self, window, image_path):
        self.window = window
        self.image_path = image_path
        self.size = random.randrange(FallingOb.MIN_SIZE, FallingOb.MAX_SIZE + 1)
        self.speed = random.randrange(FallingOb.MIN_SPEED, FallingOb.MAX_SPEED + 1)

        self.image = pygwidgets.Image(self.window, (0, 0), self.image_path)
        percent = (self.size * 100) / FallingOb.MAX_SIZE
        self.image.scale(percent, False)

        self.x = 0
        self.y = 0
        self._initial_position() # Call a helper method for initial position

    @abstractmethod
    def _initial_position(self):
        # This method will be implemented by subclasses to set initial x, y
        pass

    def update(self):
        # This update is common for both Baddies and Goodies falling/moving
        self.y = self.y + self.speed
        self.image.setLoc((self.x, self.y))
        return self._check_offscreen() # Abstract method for offscreen check

    @abstractmethod
    def _check_offscreen(self):
        # This method will be implemented by subclasses to check if offscreen
        pass

    def draw(self):
        self.image.draw()

    def collide(self, playerRect):
        return self.image.overlaps(playerRect)

    @abstractmethod
    def get_score(self):
        # To be implemented by subclasses for specific points
        pass