import pygame, sys # import pygame and sys
import time as t

clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
pygame.init() # initiate pygame

pygame.display.set_caption('project-ganon') # set the window name

WINDOW_SIZE = (800,600) # set up window size

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen

display = pygame.Surface((400, 300))


player_image = pygame.image.load('characters/void_monk/void_monk.png').convert()
player_image.set_colorkey((255,255,255))

grass_image = pygame.image.load('images/world_tiles/grass.png')
TILE_SIZE = grass_image.get_width()

dirt_image = pygame.image.load('images/world_tiles/dirt.png')

game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','2','2','2','0','0','0','0','0','0','0','2','2','2','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['0','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','0'],
            ['0','0','0','0','0','0','1','1','1','1','1','1','1','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']]


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    
    for tile in hit_list:
        
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


moving_right = False
moving_left = False
fast_fall = False
#sprint = False

player_y_momentum = 0
air_timer = 0

player_rect = pygame.Rect(60, 90, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)


"""GAME LOOP"""
bg = pygame.image.load('images/backgrounds/bg.png')
while True: # game loop
    
    #respawn
    if player_rect[1] > WINDOW_SIZE[1]:
        t.sleep(.6)
        player_rect[0] = 60
        player_rect[1] = 90
        #moving_right = False
        #moving_left = False
        #fast_fall = False
        air_timer = 0

    #draw background
    display.blit(bg, (0,-425))
    

    '''MAP HITBOXING'''
    tile_rects = []
    y = 3
    for row in game_map:
    
        x = 3
        
        for tile in row:
            
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
            
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1    


    '''MOVEMENT HANDLING'''
    player_movement = [0, 0]
    
    if moving_right:
        player_movement[0] += 3
        
    if moving_left:
        player_movement[0] -= 3
        

    if fast_fall:
        player_y_momentum += 0.4

    '''def sprinting(direction, movement):
        if direction:
            if movement[0] > 0:
                movement[0] + 2
            if movement[0] < 0:
                movement[0] - 2'''
    
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.4
    if player_y_momentum > 6:
        player_y_momentum = 6

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    #draw player
    display.blit(player_image, (player_rect.x, player_rect.y))


    """EVENT HANDLER"""
    for event in pygame.event.get():
        
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        
        if event.type == KEYDOWN:
            
            if event.key == K_d:
                moving_right = True
            
            if event.key == K_a:
                moving_left = True
            
            if event.key == K_s:
                fast_fall = True
            
            if event.key == K_SPACE:
                if air_timer < 6:
                    player_y_momentum = -6

            '''if event.key == K_LSHIFT:
                sprint = True
                if sprint:
                    sprinting(moving_left, player_movement)
                if sprint:
                    sprinting(moving_right, player_movement)'''
                    

            '''if event.key == K_h:
                player_image = pygame.image.load('characters/hatei/hatei.png').convert()
                player_image.set_colorkey((0,0,0))
            if event.key == K_c:
                player_image = pygame.image.load('characters/cindax/cindax_OG.png').convert()
                player_image.set_colorkey((0,0,0))'''
        
        if event.type == KEYUP:
            
            if event.key == K_d:
                moving_right = False
            
            if event.key == K_a:
                moving_left = False
            
            if event.key == K_s:
                fast_fall = False

            '''if event.key == K_LSHIFT:
                sprint = False'''

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps
