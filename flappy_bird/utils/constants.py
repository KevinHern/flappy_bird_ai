# Game
from pygame.transform import scale2x
from pygame.image import load

# Utils
from enum import Enum
from os.path import join, split, dirname


class PipeOrientation(Enum):
    TOP = 1
    BOTTOM = 2


def get_assets_directory():
    return join(split(dirname(__file__))[0], 'assets')


class GameImages:
    BIRD_ANIMATION = [
        scale2x(
            load(join(get_assets_directory(), "bird{}.png".format(x)))
        ) for x in range(1, 4)
    ]
    PIPE = scale2x(load(join(get_assets_directory(), "pipe.png")))
    FLOOR = scale2x(load(join(get_assets_directory(), "floor.png")))
    BACKGROUND = scale2x(load(join(get_assets_directory(), "background.png")))


print(GameImages.BIRD_ANIMATION)
