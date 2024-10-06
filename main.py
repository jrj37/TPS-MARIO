from settings import *
from level import *
from pytmx.util_pygame import load_pygame
from os.path import join
from game import Game
from support import *

if __name__ == "__main__":               
    game=Game()
    game.run()