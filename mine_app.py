# coding:utf-8
import tkinter as tk
import os
import sys
from maphelper import level_config
import baseData
from minecore import Game


class MineApp(tk.Frame):

    def __init__(self):
        print("__init__")
        tk.Frame.__init__(self)
        self.master.title("my mine game")
        self.master.resizable(False, False)
        self.master.iconbitmap(baseData.images('mine.ico'))
        self.pack(expand=tk.NO, fill=tk.BOTH)
        self.map_frame = None

        mine_map = level_config.map('primary')
        print('mine_map:%s' % mine_map.mine_map_list)
        print('mine_map.mine_map_list:%s'%mine_map._distribute_map)

        self._create_map_frame(mine_map)

        self.create_top_menu()

    def _create_map_frame(self, mine_map):
        if self.map_frame:
            #隐藏显示
            self.master.pack_forget()
        else:
            self.map_frame = GameFrame(mine_map)


    def create_top_menu(self):
        pass

class GameFrame(tk.Frame):

    def __init__(self, mine_map):
        tk.Frame.__init__(self)

        self._create_controller_frame()

        self.map_frame = tk.Frame(self, relief=tk.GROOVE, borderwidth=2)
        self.map_frame.pack(side=tk.TOP, expand=tk.YES, padx=10, pady=10)
        self.game = Game(mine_map)
        height, width = mine_map.height, mine_map.width
        self.bt_map = [[None for _ in range(0, width)] for _ in range(0, height)]
        for x in range(0, height):
            for y in range(0, width):
                self.bt_map[x][y] = tk.Button(self.map_frame,text='', width=3, height=1,
                                              command=lambda px=x, py=y: self.sweep_mine(px, py))
                self.bt_map[x][y].config(baseData.style('grid.unknown'))

    def _create_controller_frame(self):
        self.controller_bar = tk.LabelFrame(self, text='control',padx=5, pady=5)
        self.controller_bar.pack(side=tk.TOP, fill=tk.X, expand=tk.YES, padx=10, pady=2)
        self.bt_start = tk.Button( self.controller_bar, text='start', relief=tk.GROOVE)
        self.bt_start.pack(side=tk.LEFT, expand=tk.NO, padx=4)
        self.bt_reset = tk.Button(self.controller_bar, text='reset', relief=tk.GROOVE)
        self.bt_reset.pack(side=tk.LEFT, expand=tk.NO, padx=4)
        self.bt_check = tk.Button(self.controller_bar, text='check', relief=tk.GROOVE)
        self.bt_check.pack(side=tk.LEFT, expand=tk.NO, padx=4)

    def _show_map_info(self):

        map_info_str = '当前地图大小：%d X %d\n地雷数目：%d' % (self.game.height, self.game.width, self.game.mine_number)

        messagebox.showinfo('当前地图', map_info_str, parent=self)



if __name__ == "__main__":
    app = MineApp()
    app.mainloop()
