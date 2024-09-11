import tkinter as tk
import tkinter.ttk as ttk
def f窗口居中(a窗口: tk.Tk, a客户区宽: int = 0, a客户区高: int = 0):	#在创建窗口后主循环前调用
	v宽 = a客户区宽 or a窗口.winfo_width()
	v高 = a客户区高 or a窗口.winfo_height()
	v屏幕宽 = a窗口.winfo_screenwidth()
	v屏幕高 = a窗口.winfo_screenheight()
	x = int((v屏幕宽 - v宽) / 2)
	y = int((v屏幕高 - v高) / 2)
	a窗口.geometry('{}x{}+{}+{}'.format(v宽, v高, x, y))
v样式 = None
def f初始化样式():
	global v样式
	if v样式:
		return
	v样式 = ttk.Style()
	v样式.map("TEntry",
		foreground = [("invalid", "red") ]
	)