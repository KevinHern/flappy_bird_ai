# Utils
import numpy as np
from flappy_bird.utils.constants import GameImages


class GameFloor:
    FLOOR_VELOCITY = np.array([5, 0])
    IMAGE = GameImages.FLOOR
    WIDTH = GameImages.FLOOR.get_width()

    def __init__(self, height):
        # Initializing the position of 2 background tiles to make the illusion of ground moving
        self.position_floor_tile1 = np.array([0, height])
        self.position_floor_tile2 = np.array([GameFloor.WIDTH, height])

    def draw(self, game_window):
        # Moving both tiles
        self.position_floor_tile1 = np.subtract(self.position_floor_tile1, GameFloor.FLOOR_VELOCITY)
        self.position_floor_tile2 = np.subtract(self.position_floor_tile2, GameFloor.FLOOR_VELOCITY)

        # Check if Tile 1 needs to be moved to the right
        if self.position_floor_tile1[0] + GameFloor.WIDTH < 0:
            self.position_floor_tile1[0] = self.position_floor_tile2[0] + GameFloor.WIDTH

        # Check if Tile 1 needs to be moved to the right
        if self.position_floor_tile2[0] + GameFloor.WIDTH < 0:
            self.position_floor_tile2[0] = self.position_floor_tile1[0] + GameFloor.WIDTH

        # Drawing background
        game_window.blit(GameFloor.IMAGE, self.position_floor_tile1)
        game_window.blit(GameFloor.IMAGE, self.position_floor_tile2)
