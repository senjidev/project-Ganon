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
class Player:
    def __init__(self, x, y, character, damage):
        #self.skin = skin
        self.character = character
        self.damage = damage
        self.alive = True
        self.anim_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pg.time.get_ticks()

        #load images
        temp_list = []
        for i in range(4):
            img = pg.image.load(f'characters/hatei/hatei.png')
            img = pg.transform.scale(img, (img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.anim_list.append(temp_list)
        self.image = self.anim_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)


    #animation update
    def update(self):
        anim_cooldown = 100
        #update image
        self.image = self.anim_list[self.action][self.frame_index]
        #check if enough time has passed since last update
        if pg.time.get_ticks()-self.update_time > anim_cooldown:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
        #if anim has run of of img's, then reset anim
        if self.frame_index >= len(self.anim_list[self.action]):
            self.frame_index = 0
    
    #draw player
    def draw(self):
        screen.blit(self.image, self.rect)

#map config
grass_image = pg.image.load('images/world_tiles/grass.png')
dirt_image = pg.image.load('images/world_tiles/dirt.png')
TILE_SIZE = grass_image.get_width()
class Map_Gen:
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

    def __init__(self,map_name):
        self.map_name = map_name


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


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

        #load tiles

#name the crow hatei
while is_running:
    player = Player(250,400,'hatei',0)
    #set clock
    clock.tick(fps)
    #draw background
    draw_bg()
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
            
    for events in pg.event.get():
        if events.type == QUIT:
            print('GAME CLOSED')
            pg.quit()
            sys.exit()
        if events.type == KEYDOWN:
            pass
    
    #draw player
    player.update()
    player.draw()
    #screen refresh
    pg.display.update()