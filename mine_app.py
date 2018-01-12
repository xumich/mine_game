# coding:utf-8
import tkinter as tk
import webbrowser
from mine_static import levelConfig
from tkinter import messagebox
import mine_style
from mine_core import Game
import mine_widget
from mine_helper import MineHelper


class GameFrame(tk.Frame):
    def __init__(self, mine_map):
        tk.Frame.__init__(self)
        self._create_controller_frame() #控制按钮块
        self.map_frame = tk.Frame(self, relief=tk.GROOVE, borderwidth=2)
        self.map_frame.pack(side=tk.TOP, expand=tk.YES, padx=10, pady=10)
        self.game = Game(mine_map) #初始化游戏信息 self.game.state, self.game.cur_step,self.game.swept_state_map...
        height, width = mine_map.height, mine_map.width
        self.bt_map = [[None for _ in range(0, width)] for _ in range(0, height)]
        for x in range(0, height):
            for y in range(0, width):
                self.bt_map[x][y] = tk.Button(self.map_frame, text='', width=3, height=1,
                                              command=lambda px=x, py=y: self._sweep_mine(px, py))  #地图按钮绑定扫雷事件
                self.bt_map[x][y].config(mine_style.style('grid.unknown'))

                def _mark_mine(event, self=self, x=x, y=y):
                    return self.mark_grid_as_mine(event, x, y) #标记为地雷

                self.bt_map[x][y].bind('<Button-3>', _mark_mine) #鼠标右击事件
                self.bt_map[x][y].grid(row=x, column=y)
        self._create_info_frame()  # 游戏提示信息

    def _sweep_mine(self, x, y):
        if self.game.swept_state_map[x][y]: #扫过的位置
            return
        if not self.time_count_label.state:
            self.time_count_label.start_timer()
        state = self.game.play((x, y)) #游戏状态
        self.step_count_label.set_counter_value(str(self.game.cur_step))
        self._draw_map()
        if state == Game.GAME_FAIL:
            self.time_count_label.stop_timer()
            self.tips.tipInfo('sorry, you are fail')
            messagebox.showinfo('info', 'sorry', parent=self)
        elif state == Game.GAME_SUCCESS:
            self.time_count_label.stop_timer()
            self.tips.tipInfo('congratulation, you are success')
            messagebox.showerror('info', 'congratulation', parent=self)

    def _create_info_frame(self):
        self.info_frame = tk.Frame(self, relief=tk.GROOVE, borderwidth=2)
        self.info_frame.pack(side=tk.TOP, fill=tk.X, expand=tk.YES, padx=10, pady=5)
        self.step_text_label = tk.Label(self.info_frame, text='step')
        self.step_text_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.step_count_label = mine_widget.CounterLabel(self.info_frame, init_value=0, step=1)
        self.step_count_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.time_text_label = tk.Label(self.info_frame, text='time')
        self.time_text_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.time_count_label = mine_widget.TimerLabel(self.info_frame)
        self.time_count_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.flag_text_label = tk.Label(self.info_frame, text='flag')
        self.flag_text_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.flag_count_label = mine_widget.CounterLabel(self.info_frame, init_value=0, step=1)
        self.flag_count_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.tips = mine_widget.MessageLabel(self.info_frame)
        self.tips.pack(side=tk.RIGHT)

    def _draw_map(self):  # 地图的样式
        for i in range(0, self.game.height):
            for j in range(0, self.game.width):
                if self.game.swept_state_map[i][j]:  # 已经扫过的位置
                    if self.game.mine_map.is_mine((i, j)):
                        self.bt_map[i][j].config(mine_style.style('grid.mine'))
                    else:
                        temp = self.game.mine_map.distribute_map[i][j]
                        self.bt_map[i][j].config(mine_style.style('grid.swept', num=temp))
                else:  # 没有扫过的位置
                    if self.bt_map[i][j]['text'] == '?':
                        self.bt_map[i][j].config(mine_style.style('grid.marked'))
                    else:
                        self.bt_map[i][j].config(mine_style.style('grid.unknown'))

    def _create_controller_frame(self):
        self.controller_frame = tk.LabelFrame(self, text='control', padx=5, pady=5)
        self.controller_frame.pack(side=tk.TOP, fill=tk.X, expand=tk.YES, padx=10, pady=2)
        self.start_bt = tk.Button(self.controller_frame, text='start', relief=tk.GROOVE, command=self.start)
        self.start_bt.pack(side=tk.LEFT, expand=tk.NO, padx=4)
        self.reset_bt = tk.Button(self.controller_frame, text='reset', relief=tk.GROOVE, command=self.reset)
        self.reset_bt.pack(side=tk.LEFT, expand=tk.NO, padx=4)
        self.check_bt = tk.Button(self.controller_frame, text='check', relief=tk.GROOVE, command=self.check)
        self.check_bt.pack(side=tk.LEFT, expand=tk.NO, padx=4)

    def start(self):
        mine_map = MineHelper.create_from_mine_number(self.game.height, self.game.width, self.game.mine_number)
        self.game = Game(mine_map)
        self._draw_map() #地图按钮样式
        self.step_count_label.set_counter_value()
        self.flag_count_label.set_counter_value()
        self.time_count_label.reset()
        self.tips.tipInfo('game is ready!')

    def reset(self):
        self.game.game_reset()
        self._draw_map()
        self.step_count_label.set_counter_value()
        self.flag_count_label.set_counter_value()
        self.time_count_label.reset()
        self.tips.tipInfo('game is reset!')

    def check(self):
        map_info = 'map size is :%d * %d\n mine number is %d' % (
        self.game.height, self.game.width, self.game.mine_number)
        messagebox.showinfo(map_info)

    def mark_grid_as_mine(self, event, x, y):
        if self.game.state == Game.GAME_PLAY and not self.game.swept_state_map[x][y]:  # 游戏已经开始并且当前位置没有扫过
            cur_text = self.bt_map[x][y]['text']
            if cur_text == '?':
                cur_text = ''
                self.flag_count_label.decrease()
            elif cur_text == '':
                cur_text = '?'
                self.flag_count_label.increase()
            self.bt_map[x][y]['text'] = cur_text


