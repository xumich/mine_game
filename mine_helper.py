import random
from mine_core import CoreMap

class MineHelper(object):

    @staticmethod
    def create_from_mine_index_list(height, width, mine_index_list):
        return CoreMap(height, width, ((index//width, index % width) for index in mine_index_list))

    @staticmethod
    def create_from_mine_number(height, width, mine_number):
        map_size = height * width
        mine_index_list = random.sample(range(0, map_size), mine_number)
        return MineHelper.create_from_mine_index_list(height, width, mine_index_list)