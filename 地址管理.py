import os.path
import xml.etree.ElementTree as et
c地址文件 = "地址.xml"
class S地址:
	def __init__(self, a名称: str, a经度: float, a纬度: float):
		self.m名称 = str(a名称)
		self.m经度 = float(a经度)
		self.m纬度 = float(a纬度)
	def ft元组(self):
		return self.m名称, self.m经度, self.m纬度
	@staticmethod
	def fc地址元素(a元素: et.Element):
		return S地址(a元素.get("名称"), a元素.find("经度").text, a元素.find("纬度").text)
	def ft地址元素(self):
		v地址元素 = et.Element("地址", {"名称": self.m名称})
		et.SubElement(v地址元素, "经度").text = str(self.m经度)
		et.SubElement(v地址元素, "纬度").text = str(self.m纬度)
		return v地址元素
class C地址管理:
	def __init__(self):
		self.ma地址 = []
	def __getitem__(self, k):
		return self.ma地址[k]
	def __iter__(self):
		return self.ma地址.__iter__()
	def f打开文件(self, a路径: str = c地址文件):
		if not os.path.exists(a路径):
			return False
		v树 = et.parse(a路径)
		v根 = v树.getroot()
		va地址 = []
		for v地址元素 in v根.findall("地址"):
			v地址 = S地址.fc地址元素(v地址元素)
			va地址.append(v地址)
		self.ma地址 = va地址
		return True
	def f保存文件(self, a路径: str = c地址文件):
		v根 = et.Element("地址组")
		i = 0
		for v地址 in self.ma地址:
			v地址元素 = v地址.ft地址元素()
			v地址元素.set("索引", str(i))
			v根.append(v地址元素)
			i += 1
		v树 = et.ElementTree(v根)
		v树.write(a路径, encoding = "utf-8")
	def fe地址名称(self):
		for v地址 in self.ma地址:
			yield v地址.m名称
	def fe地址元组(self):
		for v地址 in self.ma地址:
			yield v地址.ft元组()
	def f交换(self, a前: int, a后: int):
		self.ma地址[a前], self.ma地址[a后] = self.ma地址[a后], self.ma地址[a前]
	def f上移(self, a索引: int):
		self.f交换(a索引, a索引-1)
	def f下移(self, a索引: int):
		self.f交换(a索引, a索引+1)
	def f替换(self, aa地址):
		self.ma地址 = list(S地址(*v) for v in aa地址)
	def fi有地址(self):
		return bool(self.ma地址)
	def fg地址数量(self):
		return len(self.ma地址)