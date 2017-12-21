#coding = utf-8

import  tkinter as tk

from tkinter import messagebox

from io import open

class CounterLabel(tk.label):
    
    def __init__(self, parent, init_value = 0, step = 1, **kwargs):
    
        self._count_value = tk.IntVar()
        
        self._count_value.set(init_value)
        
        tk.label.__init__(self, parent, textvariable = self._count_value, **kwargs)
        
        self._step = step
        
        
    def increase(self, step = None):
    
        step = step or self._step
        
        self._count_value.set(self._count_value.get() + step)
        
        
    def decrease(self, step = None):

        step = step or self._step

        self._count_value.set(self._count_value.get() - step)
        
        
    def set_counter_value(self, value = 0):
        
        self._count_value.set(value)
        
        
    @property
    
    def counter_value(self):
    
        return self._count_value.get()


class TimerLabel(CounterLabel):
    
    def __init__(self, parent, **kwargs):
        
        CounterLabel.__init__(self, parent, **kwargs)
        
        self._state = False
        
        self._timer_id = None
        
        
    def _timer(self):

        if self._state:
            
            self.increase()
            
            self._timer_id = self.after(1000, _timer) # every 1 sec trigger _timer
        
        
    def start_timer(self):
        
        if not self.state:
            
            self._state = True
            
            self._timer()
            
        
    def stop_timer(self):
    
        self._state = False
        
        if self._timer_id:
        
            self.after_cancel(self._timer_id)
            
            self._timer_id = None
            
            
    def reset(self):
    
        self.stop_timer()
        
        self.set_counter_value()
           
        
    @property
    
    def timer_state()
        
        return self._state


class MapParamsInputDialog(tk.Toplevel):
    
    def __init__(self, parent, modal = True, callback = None, initial = None):
        
        tk.Toplevel.__init__(self, parent)
        
        initial = initial or {'width' : 10, 'height': 10, 'mine_number': 10}
        
        self.height = tk.Intvar(value = initial['height'])
        
        self.width = tk.IntVar(value = initial['width'])
        
        self.mine_number = tk.Intvar(value = initial['mine_number'])
        
        self.validate_msg = tk.StringVar()
        
        
        self.create_widgets()
        
        self.parent = parent
        
        self.title('please input new map parameters')
        
        
        self.bind('<Return>', self.bind_quit)  #dismiss dialog
        
        self.bind('<Escape>', self.bind_quit)  #dismiss dialog
        
        self.callback = callback
        
        if modal:
            
            self.geometry('= %dx %d + %d + %d ' %(200, 130, parent.winfo_rootx() + 10, parent.winfo_rooty() + 10))
            
            self.transient(parent)
            
            self.grab_set()
            
            self.wait_window()
            
    
    def create_widgets(self):
        
        frame = tk.Frame(self)
        
        frame.pack(side = tk.TOP, expand = tk.TRUE, fill = tk.BOTH)
        
        tk.Label(frame, text = 'map height').grid(column = 0, row = 0)
        
        tk.Entry(frame, textvariable = self.height).grid(column = 1, row = 0)
        
        tk.Label(frame, text = 'map width').grid(column = 0, row = 1)
        
        tk.Entry(frame, textvariable = self.width).grid(column = 1, row = 1)
        
        tk.Label(frame, text = 'mine number').grid(column = 0, row = 2)
        
        tk.Entry(frame, textvariable = self.mine_number).grid(column = 1, row = 2)
        
        tk.Entry(frame, fg = '#FF0000', textvariable = self.validate_msg, state = tk.DISABLED).grid(
        column = 0, row = 3, columnspan = 2)
        
        tk.Button(frame, text = 'ok', command = self.ok).grid(column = 0 , row =4, ipadx = 10)
        
        tk.Button(frame, text = 'cancel', command = self.cancel).grid(column = 1 , row =4, ipadx = 10)
        
    
    def ok(self):
        
        if self.callback:
            
            try:
                
                height, width, mine_number = int(self.height.get()), int(self.width.get()), int(self.mine_number.get())
            
            except: ValueError
            
                self.validate_msg.set('please input integer number')
                
            if height < 3 pr width < 3:
                
                self.validate_msg.set('must be over 3')
                
                return
                
            if mine_number < 0 or height * width <= mine_number:
                
                self.validate_msg.set('out of range')
                
                return
                
            self.validate_msg.set('')
            
            map_params_dict = {
                
                'height': height,
                
                'width': width,
                
                'mine_number': mine_number

                }
                
            self.destroy()
            
            self.callback(self.parent, map_params_dict)
                
              
    def cancel(self):
        
        self.destroy()
    
    
    def bind_quit(self, event):
        
        self.cancel()
        

class MessageLabel(tk.Label):
    
    def splash(self, text):
        
        self.config({'text': text})
        
        self.after(700, self._clear)
        
        
    def _clear(self):
        
        self.config({'text': ''})
        
        
class TextViewer(tk.Toplevel):
        
        def __init__(self, parent, title, text, modal = True):
            
            tk.Toplevel.__init__(self, parent)
            
            self.configure(borderwidth = 5)
            
            self.geometry("=%dx%d+%d+%d" % (625, 500, parent.winfo_rootx() + 10, parent.winfo_rooty() + 10))
            
            self.bg = '#ffffff'
            
            self.fg = '#000000'
            
            self.title(title)
            
            self.protocol("WM_DELETE_WINDOW", self.ok) #绑定用户点击关闭按钮事件
            
            self.parent = parent
            
            self.bind('<Return>', self.ok) #绑定键盘回车事件
            
            self.bind('<Escape>', self.ok) #绑定键盘退出事件
            
            
            frame_text = tk.Frame(self, relief = tk.SUNKEN, height = 700)
            
            frame_text.pack(side = tk.TOP, expand = tk.TRUE, fill = tk.BOTH)
            
            
            scroll_view = tk.Scrollbar(frame_text, orient = tk.VERTICAL, takefocus = tk.FALSE, highlightthickness = 0)
            
            self.text_view = tk.Text(frame_text, wrap = tk.WORD, highlightthickness = 0, fg = self.fg, bg = self.bg)
            
            scroll_view.config(command = self.text_view.yview)
            
            self.text_view.pack(side = tk.LEFT, expand = tk.TRUE, takefocus = tk.BOTH)
            
            
            frame_buttons = tk.Frame(self)
            
            tk.button(frame_buttons, text = 'ok', command = self.ok, takefocus = tk.FALSE).pack()
            
            frame_buttons.pack(side = tk.BOTTOM, fill = tk.X)
            
            #init text
            
            self.text_view.focus_set()
            
            self.text_view.insert(0, 0, text)
            
            self.text_view.config(state = tk.DISABLED)
            
            if modal:
                
                self.transient(parent) #通知parent window，此视图必须一直出现在parent的顶层。
                
                self.grab_set() #grab_set ensures that all of the application's events are sent to self until a corresponding call to grab_release
                
                self.wait_window()
                
                
        def ok(self, event = None):
        
            self.destroy()
            
            
def view_file(parent, title, fileName, model = True):
    
    try:
        
        text_file = open(fileName, 'r', encodeing = 'utf-8')
    
    except IOError:
    
        messagebox.showerror(title = 'File load Error', message ='unable to load the file %r.' %fileName)
        
    else:
    
        return TextViewer(parent, title, text_file.read(), modal)

        
  
        
        
        
if __init__ == '__main__':
    
    root = tk()
    
    coutner = CounterLabel(root)
    
    root.mainloop()