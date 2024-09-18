import tkinter as tk
import tkinter.ttk as ttk
import 窗口
from 窗口 import c间距
c默认名称 = "新地址"
def F验证数值(a最小, a最大):
	def f验证数值(a值: str):
		try:
			v值 = float(a值)
			return a最小 <= v值 <= a最大
		except Exception as e:
			return False
	return f验证数值
f验证经度 = F验证数值(-180, 180)
f验证纬度 = F验证数值(-90, 90)
f验证偏移 = F验证数值(0, 99999)
def f取字符串变量(a变量: tk.StringVar, a默认值: str):
	v = a变量.get()
	return v if v else a默认值
class W地址管理(tk.Toplevel):
	def __init__(self, a父, a地址管理):
		tk.Toplevel.__init__(self, a父, width = 400)
		v系统缩放 = 窗口.fg系统缩放()
		self.title("地址管理")
		self.resizable(False, False)
		#变量
		self.m地址管理 = a地址管理
		self.mi修改 = False
		self.m经度有效 = True
		self.m纬度有效 = True
		self.m偏移有效 = True
		self.m选择有效 = False
		#表格
		c表格行 = 0
		self.w地址列表 = ttk.Treeview(self, show = "headings", columns = ("名称", "经度", "纬度", "偏移"), height = 20)
		self.w地址列表.heading("名称", text = "名称")
		self.w地址列表.heading("经度", text = "经度")
		self.w地址列表.heading("纬度", text = "纬度")
		self.w地址列表.heading("偏移", text = "偏移")
		self.w地址列表.column("名称", width = int(150 * v系统缩放))
		self.w地址列表.column("经度", width = int(100 * v系统缩放))
		self.w地址列表.column("纬度", width = int(100 * v系统缩放))
		self.w地址列表.column("偏移", width = int(80 * v系统缩放))
		self.w地址列表.bind("<<TreeviewSelect>>", self.f事件_表格选择)
		self.w地址列表.grid(row = c表格行, rowspan = 1, column = 0, columnspan = 6, padx = c间距, pady = c间距)
		self.f刷新地址列表()
		#移动按钮
		c移动按钮行 = c表格行 + 1
		self.w上移 = ttk.Button(self, text = "上移", command = self.f按钮_上移)
		self.w上移.grid(row = c移动按钮行, rowspan = 1, column = 0, columnspan = 3, padx = c间距, pady = c间距)
		self.w下移 = ttk.Button(self, text = "下移", command = self.f按钮_下移)
		self.w下移.grid(row = c移动按钮行, rowspan = 1, column = 3, columnspan = 3, padx = c间距, pady = c间距)
		#修改名称
		c名称行 = c移动按钮行 + 1
		self.w名称标签 = ttk.Label(self, text = "名称：")
		self.w名称标签.grid(row = c名称行, rowspan = 1, column = 0, columnspan = 1, padx = c间距, pady = c间距, sticky = "E")
		self.m绑定名称 = tk.StringVar(value = c默认名称)
		self.w名称 = ttk.Entry(self, textvariable = self.m绑定名称, width = 40)
		self.w名称.grid(row = c名称行, rowspan = 1, column = 1, columnspan = 5, padx = c间距, pady = c间距, sticky = "EW")
		#修改经纬度
		c数值行 = c名称行 + 1
		self.w经度标签 = ttk.Label(self, text = "经度：")
		self.w经度标签.grid(row = c数值行, rowspan = 1, column = 0, columnspan = 1, padx = c间距, pady = c间距, sticky = "E")
		self.m绑定经度 = tk.StringVar(value = "0")
		self.w经度 = ttk.Entry(self, textvariable = self.m绑定经度, width = 20, validate = "key", validatecommand = (self.register(self.f事件_输入经度), "%P"))
		self.w经度.grid(row = c数值行, rowspan = 1, column = 1, columnspan = 2, padx = c间距, pady = c间距, sticky = "EW")
		self.w纬度标签 = ttk.Label(self, text = "纬度：")
		self.w纬度标签.grid(row = c数值行+1, rowspan = 1, column = 0, columnspan = 1, padx = c间距, pady = c间距, sticky = "E")
		self.m绑定纬度 = tk.StringVar(value = "0")
		self.w纬度 = ttk.Entry(self, textvariable = self.m绑定纬度, width = 20, validate = "key", validatecommand = (self.register(self.f事件_输入纬度), "%P"))
		self.w纬度.grid(row = c数值行+1, rowspan = 1, column = 1, columnspan = 2, padx = c间距, pady = c间距, sticky = "EW")
		#修改偏移
		self.m绑定偏移 = tk.StringVar(value = "0")
		self.w偏移标签 = ttk.Label(self, text = "随机偏移：")
		self.w偏移标签.grid(row = c数值行, rowspan = 1, column = 3, columnspan = 1, padx = c间距, pady = c间距, sticky = "E")
		self.w偏移 = ttk.Entry(self, textvariable = self.m绑定偏移, width = 20, validate = "key", validatecommand = (self.register(self.f事件_输入偏移), "%P"))
		self.w偏移.grid(row = c数值行, rowspan = 1, column = 4, columnspan = 1, padx = c间距, pady = c间距, sticky = "EW")
		self.w偏移标签2 = ttk.Label(self, text = "米")
		self.w偏移标签2.grid(row = c数值行, rowspan = 1, column = 5, columnspan = 1, padx = c间距, pady = c间距, sticky = "W")
		#操作按钮
		c操作行 = c数值行 + 2
		self.w新增地址 = ttk.Button(self, text = "新增地址", command = self.f按钮_新增地址)
		self.w新增地址.grid(row = c操作行, rowspan = 1, column = 0, columnspan = 2, padx = c间距, pady = c间距)
		self.w修改地址 = ttk.Button(self, text = "修改地址", command = self.f按钮_修改地址)
		self.w修改地址.grid(row = c操作行, rowspan = 1, column = 2, columnspan = 2, padx = c间距, pady = c间距)
		self.w删除地址 = ttk.Button(self, text = "删除地址", command = self.f按钮_删除地址)
		self.w删除地址.grid(row = c操作行, rowspan = 1, column = 4, columnspan = 2, padx = c间距, pady = c间距)
		#确定&取消
		c分割线 = c操作行 + 1
		c确定取消行 = c分割线 + 1
		self.w分割线 = ttk.Separator(self)
		self.w分割线.grid(row = c分割线, rowspan = 1, column = 0, columnspan = 6, padx = c间距, pady = c间距, sticky = "EW")
		self.w确定 = ttk.Button(self, text = "保存修改并关闭窗口", command = self.f按钮_确定)
		self.w确定.grid(row = c确定取消行, rowspan = 1, column = 0, columnspan = 3, padx = c间距, pady = c间距)
		self.w取消 = ttk.Button(self, text = "取消修改并关闭窗口", command = self.f按钮_取消)
		self.w取消.grid(row = c确定取消行, rowspan = 1, column = 3, columnspan = 3, padx = c间距, pady = c间距)
		#其他
		self.bind("<Visibility>", self.f事件_加载)
	def f事件_加载(self, e):
		if e.widget == self:
			self.unbind("<Visibility>")
			窗口.f窗口居中(self)
			self.f更新修改按钮状态()
			self.f更新选择相关按钮状态()
	def f刷新地址列表(self):
		if v项列表 := self.w地址列表.get_children():
			self.w地址列表.delete(*v项列表)
		for v地址 in self.m地址管理:
			self.w地址列表.insert("", "end", values = v地址.ft元组())
	def f地址列表项取值(self, a项: str):
		return self.w地址列表.item(a项, "values")
	def f地址列表项赋值(self, a项: str, a值: tuple):
		self.w地址列表.set(a项, 0, a值[0])
		self.w地址列表.set(a项, 1, a值[1])
		self.w地址列表.set(a项, 2, a值[2])
		self.w地址列表.set(a项, 3, a值[3])
	def f交换地址(self, a项1, a项2):
		v值1 = self.f地址列表项取值(a项1)
		v值2 = self.f地址列表项取值(a项2)
		self.f地址列表项赋值(a项1, v值2)
		self.f地址列表项赋值(a项2, v值1)
	def f按钮_上移(self):
		if va选择项 := self.w地址列表.selection():
			v选择项 = va选择项[0]
		else:	#没有选择,不移动
			return
		v项列表 = self.w地址列表.get_children()
		v项位置 = v项列表.index(v选择项)
		if v项位置 == 0:	#已经在顶部,不移动
			return
		v交换项 = v项列表[v项位置-1]
		self.f交换地址(v选择项, v交换项)
		self.w地址列表.selection_set(v交换项)
		self.mi修改 = True
	def f按钮_下移(self):
		if va选择项 := self.w地址列表.selection():
			v选择项 = va选择项[0]
		else:	#没有选择,不移动
			return
		v项列表 = self.w地址列表.get_children()
		v项位置 = v项列表.index(v选择项)
		if v项位置 == len(v项列表)-1:	#已经在底部,不移动
			return
		v交换项 = v项列表[v项位置+1]
		self.f交换地址(v选择项, v交换项)
		self.w地址列表.selection_set(v交换项)
		self.mi修改 = True
	def f按钮_新增地址(self):
		v名称 = f取字符串变量(self.m绑定名称, "0")
		v经度 = f取字符串变量(self.m绑定经度, "0")
		v纬度 = f取字符串变量(self.m绑定纬度, "0")
		v偏移 = f取字符串变量(self.m绑定偏移, "0")
		self.w地址列表.insert("", "end", values = (v名称, v经度, v纬度, v偏移))
		self.mi修改 = True
	def f按钮_修改地址(self):
		v选择项 = self.w地址列表.selection()[0]
		self.f地址列表项赋值(v选择项, (self.m绑定名称.get(), self.m绑定经度.get(), self.m绑定纬度.get(), self.m绑定偏移.get()))
		self.mi修改 = True
	def f按钮_删除地址(self):
		v选择项 = self.w地址列表.selection()[0]
		self.w地址列表.delete(v选择项)	#会触发 <<TreeviewSelect>> 调用 f事件_表格选择
		self.mi修改 = True
	def f按钮_确定(self):
		if self.mi修改:
			self.m地址管理.f替换(self.w地址列表.item(v, "values") for v in self.w地址列表.get_children())
			self.m地址管理.f保存文件()
			self.master.f刷新地址()
		self.mi修改 = False
		self.destroy()
	def f按钮_取消(self):
		self.destroy()
	def f事件_表格选择(self, event):
		w表格 = event.widget
		va选择项 = w表格.selection()
		self.m选择有效 = bool(va选择项)
		self.f更新修改按钮状态()
		self.f更新选择相关按钮状态()
		if not self.m选择有效:	#没有选择,出现于删除行时
			return
		v名称, v经度, v纬度, v偏移 = w表格.item(va选择项[0], "values")
		self.m绑定名称.set(v名称)
		self.m绑定经度.set(v经度)
		self.m绑定纬度.set(v纬度)
		self.m绑定偏移.set(v偏移)
	def f事件_输入经度(self, a值):	#验证经度并设置按钮状态
		self.m经度有效 = f验证经度(a值)
		self.w经度.state(["!invalid" if self.m经度有效 else "invalid"])
		self.f更新新增按钮状态()
		self.f更新修改按钮状态()
		return True
	def f事件_输入纬度(self, a值):	#验证经度并设置按钮状态
		self.m纬度有效 = f验证纬度(a值)
		self.w纬度.state(["!invalid" if self.m纬度有效 else "invalid"])
		self.f更新新增按钮状态()
		self.f更新修改按钮状态()
		return True
	def f事件_输入偏移(self, a值):	#验证经度并设置按钮状态
		self.m偏移有效 = f验证偏移(a值)
		self.w偏移.state(["!invalid" if self.m偏移有效 else "invalid"])
		self.f更新新增按钮状态()
		self.f更新修改按钮状态()
		return True
	def f更新新增按钮状态(self):
		v启用 = self.m经度有效 and self.m纬度有效 and self.m偏移有效
		v状态 = ["!disabled" if v启用 else "disabled"]
		self.w新增地址.state(v状态)
	def f更新修改按钮状态(self):
		v启用 = self.m经度有效 and self.m纬度有效 and self.m偏移有效 and self.m选择有效
		v状态 = ["!disabled" if v启用 else "disabled"]
		self.w修改地址.state(v状态)
	def f更新选择相关按钮状态(self):
		v启用 = self.m选择有效
		v状态 = ["!disabled" if v启用 else "disabled"]
		self.w上移.state(v状态)
		self.w下移.state(v状态)
		self.w删除地址.state(v状态)