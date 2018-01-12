from collections import OrderedDict
from mine_helper import MineHelper

class LevelMapData(object):
    def __init__(self, name, verbose, height, width, mine_number):
        self.name = name
        self.verbose = verbose
        self.height = height
        self.width = width
        self.mine_number = mine_number

    @property
    def description(self):
        return '{0}({1}*{2}-{3})'.format(self.verbose, self.height, self.width, self.mine_number)


class Level_config(object):
    def __init__(self):
       self.data = OrderedDict()

    def add_level_map(self, name, **kwargs):
        kwargs.update({'name':name})
        self.data[name] = LevelMapData(**kwargs)

    def level_map(self, name):
        meta = self.data[name]
        return MineHelper.create_from_mine_number(meta.height, meta.width, meta.mine_number)


    @property
    def choices(self):
        return [(l.name, l.description) for l in self.data.values()]

levelConfig = Level_config()
levelConfig.add_level_map(name = 'primary', verbose = 'low', height = 9, width = 9, mine_number = 10)
levelConfig.add_level_map(name = 'secondary', verbose = 'high', height = 20, width = 30, mine_number = 100)
levelConfig.add_level_map(name = 'tertiary', verbose = 'top', height = 25, width = 40, mine_number = 400)
