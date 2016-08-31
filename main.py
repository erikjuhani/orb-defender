__author__ = 'erikjuhani'

import pygame as pg
import sys
from game import Game

''' Window constants '''
CAPTION = 'Orb Defender'
WIDTH = 800
HEIGHT = 640
SCREEN_SIZE = (WIDTH, HEIGHT)

def main():

    ''' Initialize pygame display '''
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    ''' Start the main game loop '''
    Game().game_loop()

    ''' When the game loop is over, quit '''
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
