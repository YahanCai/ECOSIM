from game import Game, ImageLibrary, GameObject, Vector2D
from random import choice, shuffle
import random

class Tile(GameObject):
    """
    Represents a base tile in the ecosystem simulation. This is an abstract class for other specific tile types.
    """
    def __init__(self, position, game, width=96, height=96, sourceImage=None):
        """
        Initializes the tile with a position, size, image, and game reference.
        """
        super().__init__(position, width, height, sourceImage, game)

class DirtTile(Tile):
    """
    Represents a dirt tile that may grow grass in the ecosystem.
    """
    def __init__(self, position, game):
        """
        Initializes the dirt tile and has a 50% chance to grow grass on top.
        """
        image = ImageLibrary.get('dirt_tile')
        super().__init__(position, game, width=96, height=96, sourceImage=image)
        if random.random() < 0.5:
            Grass(position, game)
    
    def update(self, timeElapsed):
        """
        Updates the dirt tile over time.
        """
        pass

class SandTile(Tile):
    """
    Represents a sand tile in the ecosystem. Sand cannot grow grass.
    """
    def __init__(self, position, game):
        """
        Updates the sand tile over time.
        """
        super().__init__(position, game, width=96, height=96, sourceImage=ImageLibrary.get('sand_tile'))
        
    def update(self, timeElapsed):
        pass

class Grass(GameObject):
    """
    Represents grass that grows on dirt tiles and may spread to adjacent tiles.
    """
    def __init__(self, position, game):
        """
        Initializes the grass with a growth timer that determines when it spreads.
        """
        width = 96
        height = 96
        sourceImage = ImageLibrary.get('grass_tuft')  
        super().__init__(position, width, height, sourceImage, game)
        self.growth_timer = random.randint(5, 20)

    def update(self, timeElapsed):
        """
        Updates the grass growth timer. When the timer runs out, the grass spreads.
        """
        self.growth_timer -= timeElapsed
        if self.growth_timer <= 0:
            self.spread()
            self.growth_timer = random.randint(5, 20)  
    
    def spread(self):
        """
        Spreads grass to adjacent dirt tiles.
        """
        pass

class Flower(GameObject):
    """
    Represents a flower that grows on dirt tiles and spreads similar to grass.
    """
    def __init__(self, position, game):
        """
        Initializes the flower with a growth timer for spreading.
        """
        width = 96
        height = 96
        sourceImage = ImageLibrary.get('grass_tile')  
        super().__init__(position, width, height, sourceImage, game)
        self.growth_timer = random.randint(5, 15)

    def update(self, timeElapsed):
        """
        Updates the flower's growth timer. Spreads when the timer runs out.
        """
        self.growth_timer -= timeElapsed
        if self.growth_timer <= 0:
            self.spread()
            self.growth_timer = random.randint(5, 15)  
    
    def spread(self):
        """
        Spreads the flower to adjacent dirt tiles.
        """
        pass
    
class OutOfBoundsException(Exception):
    """
    Custom exception for handling out-of-bounds target selections.
    """
    def __init__(self, message):
        """
        Initializes the exception with a message.
        """
        super().__init__(message)

class Animal(GameObject):
    """
    Represents a base class for animals in the ecosystem. Inherited by specific animals.
    """
    def __init__(self, position, game, width, height, sourceImage, speed, energy):
        """
        Initializes the animal with position, size, image, speed, and energy.
        """
        super().__init__(position, width, height, sourceImage, game)
        self.speed = speed
        self.energy = energy

    def update(self, timeElapsed):
        """
        Updates the animal's behavior over time. To be overridden by specific animals.
        """
        pass

