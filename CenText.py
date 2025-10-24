# CenText.py
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
import hashlib

class CenText(tk.PanedWindow):
    INPUT_NULL = -1
    INPUT_SAME = -2

    def __init__(self):
        super(CenText, self).__init__()
        self.config(orient=tk.HORIZONTAL)
        self.init_widgets()
        self.info_area.tag_configure('font1', font=('宋体', 10, 'bold'), foreground='red')
        self.info_area.tag_configure('font2', font=('楷体', 10, 'bold'), foreground='black')
        self.prev_encoding = ''

    def init_widgets(self):
        self.input_area = ScrolledText()  
        self.info_area  = tk.Text(wrap=tk.NONE)
        self.set_info_disable()
        self.add(self.input_area)
        self.add(self.info_area)

    def add_info(self, text, font='font2'):
        cur_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        self.set_info_normal()
        self.info_area.insert(tk.END, f'{cur_time} {text}\n', font)
        self.set_info_disable()

    def get_text(self):
        content = self.input_area.get('1.0', tk.END).strip()
        if len(content) == 0:
            return CenText.INPUT_NULL
        h = hashlib.sha256()
        h.update(content.encode())
        cur_encoding = h.hexdigest()
        if cur_encoding == self.prev_encoding:
            return CenText.INPUT_SAME
        self.prev_encoding = cur_encoding
        return content

    def set_info_disable(self):
        self.info_area.config(state='disabled')

    def set_info_normal(self):
        self.info_area.config(state='normal')
