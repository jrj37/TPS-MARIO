from settings import *

w,h =48,56
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image=pygame.Surface((w,h))
        self.image.fill('green')
        self.rect= self.image.get_rect(topleft=pos)