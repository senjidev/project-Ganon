import pygame as pg, sys # import pygame and sys
from pygame.locals import * # import pygame modules

pg.init() # initiate pygame

clock = pg.time.Clock() # set up the clock
fps = 60

pg.display.set_caption('project-ganon') # set the window name
WINDOW_SIZE = (800,400) # set up window size
screen = pg.display.set_mode(WINDOW_SIZE,0,32) # initiate screen
display = pg.Surface((400, 200))



background_img = pg.image.load('./images/backgrounds/bg.png').convert_alpha()
grass_image = pg.image.load('./images/world_tiles/grass.png')
dirt_image = pg.image.load('./images/world_tiles/dirt.png')

TILE_SIZE = grass_image.get_width()



#player class
class Player():
	def __init__(self,x,y,name,max_hp,strength,items):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.strength = strength
		self.start_items = items
		self.items = items
		self.alive = True
		self.anim_list = []
		self.frame_index = 0
		self.action = 0 	#0:idle, 1:attack, 2:hurt, 3:dead
		self.update_time = pg.time.get_ticks()
	    
        
        #load images
		temp_list = []
		"""I AM IN FACT WRITING IT IN PYTHON"""
		'''<3'''
		for i in range(4):
			img = pg.image.load(f'./images/knight/idle/{i}.png')
			img = pg.transform.scale(img, (img.get_width()*2, img.get_height()*2 ))
			temp_list.append(img)
		self.anim_list.append(temp_list)
		self.image = self.anim_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)


	def update(self):
		anim_cooldown = 100
 		#handle animation
		#update image
		self.image = self.anim_list[self.action][self.frame_index]
		#check if enough time passed since last update
		if pg.time.get_ticks() - self.update_time > anim_cooldown:
			self.update_time = pg.time.get_ticks()
			self.frame_index += 1
		#if anim has run out of img's then reset
		if self.frame_index >= len(self.anim_list[self.action]):
			self.frame_index = 0

	def draw(self):
		screen.blit(self.image, self.rect)


"""COLLISION DETECTION"""
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


"""MOVE FUNCTION"""
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

#function for drawing bg
def draw_bg():
    screen.blit(background_img, (0,-350))

moving_right = False
moving_left = False

player_y_momentum = 0
air_timer = 0

test_rect = pg.Rect(100,100,100,50)


"""GAME LOOP"""

while True: # game loop
    #spawn players
    player = Player(200,300,'cindax',30,10,0)

    draw_bg()
    player.update()
    player.draw()
    
    '''MAP HITBOXING'''
    tile_rects = []
    y = 0
    from kithalas_domain_numMap import game_map
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    '''MOVEMENT HANDLING'''
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 2:
        player_y_momentum = 2.5

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1



    """EVENT HANDLER"""
    for event in pg.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pg.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_SPACE:
                if air_timer < 4:
                    player_y_momentum = -3
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False

    #surf = pg.transform.scale(display, WINDOW_SIZE)
    #screen.blit(surf, (0, 0))
    pg.screen.update() # update display
    clock.tick(fps) # maintain 60 fps