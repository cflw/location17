import logging
#全局
c日志格式 = "[%(asctime)s][%(levelname)s]%(message)s"
c时间格式 = "%H:%M:%S"
c格式化器 = logging.Formatter(c日志格式, datefmt = c时间格式)
c流处理器 = logging.StreamHandler()
c流处理器.setFormatter(c格式化器)
#其他模块日志
v隧道日志 = logging.getLogger("pymobiledevice3.tunneld")
v隧道日志.setLevel(logging.DEBUG)
v隧道日志.addHandler(c流处理器)
#本程序日志
g日志 = logging.getLogger("location17")
g日志.setLevel(logging.DEBUG)
g日志.addHandler(c流处理器)
f调试 = g日志.debug
f信息 = g日志.info
f告警 = g日志.warning
f错误 = g日志.error
class C文本框处理器(logging.Handler):
	def __init__(self):
		logging.Handler.__init__(self)
		self.w文本框 = None
		self.m缓冲 = ""
		self.m状态 = False
	def emit(self, record):
		self.m缓冲 += self.format(record) + "\r\n"
	def f更新(self):
		if self.m状态 and self.m缓冲:
			self.w文本框.insert("end", self.m缓冲)
			self.m缓冲 = ""
	def f启用(self, a文本框):
		self.w文本框 = a文本框
		self.m状态 = True
	def f关闭(self):
		self.m状态 = False
g文本框处理器 = C文本框处理器()
g文本框处理器.setFormatter(c格式化器)
g文本框处理器.setLevel(logging.INFO)
g日志.addHandler(g文本框处理器)
v隧道日志.addHandler(g文本框处理器)