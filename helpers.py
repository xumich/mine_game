#coding=utf-8

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from core import Core_Map

from collections import OrderedDict

import random


class GameHelpers(object):
    
    @staticmethod
    
    def create_from_mine_index_list(height, width, mine_index_list):
        
        return Core_Map(height, width, ((index // width, index % width) for index in mine_index_list)) #地雷的位置
        
        
    @staticmethod
    
    def create_from_mine_number(height, width, mine_number):
        
        map_size = height * width
        
        mine_index_list = random.sample(range(0, map_size), mine_number)  #随机取mine_number个地雷的数

        print ('the random mine list: %s' %mine_index_list)
        
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
    

    def level_map(self, name):
        
        meta = self.data[name] # 根据名称获取地图信息
    
        return GameHelpers.create_from_mine_number(meta.height, meta.width, meta.mine_number)

        
# 初始化等级数据    
level_config = LevelConfig()

level_config.add_level_map(name = 'primary', verbose = '初级', height = 9, width= 9, mine_number = 10)

level_config.add_level_map(name = 'secondary', verbose = '中级', height = 20, width= 30, mine_number = 100)

level_config.add_level_map(name = 'tertiary', verbose = '高级', height = 25, width= 40, mine_number = 400)