from pygame.locals import *
import pygame as pg, sys

"""GLOABALS"""
global is_running
is_running = True


#init
pg.init()

#window config
pg.display.set_caption("project-ganon")
WINDOW_SIZE = (800,600)
global screen
screen = pg.display.set_mode(WINDOW_SIZE, 0, 32)
display = pg.Surface((400, 300))
#fps clock
clock = pg.time.Clock()



"""MAP COLLISIONS"""
def collision_test(rect, map):
    hit = False
    #if player_location[1] < WINDOW_SIZE[1]-player_image.get_height():



"""MAIN LOOP"""
def mainLoop():
 

    """MOVEMENT INIT VARIABLES"""
    moving_right = False
    moving_left = False

    """TEMP PLAYER SPAWN"""
    player_location = [250,250]

    """PLAYER CONFIG"""
    player_image = pg.image.load('./project-Ganon/characters/cindax/cindax_OG.png')
    player_image.set_colorkey((255, 255, 255))
    player_y_momentum = 0

    """MAPSET CONFIG"""
    helios_image = pg.image.load('./project-Ganon/maps/helios/heliosSMALLER.png')
    map_spawn = [100,100]

    """HITBOX CONFIG"""
    player_rect = pg.Rect(
        player_location[0], 
        player_location[1], 
        player_image.get_width(), 
        player_image.get_height()
        )
    #test hitbox
    #test_box = pg.Rect(100,100,100,50)

    """GAME LOOP"""
    while is_running:
        
        """BG COLORING"""
        screen.fill((175,75,255))
        display.fill((0,0,0))
        """SURFACE LAYERING"""
        #screen.blit(helios_image, map_spawn)
        #screen.blit(player_image, player_location)
        #display.blit(helios_image, map_spawn)
        display.blit(player_image, player_location)
        
        #JUMPING
        #if player_location[1]> WINDOW_SIZE[1]-player_image.get_height():
            #player_y_momentum = -player_y_momentum
        
       # player_y_momentum += 0.2
        
       # player_location[1] += player_y_momentum
        
        #PLAYER MOVEMENT
        if moving_right == True:
            player_location[0]+= 4
        if moving_left == True:
            player_location[0] -= 4

        #HITBOX SPAWN CONFIG
        #player hitbox
        player_rect.x = player_location[0]
        player_rect.y = player_location[1]
        #test box config
        '''if player_rect.colliderect(test_box):
            pg.draw.rect(screen,(255,0,0), test_box)
        else:
            pg.draw.rect(screen,(0,0,0), test_box)'''
        
        #bg color

        #event handler
        for event in pg.event.get():
            """EVENTS"""
            #game closed
            if event.type == QUIT:
                print("Game Closed")
                pg.quit()
                sys.exit()
            #user input
            if event.type == KEYDOWN:
                if event.key == K_d:
                    moving_right = True
                    print("D Pressed")
                if event.key == K_a:
                    moving_left = True
                    print("A Pressed")
                #if event.key == K_s: for fast falling later
            if event.type == KEYUP:
                if event.key == K_d:
                    moving_right = False
                    print("D Released")
                if event.key == K_a:
                    moving_left = False
                    print("A Released")

                #if event.key == K_s: for fast falling later
        surf = pg.transform.scale(display,WINDOW_SIZE)
        screen.blit(surf, (0,0))
        pg.display.update() #window refresh
        clock.tick(60) #fps set


if __name__ == '__main__':
    mainLoop()