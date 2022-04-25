game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','2','2','2','0','0','0','0','0','0','0','2','2','2','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','0'],
            ['0','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','0'],
            ['0','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','0'],
            ['0','0','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','0','0'],
            ['0','0','0','0','0','0','0','1','1','1','1','1','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']]











from pygame.locals import *
import pygame as pg, sys

pg.init()
is_running = True

#fps config
clock = pg.time.Clock()
fps = 60

#window setup
WINDOW_SIZE = [800, 600]
screen = pg.display.set_mode(WINDOW_SIZE, 0, 32)
pg.display.set_caption('project-ganon')


#draw background
def draw_bg():
    background_img = pg.image.load('images/backgrounds/bg.png')
    screen.blit(background_img, (0,-270))

#player class

#map config
grass_image = pg.image.load('images/world_tiles/grass.png')
dirt_image = pg.image.load('images/world_tiles/dirt.png')
TILE_SIZE = grass_image.get_width()


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

#movement functionality
moving_right = False
moving_left = False
player_y_momentum = 0
air_timer = 0
def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
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


#name the crow hatei
while is_running:
    #player = Player(250,400,'hatei',0)
    player_image = pg.image.load('characters/hatei/player.png').convert()
    #player hitboxing
    player_rect = pg.Rect(50, 50, player_image.get_width(), player_image.get_height())

    
   
    #draw background
    screen.fill((0,0,0))
    #map hitboxing
    tile_rects = []
    y = 0
    from kithalas_domain_numMap import game_map
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                screen.blit(dirt_image, (x*TILE_SIZE,y*TILE_SIZE))
            if tile == '2':
                screen.blit(grass_image, (x*TILE_SIZE,y*TILE_SIZE))
            if tile != '0':
                tile_rects.append(pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1
    #movement config
    player_movement = [0,0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3
    
    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    #collision detection
    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    #draw player
    screen.blit(player_image, (player_rect.x, player_rect.y))
    #event handler
    for events in pg.event.get():
        
        if events.type == QUIT:
            print('GAME CLOSED')
            pg.quit()
            sys.exit()
        
        if events.type == KEYDOWN:
            if events.key == K_d:
                moving_right = True
            if events.key == K_a:
                moving_left = True
            if events.key == K_SPACE:
                if air_timer < 6:
                    player_y_momentum = -5

        if events.type == KEYUP:
            if events.key == K_d:
                moving_right = False
            if events.key == K_a:
                moving_left = False
            
    
   
   
    #set clock
    clock.tick(fps)
    #screen refresh
    pg.display.update()            