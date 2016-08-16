import pygame as pg
import sys
from game import Game

''' Window constants '''
CAPTION = 'Kingdom Heart'
WIDTH = 640
HEIGHT = 480
SCREEN_SIZE = (WIDTH, HEIGHT)

def main():

    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    Game().game_loop()

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
