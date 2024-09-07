from game import Game, ImageLibrary, GameObject, Vector2D
from random import choice, shuffle
import random

class Tile(GameObject):
    def __init__(self, position, game, width=96, height=96, sourceImage=None):
        super().__init__(position, width, height, sourceImage, game)

class EcoSim(Game):
    
    def __init__(self):
        super().__init__()


def main():
    ImageLibrary.load('images')  
    ecosim = EcoSim()
    
    ecosim.run()

if __name__ == '__main__':
    main()