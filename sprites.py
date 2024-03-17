from typing import Any
from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf=pygame.Surface((TILE_SIZE,TILE_SIZE)),groups=None):
        super().__init__(groups)
        self.image = surf
        self.image.fill('blue')
        self.rect =self.image.get_frect(topleft=pos) 
        self.old_rect=self.rect.copy()
        
class MovingSprite(Sprite):
    def __init__(self, groups,start_pos,end_pos,move_dir,speed):
        surf = pygame.Surface((200,50))
        super().__init__(start_pos, surf, groups)
        self.rect.center= start_pos
        self.start_pos=start_pos
        self.end_pos =start_pos
        
        #movement
        self.speed =speed
        self.direction=vector(1,0) if move_dir =='x'else vector(0,1)
        self.move_dir =move_dir
        
    def update(self,dt):
        self.old_rect=self.rect.copy()
        self.rect.topleft+=self.direction*self.speed*dt