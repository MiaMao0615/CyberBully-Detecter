import tkinter as tk


class StatBar(tk.Frame):

    def __init__(self):
        super(StatBar, self).__init__()
        # 设置控件背景颜色
        self.config(bg='#95afc0')
        # 标签子控件
        self.message = tk.Label(self, text='准备就绪', bg='#95afc0')
        self.message.pack(side=tk.LEFT)

    def set_message(self, text):
        self.message['text'] = text


if __name__ == '__main__':
    window = tk.Tk()
    window.geometry('500x300+200+200')

    sbar = StatBar()
    sbar.pack(side=tk.BOTTOM, fill=tk.X)

    button = tk.Button(text='按钮', command=lambda : sbar.set_message('修改文字'))
    button.pack(side=tk.TOP)

    window.mainloop()


    