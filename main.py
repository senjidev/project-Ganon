from pygame.locals import *
import pygame as pg, sys

"""GLOABALS"""
global is_running
is_running = True


#init
pg.init()

#window config
pg.display.set_caption("project-ganon")
WINDOW_SIZE = (800,800)
global screen
screen = pg.display.set_mode(WINDOW_SIZE, 0, 32)

#fps clock
clock = pg.time.Clock()

"""GAME LOOP"""
def mainLoop():
    while is_running:
        #bg color
        screen.fill((255, 0, 0))

        #event handler
        for event in pg.event.get():
            """EVENTS"""
            #game closed
            if event.type == QUIT:
                print('Game Closed')
                pg.quit()
                sys.exit()
        
        pg.display.update() #window refresh
        clock.tick(60) #fps set


if __name__ == '__main__':
    mainLoop()