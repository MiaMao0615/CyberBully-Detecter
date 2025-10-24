# TopMenu.py
import tkinter as tk
import sys

class TopMenu(tk.Menu):
    def __init__(self, predict_function):
        super(TopMenu, self).__init__()
        self.predict_function = predict_function
        self.file_menu()
        self.detect_menu()
        self.help_menu()

    def file_menu(self):
        file_menu = tk.Menu(tearoff=False)
        file_menu.add_command(label='打开')
        file_menu.add_separator()
        file_menu.add_command(label='退出', command=sys.exit)
        self.add_cascade(label='文件', menu=file_menu)

    
    def detect_menu(self):
        detect_menu = tk.Menu(tearoff=False)
        detect_menu.add_command(label='检测', command=self.predict_function)
        self.add_cascade(label='检测', menu=detect_menu)

    def help_menu(self):
        help_menu = tk.Menu(tearoff=False)
        help_menu.add_command(label='关于')
        self.add_cascade(label='帮助', menu=help_menu)