class Mine_app(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title('mine_game')
        self.master.resizable(False, False)
        self.pack(expand=tk.NO, fill=tk.BOTH)
        self.map_frame = None

        mine_map = levelConfig.level_map('primary') #根据等级获取地雷游戏信息
        print mine_map.mine_list
        self._create_frame_map(mine_map) #游戏块：控制（开始／重置／查看），地图布置（按钮样式／扫雷算法判断），游戏信息块（步数／时间／标记）
        self.create_top_menu()  #游戏菜单下拉块

    def _create_frame_map(self, mine_map):
        if self.map_frame:
            self.map_frame.pack_forget()
        self.map_frame = GameFrame(mine_map)
        self.map_frame.pack(side=tk.TOP)

    def create_top_menu(self):
        top = self.winfo_toplevel()
        menu_bar = tk.Menu(top)
        top['menu'] = menu_bar
        game_menu = tk.Menu(menu_bar)
        game_menu.add_command(label='start', command=self.map_frame.start)
        game_menu.add_command(label='reset', command=self.map_frame.reset)
        game_menu.add_separator()
        game_menu.add_command(label='quit', command=self.quit)
        menu_bar.add_cascade(label='game', menu=game_menu)

        map_menu = tk.Menu(menu_bar)
        self.level = tk.StringVar()
        self.level.set('primary')
        for name, description in levelConfig.choices:
            map_menu.add_radiobutton(label=description,
                                     variable=self.level,
                                     value=name,
                                     command=self.select_map_level)
        map_menu.add_separator()
        map_menu.add_command(label='define', command=self.create_custom_map)
        menu_bar.add_cascade(label='map', menu=map_menu)

        about_menu = tk.Menu(menu_bar)
        about_menu.add_command(label='home', command=lambda: webbrowser.open_new_tab('www.google.com'))
        about_menu.add_command(label='about', command=self.show_about_info)
        menu_bar.add_cascade(label='about', menu=about_menu)

    def select_map_level(self):
        level = self.level.get() #获取选中的等级
        print level
        mine_map = levelConfig.level_map(level)
        self._create_frame_map(mine_map)

    def create_custom_map(self):
        params = {
            'width': self.map_frame.game.width,
            'height': self.map_frame.game.height,
            'mine_number': self.map_frame.game.mine_number
        }
        return mine_widget.CustomMap(self, callback=Mine_app.get_map_params, initial=params) #回调函数get_map_params

    def show_about_info(self):
        messagebox.showinfo('info', 'mine_map is : %d * %d and mine_number is:%d'%(self.map_frame.game.height, self.map_frame.game.width, self.map_frame.game.mine_number))

    def get_map_params(self, params_dict):
        new_map = MineHelper.create_from_mine_number(**params_dict) #key要相同
        self._create_frame_map(new_map)



def main():
    app = Mine_app()
    app.mainloop()


if __name__ == '__main__':
    main()
