import pygame as pg
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