class Wombat(Animal):
    """
    Represents a wombat in the ecosystem that eats grass to restore energy.
    """
    def __init__(self, position, game):
        """
        Initializes the wombat with specific attributes like speed and energy.
        """
        width = 96
        height = 96
        sourceImage = ImageLibrary.get('wombat1')
        speed = 10
        energy = 100
        super().__init__(position, game, width, height, sourceImage, speed, energy)
        self.target = self.selectTarget()

    def selectTarget(self):
        """
        Selects a random target within the game bounds for the wombat to move towards.
        Raises an OutOfBoundsException if the target is out of bounds.
        """
        while True:
            try:
                target = Vector2D(random.randint(0,11) * 96, random.randint(0,9) * 96)
                if target.x < 0 or target.x > 1152 or target.y < 0 or target.y > 984:
                    raise OutOfBoundsException(f"Target {target} is out of bounds")
                return target
            except OutOfBoundsException as e:
                print(e)

    def update(self, timeElapsed):
        """
        Updates the wombat's behavior. Moves towards a target or eats grass when low on energy.
        """
        self.energy -= timeElapsed
        if self.energy <= 0:
            self.destroy()
        elif self.energy < 20:
            pass

        else:
            trajectory = self.target.subtract(self.get_position()).normalize().scale(self.speed * timeElapsed)
            self.move_by(trajectory.x, trajectory.y)
            if self.get_position().distance(self.target) < 48:
                self.target = self.selectTarget()

class Snake(Animal):
    """
    Represents a snake in the ecosystem that eats wombats to restore energy.
    """
    def __init__(self, position, game):
        """
        Initializes the snake with specific attributes like speed and energy.
        """
        width = 96
        height = 96
        sourceImage = ImageLibrary.get('snake1')
        speed = 15
        energy = 80
        super().__init__(position, game, width, height, sourceImage, speed, energy)
        self.target = self.selectTarget()

    def selectTarget(self):
        """
        Selects a random target within the game bounds for the snake to move towards.
        Raises an OutOfBoundsException if the target is out of bounds.
        """
        while True:
            try:
                target = Vector2D(random.randint(0, 11) * 96, random.randint(0, 9) * 96)
                if target.x < 0 or target.x > 1152 or target.y < 0 or target.y > 984:
                    raise OutOfBoundsException(f"Target {target} is out of bounds")
                return target
            except OutOfBoundsException as e:
                print(e)
    
    def update(self, timeElapsed):
        """
        Updates the snake's behavior. Moves towards a target or eats wombats when low on energy.
        """
        self.energy -= timeElapsed
        if self.energy <= 0:
            self.destroy()
        elif self.energy < 20:
            pass
        
        else:
            trajectory = self.target.subtract(self.get_position()).normalize().scale(self.speed * timeElapsed)
            self.move_by(trajectory.x, trajectory.y)
            if self.get_position().distance(self.target) < 48:
                self.target = self.selectTarget()

class Bird(Animal):
    """
    Represents a bird in the ecosystem that eats flowers to restore energy.
    """
    def __init__(self, position, game):
        """
        Initializes the bird with specific attributes like speed and energy.
        """
        width = 96
        height = 96
        sourceImage = ImageLibrary.get('wombat2')
        speed = 20
        energy = 60
        super().__init__(position, game, width, height, sourceImage, speed, energy)

    def update(self, timeElapsed):
        self.energy -= timeElapsed
        if self.energy <= 0:
            self.destroy()
        elif self.energy < 20:
            pass
        else:
            pass

class EcoSim(Game):
    """
    The main class that represents the ecosystem simulation.
    Responsible for setting up the environment with tiles and animals.
    """
    
    def __init__(self):
        """
        Initializes the ecosystem simulation by creating a grid of tiles and animals.
        """
        super().__init__()
        self.tiles = []
        self.animals = []
        self.setup_environment()
    
    def setup_environment(self):
        """
        Sets up the simulation environment by adding tiles and animals to the game.
        """
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
        for i in range(6): 
            position = Vector2D(random.randint(0, 11) * 96, random.randint(0, 9) * 96)
            self.animals.append(Bird(position, self))


def main():
    ImageLibrary.load('images')  
    ecosim = EcoSim()
    
    ecosim.run()

if __name__ == '__main__':
    main()