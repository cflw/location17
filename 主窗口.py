import ctypes
import tkinter as tk
import tkinter.ttk as ttk
import async_tkinter_loop	#async-tkinter-loop
import 窗口
import 日志
class W主窗口(tk.Tk):
	def __init__(self, a地址管理, a手机管理):
		ctypes.windll.shcore.SetProcessDpiAwareness(1)
		ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
		tk.Tk.__init__(self)
		self.tk.call("tk", "scaling", ScaleFactor / 75)
		self.title("Location17")
		窗口.f窗口居中(self, 306, 462)
		self.resizable(False, False)
		#变量
		self.m地址管理 = a地址管理
		self.m地址管理.f打开文件()
		self.m手机管理 = a手机管理
		self.m手机管理.f刷新列表()
		self.m选择地址 = 0
		self.m选择手机 = 0
		#地址&手机
		self.w地址框架 = ttk.LabelFrame(self, text = "虚拟定位",width = 400, height = 400)
		self.w地址框架.grid(row = 0, rowspan = 1, column = 0, columnspan = 1, padx = 4, pady = 4)
		self.w地址标签 = ttk.Label(self.w地址框架, text = "地址：")
		self.w地址标签.grid(row = 0, rowspan = 1, column = 0, columnspan = 1, padx = 4, pady = 4, sticky = "E")
		self.w地址 = ttk.Combobox(self.w地址框架, values = list(self.m地址管理.fe地址名称()), state = "readonly")
		self.w地址.bind("<<ComboboxSelected>>", self.f事件_地址被选择)
		self.w地址.grid(row = 0, rowspan = 1, column = 1, columnspan = 5, padx = 4, pady = 4, sticky = "EW")
		self.w手机标签 = ttk.Label(self.w地址框架, text = "手机：")
		self.w手机标签.grid(row = 1, rowspan = 1, column = 0, columnspan = 1, padx = 4, pady = 4, sticky = "E")
		self.w手机 = ttk.Combobox(self.w地址框架, values = list(self.m手机管理.fe显示名称()),state = "readonly")
		self.w手机.grid(row = 1, rowspan = 1, column = 1, columnspan = 5, padx = 4, pady = 4, sticky = "EW")
		self.w地址管理 = ttk.Button(self.w地址框架, text = "地址管理", command = self.f按钮_地址管理)
		self.w地址管理.grid(row = 2, rowspan = 1, column = 0, columnspan = 2, padx = 4, pady = 4)
		self.w修改定位 = ttk.Button(self.w地址框架, text = "修改定位", command = self.f按钮_修改定位)
		self.w修改定位.grid(row = 2, rowspan = 1, column = 2, columnspan = 2, padx = 4, pady = 4)
		self.w还原定位 = ttk.Button(self.w地址框架, text = "还原定位", command = self.f按钮_还原定位)
		self.w还原定位.grid(row = 2, rowspan = 1, column = 4, columnspan = 2, padx = 4, pady = 4)
		#日志
		self.w日志框架 = ttk.LabelFrame(self, text = "日志")
		self.w日志框架.grid(row = 1, column = 0, padx = 4, pady = 4)
		self.w清空日志 = ttk.Button(self.w日志框架, text = "清空日志", command = self.f按钮_清空日志)
		self.w清空日志.pack(side = "top", padx = 4, pady = 4)
		self.w日志 = tk.Text(self.w日志框架, height = 20, width = 40)
		self.w日志.pack(side = "top", fill = "both", padx = 4, pady = 4)
		#子窗口
		self.w子窗口 = None
		#其他
		if self.m地址管理.fi有地址():
			self.w地址.current(0)
		if self.m手机管理.fi有手机():
			self.w手机.current(0)
		self.m日志框处理器 = 日志.g文本框处理器
		self.bind("<Visibility>", self.f事件_加载)
		self.bind("<Destroy>", self.f事件_关闭)
		self.m更新事件 = self.f事件_更新()
	def f事件_更新(self):
		self.m日志框处理器.f更新()
		self.m更新事件 = self.after(10, self.f事件_更新)
	def f事件_加载(self, e):
		if e.widget == self:
			self.unbind("<Visibility>")
			self.m日志框处理器.f启用(self.w日志)
			日志.f调试("窗口加载")
	def f事件_关闭(self, e):
		if e.widget == self:
			self.m日志框处理器.f关闭()
			self.after_cancel(self.m更新事件)
			日志.f调试("窗口关闭")
	def f按钮_地址管理(self):
		import 地址管理窗口
		if not self.w子窗口 or not self.w子窗口.winfo_exists():
			self.w子窗口 = 地址管理窗口.W地址管理(self, self.m地址管理)
	@async_tkinter_loop.async_handler
	async def f按钮_修改定位(self):
		v地址 = self.fg选择地址()
		if not v地址:
			日志.f告警("未选择地址")
			return
		v手机 = self.fg选择手机()
		if not v手机:
			日志.f告警("未选择手机")
			return
		日志.f信息(f"修改定位: 手机={v手机.fg设备名称()}, 经度={v地址.m经度}, 纬度={v地址.m纬度}")
		v结果 = await v手机.f修改定位(a经度 = v地址.m经度, a纬度 = v地址.m纬度)
		if v结果:
			日志.f信息("修改定位成功")
		else:
			日志.f信息("修改定位失败")
	@async_tkinter_loop.async_handler
	async def f按钮_还原定位(self):
		v手机 = self.fg选择手机()
		if not v手机:
			日志.f告警("未选择手机")
			return
		日志.f信息(f"还原定位: 手机={v手机.fg设备名称()}")
		v结果 = await v手机.f还原定位()
		if v结果:
			日志.f信息("还原定位成功")
		else:
			日志.f信息("还原定位失败")
	def f按钮_清空日志(self):
		self.w日志.delete(1.0, "end")
	def fg选择手机(self):
		v选择 = self.w手机.current()
		if v选择 == -1:
			return None
		return self.m手机管理[v选择]
	def fg选择地址(self):
		v选择 = self.w地址.current()
		if v选择 == -1:
			return None
		return self.m地址管理[v选择]
	def f写入日志(self, a内容: str):
		self.w日志.insert("end", "\r\n" + a内容)
	def f刷新地址(self):
		self.w地址["value"] = list(self.m地址管理.fe地址名称())
		v地址数量 = self.m地址管理.fg地址数量()
		if v地址数量 <= self.m选择地址:	#刷新后的地址数量可能比选择索引小
			self.m选择地址 = v地址数量 - 1
		self.w地址.current(self.m选择地址)
		日志.f调试("刷新地址")
	def f事件_地址被选择(self, event):
		w选择框 = event.widget
		self.m选择地址 = v选择 = w选择框.current()
		日志.f调试(f"选择地址: 选择={v选择}, 名称={self.m地址管理[v选择].m名称}")