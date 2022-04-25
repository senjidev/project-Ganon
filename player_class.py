import pygame as pg
from test import screen
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