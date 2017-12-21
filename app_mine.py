#coding = utf-8

from helper import GameHelpers

from helper import level_config

import widgets

import static

import tkinter as tk

from core import Game



class App(tk.Frame):

    def __init__(self):
    
        tk.Frame.__init__(self)
        
        self.master.title(static.APP_NAME)
        
        self.master.resizable(False, False)
        
        self.master.iconbitmap(static.images(''))
        
        self.pack(expand = tk.NO, fill = tk.BOTH)
        
        self.map_frame = None
        
        mine_map = level_config.map('primary') #根据游戏等级获取游戏地图
        
        self._create_map_frame(mine_map) #绘置地图
        
        self.create_top_menu()  #菜单：游戏/地图/关于
        
        
    def create_top_menu(self):
        
        top = self.winfo.tolevel()
        
        menu_bar = tk.Menu(top)
        
        top['menu'] = menu_bar
        
        
        game_menu = tk.Menu(menu_bar)
        
        game_menu.add_command(label ='start', command = self.map_frame.start)
        
        game_menu.add_command(label ='reset', command = self.map_frame.reset)
        
        game_menu.add_separator()  #----
        
        game_menu.add_command(label = 'quit', command = self.exit_app)
        
        menu_bar.add_cascade(label = 'game', menu = game_menu)
        
        
        map_menu = tk.Menu(menu_bar)
        
        self.level = tk.StringVar()
        
        self.level.set('primary')
        
        for level, label in level_config.choices:
        
            map_menu.add_radiobutton(label = label,
            
                                     variable = self.level, 
                                     
                                     value = level, 
                                     
                                     command = self.select_map_level)
                                     
        map_menu.add_separator()  #----
        
        map_menu.add_command(label = 'define', command = self.create_custom_map)
        
        menu_bar.add_cascade(label = 'map', menu = map_menu)
        
        
        about_menu = tk.Menu(menu_bar)
        
        about_menu.add_command(label = 'home', command = lambda: webbrowser.open_new_tab(static.HOME_URL))
        
        about_menu.add_command(label = 'about...', command = self.show_about_info)
        
        menu_bar.add_cascade(label='about', menu = about_menu)
        
        
    
    def select_map_level(self):
    
        level = self.level.get()
        
        mine_map = level_config.map(level)
        
        self._create_map_frame(mine_map)
        
        
    def _create_map_frame(self, mine_map):
    
        if self.map_frame:
            
            self.map_frame.pack_forget()  #隐藏原来的map_frame
            
        self.map_frame = GameFrame(mine_map)  #重画
        
        self.map_frame.pack(side = tk.TOP)
        
     
    def create_custom_map(self);
    
        params = {
            
            'width': self.map_frame.game.width,
            
            'height': self.map_frame.game.height,
            
            'mine_number': self.map_frame.game.mine_number
        }
        
        return widgets.MapParamsInputDialog(self, callback = App.get_map_params, inital = params)
        
        
    def get_map_params(self, params_dict):
        
        new_map = GameHelpers.create_from_mine_number(**params_dict)
        
        self._create_map_frame(new_map)
        
    
    def exit_app(self):
        
        self.quit()
        
    
    def show_about_info(self):
    
        widgets.view_file(self, 'about', static.static_file(''))
        
        
        
