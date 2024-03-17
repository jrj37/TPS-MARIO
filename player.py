from settings import *

FPS=10
w,h =48,56
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites):
        super().__init__(groups)
        self.image=pygame.Surface((w,h))
        self.image.fill('green')

        #rects 
        self.rect= self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

        #movement
        self.speed =200
        self.direction=vector(0,0)
        self.jump = False
        self.jump_height = 9

        #collision
        self.collision_sprites=collision_sprites
        print(self.collision_sprites)
        
    def input(self):
        keys = pygame.key.get_pressed()
        input_vector=vector(0,0)
        if keys[pygame.K_RIGHT]:
            input_vector.x+=1
             
        if keys[pygame.K_LEFT]:
            input_vector.x-=1    
        
        if keys[pygame.K_SPACE]:
            self.jump = True 
        
        self.direction = input_vector.normalize() if input_vector else input_vector

    def move(self,dt):
        self.rect.x += self.direction.x * self.speed*dt
        self.rect.y += self.direction.y * self.speed*dt

        if self.jump:
            self.direction.y = -self.jump_height
            self.jump = False 
    
    def update(self,dt):
        self.input()
        self.move(dt)
