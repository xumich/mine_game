# coding:utf-8
try:

    import tkinter as tk

except ImportError:

    import Tkinter as tk

try:

    from tkinter import messagebox

except ImportError:

    import tkMessageBox as messagebox

from io import open

class CounterLabel(tk.Label):
    def __init__(self, parent, init_value = 0, step = 1, **kwargs):
        self._count_value = tk.IntVar()
        self._count_value.set(init_value)
        tk.Label.__init__(self, parent, textvariable=self._count_value, **kwargs)
        self._step = step

    def increase(self, step = None):
        step = step or self._step
        self._count_value.set(self._count_value.get() + step)

    def decrease(self, step=None):
        step = step or self._step
        self._count_value.set(self._count_value.get() - step)

    def set_counter_value(self, value = 0):
        self._count_value.set(value)

    @property
    def count_value(self):
        return self._count_value.get()


class TimerLabel(CounterLabel):

    def __init__(self, parent, **kwargs):
        CounterLabel.__init__(self, parent, **kwargs)
        self._state = False
        self._timer_id = None

    def _timer(self):
        if self._state:
            self.increase()
            self._timer_id = self.after(1000, self._timer)

    def start_timer(self):
        if not self._state:
            self._state = True
            self._timer()

    def stop_timer(self):
        if self._state:
            self._state = False
            self._timer_id = None

    def reset(self):
        self.stop_timer()
        self.set_counter_value()

    @property
    def state(self):
        return self._state

class MessageLabel(tk.Label):

    def tipInfo(self, text):
        self.config({'text': text})
        self.after(700,self._clear)

    def _clear(self):
        self.config({'text': ''})

class CustomMap(tk.Toplevel):
    def __init__(self, parent, modal=True, callback=None, initial=None):
        tk.Toplevel.__init__(self, parent)
        initial = initial or {'width': 10, 'height': 10, 'mine_number': 10}
        self.height = tk.IntVar(value=initial['height'])
        self.width = tk.IntVar(value=initial['width'])
        self.mine_number = tk.IntVar(value=initial['mine_number'])
        self.validate_msg = tk.StringVar()

        self.create_widget()
        self.parent = parent
        self.title('input the parameters')

        self.bind('<Return>', self.quit)
        self.bind('<Escape>', self.quit)
        self.callback = callback

        if modal:
            self.geometry('=%dx%d+%d+%d'%(200,200,parent.winfo_rootx()+10, parent.winfo_rooty()+10))
            self.transient(parent)
            self.grab_set()
            self.wait_window()

    def create_widget(self):
        frame = tk.Frame(self)
        frame.pack()
        tk.Label(frame, text='map height').grid(column=0, row=0)
        tk.Entry(frame, textvariable=self.height).grid(column=1, row=0)

        tk.Label(frame, text='map width').grid(column=0, row=1)
        tk.Entry(frame, textvariable=self.width).grid(column=1, row=1)

        tk.Label(frame, text='map mine_number').grid(column=0, row=2)
        tk.Entry(frame, textvariable=self.mine_number).grid(column=1, row=2)
        tk.Entry(frame, fg='#FF0000', textvariable=self.validate_msg, state=tk.DISABLED).grid(column=0, row=3, columnspan=2) #校验提示信息

        tk.Button(frame, text='ok', command=self.ok).grid(column=0, row=4, ipadx=10)
        tk.Button(frame, text='cancel', command=self.destroy).grid(column=1, row=4, ipadx=10)

    def ok(self):
        if self.callback:
            try:
                height, width, mine_number = int(self.height.get()), int(self.width.get()), int(self.mine_number.get())
            except ValueError:
                self.validate_msg.set('please input number')
                return
            if height < 3 or width < 3:
                self.validate_msg.set('地图长度必须大于等于3！')
                return
            if mine_number < 0 or height * width <= mine_number:
                self.validate_msg.set('地图数目范围不正确！')
                return

            self.validate_msg.set('')
            map_params_dict = {
                'height': height,
                'width': width,
                'mine_number': mine_number
            }
            self.destroy()
            self.callback(self.parent, map_params_dict) # 回调函数　call fucntion: get_map_params(self, params_dict)