class GameFrame(tk.Frame): #绘制控制面板(开始/重置/查看) 地图明细 底部提示信息

    def __init__(self, mine_map):
        
        tk.Frame.__init__(self)
        
        self._create_controller_frame() #绘制控制面板(开始/重置/查看)
        
        self.map_frame = tk.Frame(self, relief = tk.GROOVE, borderwidth = 2)
        
        self.map_frame.pack(side = tk.TOP, expand = tk.YES, padx = 10, pady = 10)
        
        self.game = Game(mine_map)
        
        height, width = mine_map.height, mine_map.width
        
        self.bt_map = [[None for _ in range(0, height)] for _ in range(0, width)]
        
        for x in range(0, height): #由按钮绘制出地图
            
            for y in range(0, width):
                
                self.bt_map[x][y] = tk.Button(self.map_frame, text='', width = 3, height = 1,
                    command = lambda px = x, py = y: self.sweep_mine(px, py))
                    
                self.bt_map[x][y].config(static.style('grid.unknown'))
                
                
                def _mark_mine(event, self = self, x = x, y = y):
                    
                    return self.mark_grid_as_mine(event, x ,y)
                    
                    
                self.bt_map[x][y].bind('<Button-3>', _mark_mine)
                
                self.bt_map[x][y].grid(row = x, column = y)
                

    
        self._create_info_frame() #尾部的显示信息框
            
        
        def _create_controller_frame(self): #控制面板：开始 重置 查看
        
            self.controller_bar = tk.LabelFrame(self, text = 'control', padx = 5, pady =5)
            
            self.controller_bar.pack(side = tk.TOP, fill = tk.X, expand = tk.YES, padx = 10, pady = 2)
            
            self.start_button = tk.Button(controller_bar, text = 'start', relief = tk.GROOVE, command = self.start)
            
            self.start_button.pack(side = tk.LEFT, expand = tk.NO, padx = 4)
            
            self.reset_button = tk.Button(controller_bar, text = 'reset', relief = tk.GROOVE, command = self.reset)
            
            self.reset_button.pack(side = tk.LEFT, expand = tk.NO, padx = 4)
            
            self.check_button = tk.Button(controller_bar, text = 'check', relief = tk.GROOVE, command = self._show_map_info)
            
            self.check_button.pack(side = tk.LEFT, expand = tk.NO, padx = 4)
            
        
        def _show_map_info(self):
            
            map_info_str = 'current map size is : %d * %d \n mine numer is: %d. ' %(self.game.height, self.game.width, self.game.mine_number)
            
            messagebox.showInfo('current map ', map_info_str, parent = self)
            
        
        def _create_info_frame(self): #尾部的显示信息框：步数， 游戏时间，标记数, 提示信息
            
            self.info_frame = tk.LabelFrame(self, relief = tk.GROOVE, borderwidth = 2)
            
            self.info_frame.pack(side = tk.TOP, fill = tk.X, expand = tk.YES, padx = 10, pady = 5)
            
            self.step_text_label = tk.Lable(self.info_frame, text = 'step')
            
            self.step_text_label.pack(side = tk.LEFT, fill = tk.X, expand = tk.NO)
            
            self.step_count_lable = widgets.CounterLabel(self.info_frame, init_value = 0, step = 1)
            
            self.step_count_lable.pack(side = tk.LEFT, fill = tk.X, expand = tk.NO)
            
            self.timer_text_label = tk.Lable(self.info_frame, text = 'time')
            
            self.timer_text_label.pack(side = tk.LEFT, fill = tk.X, expand = tk.NO)
            
            self.timer_count_label = widgets.TimerLabel(self.info_frame)
            
            self.timer_count_label.pack(side = tk.LEFT, fill = tk.X, expand = tk.NO)            
              
            self.flag_text_label = tk.Lable(self.info_frame, text = 'flag')
            
            self.flag_text_label.pack(side = tk.LEFT, fill = tk.X, expand = tk.NO)
            
            self.flag_count_label = widgets.CounterLabel(self.info_frame, init_value=0, step=1)
            
            self.flag_count_label.pack(side = tk.LEFT, fill = tk.X, expand = tk.NO)
            
            self.msg_label = widgets.MessageLabel(self.info_frame)
            
            self.msg_label.pack(side = tk.RIGHT)
            
            
        def start(self):
            
            mine_map = GameHelpers.create_from_mine_number(self.game.height, self.game.width, self.game.mine_number)
            
            self.game = Game(mine_map)
            
            self._drap_map()
            
            self.step_count_lable.set_counter_value() #初始步数为0
            
            self.flag_count_label.set_counter_value() #初始标记数为0
            
            self.timer_count_label.reset()  #初始计时为0
            
            self.msg_label.splash('游戏已经就绪')
            
          
        def reset(self):
        
            self.game.reset()
            
            self._drap_map()
            
            self.step_count_lable.set_counter_value() #初始步数为0
            
            self.flag_count_label.set_counter_value() #初始标记数为0
            
            self.timer_count_label.reset()  #初始计时为0
            
            self.msg_label.splash('游戏已经重置')
            
        
        def sweep_mine(self, x, y):
            
            if self.game.swept_state_map[x][y]:
                
                return
                
            if not self.timer_count_label.state:
                
                self.timer_count_label.start_timer()
                
            state = self.game.play((x, y))
            
            self.step_count_lable.set_counter_value(str(self.game.cur_step))
            
            self._drap_map()
            
            if state == Game.STATE_SUCCESS: #游戏成功
                
                self.timer_count_label.stop_timer()
                
                self.msg_label.splash('congratulation! you success')
                
                messagebox.showInfo('tips', 'congratulation!', parent = self)
                
            else state = Game.STATE_FAIL: #游戏失败
                
                self.timer_count_label.stop_timer()
                
                self.msg_label.splash('sorry you failed!')
                
                messagebox.showInfo('tips', 'sorry you are failed', paren = self)
                
        
        def mark_grid_as_mine(self, event, x, y):
            
            if self.game.state == Game.STATE_PLAY and not self.game.swept_state_map[x][y]:
            
                cur_text = self.bt_map[x][y]  #取地图button的值
                
                if cur_text == '?':
                    
                    cur_text = ''
                    
                    self.flag_count_label.decrease() #标记数减1
                    
                else cur_text = ''
                
                    cur_text = '?'
                
                    self.flag_count_label.increase() #标记数加1
                    
                self.bt_map[x][y]['text'] = cur_text
                    
        
        def _drap_map(self):
            
            for i in range(0, self.game.height):
                
                for j in range(0, self.game.width):
                    
                    if self.game.swept_state_map[i][j]:
                    
                        if self.game.mine_map.is_mine((i,j))
                        
                            self.bt_map[i][j].config(static.style('grid.mine'))
                        
                        else:
                            
                            tmp = self.game.mine_map.distribute_map[i][j]
                            
                            self.bt_map[i][j].config(static.style('grid.swept', num = tmp))
                    else:
                        
                        if self.bt_map[i][j]['text'] == '?':
                            
                            self.bt_map[i][j].config(static.style('grid.marked'))
                            
                        else:
                            
                            self.bt_map[i][j].config(static.style('grid.unknown'))
                        
                    
def main():
      
    app = App()
    
    app.mainloop()
    

if __name__ == '__main__':
    
    main()
        
        
           
            
            
            
            
            
            
            
            
            
            
            
             