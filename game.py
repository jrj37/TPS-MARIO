from settings import *
from level import *
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('SUPER TPS WORLD')
        self.clock =pygame.time.Clock()
        
        self.tmx_maps={0: load_pygame(join('.','data','levels','omni.tmx'))}
        print(self.tmx_maps)
        
        self.current_stage=Level(self.tmx_maps[0])
        
    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('.', 'graphics', 'level', 'flag'),
            'saw': import_folder('.', 'graphics', 'enemies', 'saw', 'animation'),
            'floor_spike' : import_folder('.', 'graphics', 'enemies', 'floor_spikes'),
            'palms' : import_folder('.', 'graphics', 'level', 'palms'),
            'candles' : import_folder('.', 'graphics', 'level', 'candle'),
            'window' : import_folder('.', 'graphics', 'level', 'window'),
            'big chain' : import_folder('.', 'graphics', 'level', 'big chains'),
            'small chain' : import_folder('.', 'graphics', 'level', 'small chains'),
            'player' : import_folder('.', 'graphics', 'player'),
        }
        
    def run(self):
        while True:
            dt = self.clock.tick()/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.current_stage.run(dt) 
            pygame.display.update()