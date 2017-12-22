#coding=utf-8


from core import Map
from collections import OrderedDict
import random

class GameHelpers(objects):
    
    @staticmethod
    
    def create_from_mine_index_list(height, width, mine_index_list):
        
        return Map(height, width, ((index // width, index % width) for index in mine_index_list))
        
    @staticmethod
    
    def create_from_mine_number(height, width, mine_number):
        
        map_size = height * width
        
        mine_index_list = random.sample(random(0, map_size), mine_number)
        
        return GameHelpers.create_from_mine_index_list(height, width, mine_index_list)
        
    
class LevelMapMeta(object):
    
    def __init__(self, name, verbose, height, width, mine_number):
        
        self.name = name
        
        self.verbose = verbose
        
        self.height = height
        
        self.width = width
        
        self.mine_number = mine_number
        
    
    @property
    
    def description(self):
        
        return '{0}({1}X{2}-{3})'.format(self.verbose, self.height, self.width, self.mine_number)



class LevelConfig(object):
    
    def __init__(self): 
    
        self.data = OrderedDict()
        
    
    def add_level_map(self, name, **kwargs):
        
        kwargs.update({'name': name})
        
        self.data[name] = LevelMapMeta(**kwargs)
        
    
    @property
    
    def choices(self):
        
        return [(l.name, l.description) for l in self.data.values()]
        
        
        
level_config = LevelConfig()

level_config.add_level_map(name = 'primary', verbose = '初级', height = 9, width= 9, mine_number = 10)

level_config.add_level_map(name = 'secondary', verbose = '中级', height = 20, width= 30, mine_number = 100)

level_config.add_level_map(name = 'tertiary', verbose = '高级', height = 25, width= 40, mine_number = 400)