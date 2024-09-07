from game import *


class EcoSim(Game):
    
    def __init__(self):
        super().__init__()


def main():
    ImageLibrary.load('images')  
    ecosim = EcoSim()
    
    ecosim.run()

if __name__ == '__main__':
    main()