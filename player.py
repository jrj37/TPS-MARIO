from settings import *

FPS=10
w,h =48,56
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites):
        super().__init__(groups)
        self.image=pygame.Surface((w,h))
        self.image.fill('green')
        self.rect= self.image.get_frect(topleft=pos)
        #movement
        self.speed =200
        self.direction=vector(1,0)
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
        self.direction = input_vector.normalize() if input_vector else input_vector
            
        

    def move(self,dt):
        self.rect.x += self.direction.x * self.speed*dt
        self.rect.y += self.direction.y * self.speed*dt
        
    def update(self,dt):
        self.input()
        self.move(dt)
