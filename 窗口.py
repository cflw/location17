import ctypes
import tkinter as tk
import tkinter.ttk as ttk
v窗口缩放 = 1
v系统缩放 = 1
c间距 = 4
def f开启高分屏适配():
	global v窗口缩放, v系统缩放, c间距
	ctypes.windll.shcore.SetProcessDpiAwareness(1)
	ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
	v窗口缩放 = ScaleFactor / 75
	v系统缩放 = ScaleFactor / 100
	c间距 = int(4 * v系统缩放)
def fg窗口缩放():
	return v窗口缩放
def fg系统缩放():
	return v系统缩放
def f窗口居中(a窗口: tk.Tk, a客户区宽: int = 0, a客户区高: int = 0):
	"""再创建窗口后调用, 自动计算缩放"""
	v窗口宽 = int(a客户区宽) or a窗口.winfo_width()
	v窗口高 = int(a客户区高) or a窗口.winfo_height()
	v屏幕宽 = a窗口.winfo_screenwidth()
	v屏幕高 = a窗口.winfo_screenheight()
	x = int((v屏幕宽 - v窗口宽) / 2)
	y = int((v屏幕高 - v窗口高) / 2)
	a窗口.geometry('{}x{}+{}+{}'.format(v窗口宽, v窗口高, x, y))
v样式 = None
def f初始化样式():
	global v样式
	if v样式:
		return
	v样式 = ttk.Style()
	v样式.configure("Treeview", rowheight = int(20 * v系统缩放))
	v样式.map("TEntry",
		foreground = [("invalid", "red") ]
	)