#coding=utf-8

import Queue as queue

class Core_Map(object):
    
    MINE_FLAG = 1
    
    def __init__(self, height, width, mine_pos_list):
        
        self._height = height
        
        self._width = width
        
        self._mine_list = list(set(mine_pos_list)) #地雷的位置

        print ('mine pos list: %s' %self._mine_list)
        
        self._generate_distribute_map()
        
    
    @property
    def height(self):
        
        return self._height
    
    @property
    
    def width(self):
        
        return self._width
        
    @property
    
    def map_size(self):
        
        return self._height * self._width
    
    @property
    
    def mine_list(self):
        
        return self._mine_list
    
    @property
    
    def mine_number(self):
        
        return len(self._mine_list)
        
    @property
    
    def distribute_map(self):    
        
        return self._distribute_map
        
        
    def _generate_distribute_map(self):
        
        # count_add = 0
        
        # count_one = 0
        
        # count_zero = 0        
        
        self._distribute_map = [[0 for _ in range(0, self.width)] for _ in range(0, self.height)]
        
        offset_step = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]  #相邻的8个位置上下左右移动
        
        for t_x, t_y in self._mine_list:
            
            self._distribute_map[t_x][t_y] = Core_Map.MINE_FLAG
            
            for o_x, o_y in offset_step:
                
                d_x, d_y = o_x + t_x, o_y + t_y                       
                
                if self.is_in_map((d_x, d_y)) and self._distribute_map[d_x][d_y] != Core_Map.MINE_FLAG:
                
                    # count_add += 1                                        
                
                    self._distribute_map[d_x][d_y] += 1
        
        # for _ditribute in self._distribute_map:
        
            # print ('_distribute_map is : %s' %_ditribute)
            
        # print '-----------'
            
        # for x in range(0, self.height):
            
            # for y in range(0, self.width):
                
                # if self._distribute_map[x][y] == 1:
                
                    # count_one += 1
                
                # else:
                
                    # count_zero += 1
                
            
        # print 'count_add = %d ' %count_add
        
        # print 'count_one = %d ' %count_one
        
        # print 'count_zero = %d ' %count_zero


                    
    
    def is_in_map(self, pos,offset = None):
        
        if offset:
            
            x, y = pos[0] + offset[0], pos[1] + offset[1]
        
        else:
            
            x, y = pos
            
        if (x in range(0, self.height) and y in range(0, self.width)) != True:
            
            print x, y
            
        return x in range(0, self.height) and y in range(0, self.width)    
        
    
    def is_mine(self, pos):
        
        return pos in self._mine_list
        
    
    def get_near_mine_number(self, pos):
        
        x, y = pos
        
        return self._distribute_map[x][y]   
    
    
    
    
    

class Game(object): 
    
    STATE_PLAY = 1
    
    STATE_SUCCESS = 2
    
    STATE_FAIL = 3
    
    def __init__(self, mine_map):
        
        self._mine_map = mine_map
        
        self._init_game()
        
    
    def _init_game(self):
        
        self._swept_state_map = [[False for _ in range(0, self._mine_map.width)] for _ in range(0 ,self._mine_map.height)]
        
        self._not_swept_number = self._mine_map.map_size
        
        self._cur_step = 0
        
        self._sweep_trace = []
        
        self._state = Game.STATE_PLAY
        
    
    def reset(self):
        
        self._init_game()
        
    
    @property
    
    def cur_step(self):
        
        return self._cur_step
        
    @property
    
    def sweep_trace(self):
        
        return self._sweep_trace
        
    @property
    
    def state(self):
        
        return self._state
        
    @property
    
    def not_swept_number(self):
        
        return self._not_swept_number
        
    @property
    
    def swept_state_map(self):
        
        return self._swept_state_map
        
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
    
    def mine_map(self):
        
        return self._mine_map
        
        
    def _sweep(self, click_pos):
        
        if self._state == Game.STATE_SUCCESS or self. _state == Game.STATE_FAIL:
            
            return self._state
            
        self._cur_step += 1
        
        self._sweep_trace.append(click_pos)
        
        cx, cy = click_pos
        
        if self._swept_state_map[cx][cy]:
            
            self._state = Game.STATE_PLAY
            
            return self._state
            
            
        near_mine_number = self._mine_map.get_near_mine_number(click_pos)
        
        if near_mine_number == Core_Map.MINE_FLAG:
            
            self._not_swept_number -= 1
            
            self._swept_state_map[cx][cy] = True
            
            return Game.STATE_FAIL
            
        elif near_mine_number > 0:
            
            self._not_swept_number -= 1
            
            self._swept_state_map[cx][cy] = True
            
            if self._not_swept_number == self._mine_map.mine_number: #没扫的个数等于地雷的个数
                
                self._state = Game.STATE_SUCCESS
                
            else:
                
                self._state = Game.STATE_PLAY
            
            return self._state
            
        else:
            
            scan_step = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            
            assert near_mine_number == 0
            
            q = queue.Queue()
            
            q.put(click_pos)
            
            self._not_swept_number -= -1
            
            self._swept_state_map[cx][cy] = True
            
            while not q.empty():
                
                c_x, c_y = q.get()
                
                for o_x, o_y in scan_step:
                    
                    d_x, d_y = c_x + o_x, c_y + o_y
                    
                    if self._mine_map.is_in_map((d_x, d_y)) and not self._sweep_trace[d_x][d_y]:
                        
                        near_mine_number = self._mine_map.get_near_mine_number((d_x, d_y))
                        
                        if near_mine_number == Core_Map.MINE_FLAG:
                            
                            pass
                        
                        elif near_mine_number == 0:
                            
                            q.put((d_x, d_y))
                            
                            self._swept_state_map[d_x][d_y] = True
                            
                            self._not_swept_number -= 1
                         
                        else:
                            
                            self._swept_state_map[d_x][d_y] = True
                            
                            self._not_swept_number -= 1
                            
                assert self._not_swept_number >= self._mine_map.mine_number
                
                if self._not_swept_number == self._mine_map.mine_number:
                    
                    self._state = Game.STATE_SUCCESS
                
                else:
                    
                    self._state = Game.STATE_PLAY
                
                return self._state
                
    
    def play(self, click_pos):    
        
        state = self._sweep(click_pos)
        
        if state == Game.STATE_SUCCESS or state == Game.STATE_FAIL:
            
            self._sweep_all_map()
            
    
    def _sweep_all_map(self): #重置扫过的状态
        
        self._swept_state_map = [[True for _ in range(0, self.width)] for _ in range(0, self.width)]
        
        self._not_swept_number = self._mine_map.mine_number
                            
                            
                            
                    
           
                
           
         
    
    
    
    
