# coding:utf-8
try:
    import queue
except ImportError:
    import Queue as queue

class CoreMap(object):
    MINE_FLAG = -1

    def __init__(self, height, width, mine_pos_list):
        self._height = height
        self._width = width
        self._mine_list = list(set(mine_pos_list))
        self._mine_number = 0
        self._generate_distribute_map()

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def mine_list(self):
        return self._mine_list

    @property
    def map_size(self):
        return self._height * self._width

    @property
    def mine_number(self):
        return len(self._mine_list)

    @property
    def distribute_map(self):
        return self._distribute_map

    def _generate_distribute_map(self):
        self._distribute_map = [[0 for _ in range(0, self._width)] for _ in range(0, self._height)]
        offset_step = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        for t_x, t_y in self._mine_list:
            self._distribute_map[t_x][t_y] = CoreMap.MINE_FLAG
            for o_x, o_y in offset_step:
                d_x, d_y = t_x + o_x, t_y + o_y
                if self.is_in_map((d_x, d_y)) and self._distribute_map[d_x][d_y] != CoreMap.MINE_FLAG:
                    self._distribute_map[d_x][d_y] += 1

    def is_in_map(self, pos, offset=None):
        if offset:
            x, y = pos[0] + offset[0], pos[1] + offset[1]
        else:
            x, y = pos
        return x in range(0, self._height) and y in range(0, self._width)

    def is_mine(self, pos):
        return pos in self._mine_list

    def get_near_mine(self, pos):
        x, y = pos
        return self._distribute_map[x][y]


class Game(object):
    GAME_PLAY = 1
    GAME_SUCCESS = 2
    GAME_FAIL = 3

    def __init__(self, mine_map):
        self._mine_map = mine_map
        self._init_game()

    def _init_game(self):
        self._swept_state_map = [[False for _ in range(0, self._mine_map.width)] for _ in
                                 range(0, self._mine_map.height)]
        self._swept_trace = []
        self._cur_step = 0
        self._state = Game.GAME_PLAY
        self._not_swept_number = self._mine_map.map_size

    def game_reset(self):
        self._init_game()

    @property
    def cur_step(self):
        return self._cur_step

    @property
    def swept_state_map(self):
        return self._swept_state_map

    @property
    def swept_trace(self):
        return self._swept_trace

    @property
    def cur_step(self):
        return self._cur_step

    @property
    def state(self):
        return self._state

    @property
    def mine_map(self):
        return self._mine_map

    @property
    def height(self):
        return self._mine_map.height

    @property
    def width(self):
        return self._mine_map.width

    @property
    def mine_number(self):
        return self._mine_map.mine_number

    @property
    def map_size(self):
        return self._mine_map.map_size

    @property
    def not_swept_number(self):
        return self._not_swept_number

    def play(self, pos):
        state = self._sweep(pos)
        if state == Game.GAME_SUCCESS or state == Game.GAME_FAIL:
            self._sweep_all()
        return state

    def _sweep_all(self):
        self._swept_state_map = [[True for _ in range(0, self._mine_map.width)] for _ in range(0, self._mine_map.height)]
        self._not_swept_number = self.mine_map.map_size - self.mine_map.mine_number

    def _sweep(self, pos):
        x, y = pos
        if self._state == Game.GAME_SUCCESS or self._state == Game.GAME_FAIL:
            return self._state
        self._cur_step += 1
        self._swept_trace.append(pos)
        if self.swept_state_map[x][y]:
            self._state = Game.GAME_PLAY
            return self._state
        near_mine_number = self._mine_map.get_near_mine(pos)
        if near_mine_number == CoreMap.MINE_FLAG:#地雷
            self._not_swept_number -= 1
            self._swept_state_map[x][y] = True
            return Game.GAME_FAIL
        elif near_mine_number > 0:
            self._not_swept_number -= 1
            self._swept_state_map[x][y] = True
            if self._not_swept_number == self._mine_map.mine_number:
                self._state = Game.GAME_SUCCESS
            else:
                self._state = Game.GAME_PLAY
            return self._state
        else: #小于0空白处
            scan_step = [(-1, 0), (0, 1), (0, -1), (1, 0)] #上下左右的位置
            q = queue.Queue() #队列
            q.put(pos)
            self._not_swept_number -= 1
            self._swept_state_map[x][y] = True
            while not q.empty():
                for cx, cy in scan_step:
                    tx, ty = x + cx, y + cy
                    if self._mine_map.is_in_map((tx, ty)) and self._swept_state_map[tx][ty]: #在地图范围并且没有扫过的位置
                        near_mine_number = self._mine_map.get_near_mine((tx, ty))
                        if near_mine_number == CoreMap.MINE_FLAG:
                            pass
                        elif near_mine_number > 0:
                            self._not_swept_number -= 1
                            self._swept_state_map[tx][ty] = True
                        else:
                            q.put(tx, ty)
                            self._not_swept_number -= 1
                            self._swept_state_map[tx][ty] = True
            if self._not_swept_number == self._mine_map.mine_number:
                self._state = Game.GAME_SUCCESS
            else:
                self._state = Game.GAME_PLAY
            return self._state
