from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector(500,0)

        def draw(self):
            for sprite in self:
                offset_pos = sprite.rect.topleft + self.offset
                self.display_surface.blit(sprite.image, offset_pos)