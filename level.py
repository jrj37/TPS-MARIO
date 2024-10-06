from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite
from player import Player
from groups import AllSprites
from enemies import Tooth, Shell,Pearl

class Level:
    
    def __init__(self,tmx_map, level_frames):
        self.display_surface=pygame.display.get_surface()
        
        #data 
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_bottom = tmx_map.height * TILE_SIZE
        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        
        self.damage_sprites = pygame.sprite.Group()
        self.tooth_sprites= pygame.sprite.Group()
        self.pearl_sprites= pygame.sprite.Group()
        
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map, level_frames)
        self.pearl_surf= level_frames['pearl']
    
    def setup(self,tmx_map, level_frames):
        # tiles
        for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain' : groups.append(self.collision_sprites)
                if layer == 'Platforms' : groups.append(self.semi_collision_sprites)
                match layer:
                    case 'BG': z = Z_LAYERS['bg tiles']
                    case 'FG' : z = Z_LAYERS['fg']
                    case _ : z = Z_LAYERS['main']
                Sprite((x*TILE_SIZE,y* TILE_SIZE), surf, groups)
        
        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name =='player':
               self.player = Player(
                   pos = (obj.x,obj.y),
                   groups = self.all_sprites,
                   collision_sprites = self.collision_sprites,
                   semi_collision_sprites = self.semi_collision_sprites,
                   frames = level_frames['player'])
            else:
                #if obj.name == 'flag':
                    #self.level_finish.rect=pygame.FRect((obj.x,obj.y),(obj.width,obj.height))
                if obj.name in ('barrel', 'crate'):
                    Sprite(((obj.x, obj.y)), obj.image, (self.all_sprites, self.collision_sprites))
                else:
                    if 'palm' not in obj.name:
                        frames = level_frames[obj.name]
                        AnimatedSprite(((obj.x, obj.y)), frames, self.all_sprites)
                        
        # moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == 'helicopter':
                if obj.width > obj.height: #horizontal
                    move_dir = 'x'
                    start_pos = (obj.x,obj.y + obj.height / 2)
                    end_pos = (obj.x+obj.width,obj.y + obj.height / 2)
                else: #vertical
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width / 2,obj.y)
                    end_pos = (obj.x + obj.width / 2 ,obj.y+obj.height)
                speed = obj.properties['speed']
                MovingSprite((self.all_sprites, self.semi_collision_sprites), start_pos, end_pos, move_dir, speed)
                
        #enemies 
        for obj in tmx_map.get_layer_by_name('Enemies'):
            if obj.name == 'tooth':
                Tooth((obj.x,obj.y),level_frames['tooth'],(self.all_sprites,self.damage_sprites,self.tooth_sprites),self.collision_sprites)
            if obj.name =='shell':
                Shell(pos=(obj.x,obj.y),frames=level_frames['shell'],groups=(self.all_sprites,self.collision_sprites),reverse=obj.properties['reverse'],player=self.player,create_pearl=self.create_pearl)
     
        #water
        for obj in tmx_map.get_layer_by_name('Water'):
            rows = int (obj.height / TILE_SIZE)
            cols = int(obj.width / TILE_SIZE)
            
            for row in range(rows):
                for col in range(cols):
                    x = obj.x + col * TILE_SIZE
                    y = obj.y + row * TILE_SIZE
                    
                    if row==0:
                        AnimatedSprite((x,y),level_frames['water_top'],self.all_sprites,Z_LAYERS['water'])
                    else:
                        Sprite((x,y),level_frames['water_body'],self.all_sprites,Z_LAYERS['water'])
                       
    def create_pearl(self,pos,direction): 
        Pearl(pos,(self.all_sprites,self.damage_sprites,self.pearl_sprites),self.pearl_surf,direction,150)                
    
    def pearl_collision(self):
        for sprite in self.collision_sprites:
            pygame.sprite.spritecollide(sprite,self.pearl_sprites,True)
            
    def hit_collision(self):
        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                print('player damage')
                if sprite.name=='pearl':
                    sprite.kill()             
    
    def check_constraint(self):
        #gauche droite
        if self.player.hitbox_rect.left <= 0:
            self.player.hitbox_rect.left = 0
        if self.player.hitbox_rect.right >= self.level_width:
            self.player.hitbox_rect.right = self.level_width
        #haut bas
        if self.player.hitbox_rect.top <= 0:
            self.player.hitbox_rect.top = 0
        if self.player.hitbox_rect.bottom > self.level_bottom:
            print("player is dead")
            
        #if self.player.hitbox_rect.colliderect(self.level_finish.rect):
         #   print('level finish')
    def run(self,dt):
        self.display_surface.fill('black')
        
        self.all_sprites.update(dt)
        self.pearl_collision()
        self.hit_collision()
        self.all_sprites.MyDraw(self.player.hitbox_rect.center)   
        self.check_constraint()