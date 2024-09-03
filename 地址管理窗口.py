import tkinter as tk
import tkinter.ttk as ttk
import 窗口
c默认名称 = "新地址"
c默认经度 = "0"
c默认纬度 = "0"
def f验证小数(a值: str):
	if a值:
		try:
			float(a值)
			return True
		except ValueError:
			return False
	return True	#可以空
def f取字符串变量(a变量: tk.StringVar, a默认值: str):
	v = a变量.get()
	return v if v else a默认值
class W地址管理(tk.Toplevel):
	def __init__(self, a父, a地址管理):
		tk.Toplevel.__init__(self, a父, width = 400)
		self.title("地址管理")
		窗口.f窗口居中(self, 412, 611)
		self.resizable(False, False)
		#变量
		self.m地址管理 = a地址管理
		self.mi修改 = False
		#表格
		c表格行 = 0
		self.w地址列表 = ttk.Treeview(self, show = "headings", columns = ("名称", "经度", "纬度"), height = 20)
		self.w地址列表.heading("名称", text = "名称")
		self.w地址列表.heading("经度", text = "经度")
		self.w地址列表.heading("纬度", text = "纬度")
		self.w地址列表.column("名称", width = 200)
		self.w地址列表.column("经度", width = 100)
		self.w地址列表.column("纬度", width = 100)
		self.w地址列表.bind("<<TreeviewSelect>>", self.f事件_表格选择)
		self.w地址列表.grid(row = c表格行, rowspan = 1, column = 0, columnspan = 6, padx = 4, pady = 4)
		self.f刷新地址列表()
		#移动按钮
		c移动按钮行 = c表格行 + 1
		self.w上移 = ttk.Button(self, text = "上移", command = self.f按钮_上移)
		self.w上移.grid(row = c移动按钮行, rowspan = 1, column = 0, columnspan = 3, padx = 4, pady = 4)
		self.w下移 = ttk.Button(self, text = "下移", command = self.f按钮_下移)
		self.w下移.grid(row = c移动按钮行, rowspan = 1, column = 3, columnspan = 3, padx = 4, pady = 4)
		#修改值
		c名称行 = c移动按钮行 + 1
		self.w名称标签 = ttk.Label(self, text = "名称：")
		self.w名称标签.grid(row = c名称行, rowspan = 1, column = 0, columnspan = 1, padx = 4, pady = 4, sticky = "E")
		self.m绑定名称 = tk.StringVar(value = c默认名称)
		self.w名称 = ttk.Entry(self, textvariable = self.m绑定名称, width = 40)
		self.w名称.grid(row = c名称行, rowspan = 1, column = 1, columnspan = 5, padx = 4, pady = 4, sticky = "EW")
		c数值行 = c名称行 + 1
		self.w经度标签 = ttk.Label(self, text = "经度：")
		self.w经度标签.grid(row = c数值行, rowspan = 1, column = 0, columnspan = 1, padx = 4, pady = 4, sticky = "E")
		self.m绑定经度 = tk.StringVar(value = c默认经度)
		self.w经度 = ttk.Entry(self, textvariable = self.m绑定经度, width = 20, validate = "key", validatecommand = (self.register(f验证小数), "%P"))
		self.w经度.grid(row = c数值行, rowspan = 1, column = 1, columnspan = 2, padx = 4, pady = 4, sticky = "EW")
		self.w纬度标签 = ttk.Label(self, text = "纬度：")
		self.w纬度标签.grid(row = c数值行, rowspan = 1, column = 3, columnspan = 1, padx = 4, pady = 4, sticky = "E")
		self.m绑定纬度 = tk.StringVar(value = c默认纬度)
		self.w纬度 = ttk.Entry(self, textvariable = self.m绑定纬度, width = 20, validate = "key", validatecommand = (self.register(f验证小数), "%P"))
		self.w纬度.grid(row = c数值行, rowspan = 1, column = 4, columnspan = 2, padx = 4, pady = 4, sticky = "EW")
		#操作按钮
		c操作行 = c数值行 + 1
		self.w新增地址 = ttk.Button(self, text = "新增地址", command = self.f按钮_新增地址)
		self.w新增地址.grid(row = c操作行, rowspan = 1, column = 0, columnspan = 2, padx = 4, pady = 4)
		self.w修改地址 = ttk.Button(self, text = "修改地址", command = self.f按钮_修改地址)
		self.w修改地址.grid(row = c操作行, rowspan = 1, column = 2, columnspan = 2, padx = 4, pady = 4)
		self.w删除地址 = ttk.Button(self, text = "删除地址", command = self.f按钮_删除地址)
		self.w删除地址.grid(row = c操作行, rowspan = 1, column = 4, columnspan = 2, padx = 4, pady = 4)
		#确定&取消
		c分割线 = c操作行 + 1
		c确定取消行 = c分割线 + 1
		self.w分割线 = ttk.Separator(self)
		self.w分割线.grid(row = c分割线, rowspan = 1, column = 0, columnspan = 6, padx = 4, pady = 4, sticky = "EW")
		self.w确定 = ttk.Button(self, text = "保存修改并关闭窗口", command = self.f按钮_确定)
		self.w确定.grid(row = c确定取消行, rowspan = 1, column = 0, columnspan = 3, padx = 4, pady = 4)
		self.w取消 = ttk.Button(self, text = "取消修改并关闭窗口", command = self.f按钮_取消)
		self.w取消.grid(row = c确定取消行, rowspan = 1, column = 3, columnspan = 3, padx = 4, pady = 4)
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
		v名称 = f取字符串变量(self.m绑定名称, c默认名称)
		v经度 = f取字符串变量(self.m绑定经度, c默认经度)
		v纬度 = f取字符串变量(self.m绑定纬度, c默认纬度)
		self.w地址列表.insert("", "end", values = (v名称, v经度, v纬度))
		self.mi修改 = True
	def f按钮_修改地址(self):
		v选择项 = self.w地址列表.selection()[0]
		self.f地址列表项赋值(v选择项, (self.m绑定名称.get(), self.m绑定经度.get(), self.m绑定纬度.get()))
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
		if not va选择项:	#没有选择,出现于删除行时
			return
		v名称, v经度, v纬度 = w表格.item(va选择项[0], "values")
		self.m绑定名称.set(v名称)
		self.m绑定经度.set(v经度)
		self.m绑定纬度.set(v纬度)