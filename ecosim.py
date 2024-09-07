from game import Game, ImageLibrary, GameObject, Vector2D
from random import choice, shuffle
import random

class Tile(GameObject):
    def __init__(self, position, game, width=96, height=96, sourceImage=None):
        super().__init__(position, width, height, sourceImage, game)

class DirtTile(Tile):
    def __init__(self, position, game):
        image = ImageLibrary.get('dirt_tile')
        super().__init__(position, game, width=96, height=96, sourceImage=image)
        if random.random() < 0.5:
            Grass(position, game)
    
    def update(self, timeElapsed):
        pass

class SandTile(Tile):
    def __init__(self, position, game):
        super().__init__(position, game, width=96, height=96, sourceImage=ImageLibrary.get('sand_tile'))
        
    def update(self, timeElapsed):
        pass

class Grass(GameObject):
    def __init__(self, position, game):
        width = 96
        height = 96
        sourceImage = ImageLibrary.get('grass_tuft')  
        super().__init__(position, width, height, sourceImage, game)
        self.growth_timer = random.randint(5, 20)

    def update(self, timeElapsed):
        self.growth_timer -= timeElapsed
        if self.growth_timer <= 0:
            self.spread()
            self.growth_timer = random.randint(5, 20)  
    def spread(self):
        pass

class Animal(GameObject):
    def __init__(self, position, game, width, height, sourceImage, speed, energy):
        super().__init__(position, width, height, sourceImage, game)
        self.speed = speed
        self.energy = energy

    def update(self, timeElapsed):
        pass

class Wombat(Animal):
    def __init__(self, position, game):
        width = 96
        height = 96
        sourceImage = ImageLibrary.get('wombat1')
        speed = 10
        energy = 100
        super().__init__(position, game, width, height, sourceImage, speed, energy)

    def update(self, timeElapsed):
        pass

class Snake(Animal):
    def __init__(self, position, game):
        width = 96
        height = 96
        sourceImage = ImageLibrary.get('snake1')
        speed = 15
        energy = 80
        super().__init__(position, game, width, height, sourceImage, speed, energy)
    
    def update(self, timeElapsed):
        pass

class EcoSim(Game):
    
    def __init__(self):
        super().__init__()
        self.tiles = []
        self.animals = []
        self.setup_environment()
    
    def setup_environment(self):
        for y in range(10):
            for x in range(12):
                position = Vector2D(x * 96, y * 96)
                tile_type = DirtTile if random.random() < 0.5 else SandTile
                self.tiles.append(tile_type(position, self))

        for i in range(10): 
            position = Vector2D(random.randint(0, 11) * 96, random.randint(0, 9) * 96)
            self.animals.append(Wombat(position, self))
        for i in range(5): 
            position = Vector2D(random.randint(0, 11) * 96, random.randint(0, 9) * 96)
            self.animals.append(Snake(position, self))


def main():
    ImageLibrary.load('images')  
    ecosim = EcoSim()
    
    ecosim.run()

if __name__ == '__main__':
    main()