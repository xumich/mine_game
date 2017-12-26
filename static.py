#coding = utf-8

import os 
import sys


APP_NAME = 'mine_game'

HOME_URL = 'http://www.baidu.com'

PROJECT_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
print PROJECT_PATH

RESOURCE_PATH = os.path.join(PROJECT_PATH, 'images')
print RESOURCE_PATH

def static_file(fileName):

    return os.path.join(PROJECT_PATH, fileName)
    

def get_style(style_name, **kwargs):

    return loader.style(style_name, **kwargs)

    
class GridStyle(object):

    unknown = {'relief': 'raised', 'text': '', 'bg': '#DDDDDD', 'fg': '#000000'}
    
    marked = {'relief':'raised', 'text':'?', 'bg': '#DDDDDD', 'fg':'#000000'}
    
    mine = {'relief': 'sunken', 'text': 'X', 'bg': '#D71A23', 'fg': '#FFFFFF'}
    
    @staticmethod
    
    def swept(num):
    
        colors = ['#BBBBBB',

                  '#000000',

                  '#0602E7',

                  '#F52703',

                  '#6F3F17',

                  '#FFFE07',

                  '#FF12FF',

                  '#3EE8D3',

                  '#FDFCD6'
        ]
        
        return {'relief': 'sunken', 'text': num or ' ', 'bg': '#DDDDDD', 'fg': colors[num]}

        
class StyleLoader(object):

    def style(self, style_name, **kwargs):
    
        func = reduce(getattr, style_name.split('.'), self)
        
        return func(**kwargs) if callable(func) else func
        
        
    def register(self, style_pre, obj):
    
        setattr(self, style_pre, obj)
        
        
loader = StyleLoader()

loader.register('grid', GridStyle)

print getattr(GridStyle, 'unknown', 'not found')

print getattr(StyleLoader, 'grid.unknown', 'not found')

print get_style('grid.mine')