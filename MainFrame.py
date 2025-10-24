# MainFrame.py
import tkinter as tk
from CyberBullyRecognizer import CyberBullyRecognizer   # ← 改成新分类器
from TopMenu import TopMenu
from StatBar import StatBar
from CenText import CenText

class MainFrame(tk.Tk):
    def __init__(self):
        super(MainFrame, self).__init__()
        self.window_w, self.window_h = 800, 500
        screen_w, screen_h = self.winfo_screenwidth(), self.winfo_screenheight()
        screen_x, screen_y = int(screen_w/2 - self.window_w/2), int(screen_h/2 - self.window_h/2)
        self.geometry(f'{self.window_w}x{self.window_h}+{screen_x}+{screen_y}')
        self.title('网络暴力识别器')  # ← 统一窗口名称
        self.init_widgets()
        # 0=正常，1=网络暴力（与你的数据一致）
        self.recognizer = CyberBullyRecognizer(label_map={1: '网络暴力言论', 0: '正常言论'})

    def init_widgets(self):
        self.menu = TopMenu(predict_function=self.on_menu_predict)
        self.config(menu=self.menu)
        self.text = CenText()
        self.text.pack(fill=tk.BOTH, expand=True)
        self.sbar = StatBar()
        self.sbar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_menu_predict(self):
        text = self.text.get_text()   # ← 统一为文本名称
        if text == CenText.INPUT_NULL:
            self.text.add_info('文本为空!', font='font1'); return
        if text == CenText.INPUT_SAME:
            self.text.add_info('文本未变化!', font='font1'); return
        self.sbar.set_message('正在检测...')
        labels = self.recognizer.predict([text])
        self.text.add_info(f'预测结果: {labels[0]}')
        self.sbar.set_message('检测完成')

    def show(self):
        self.mainloop()
