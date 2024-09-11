import math
import random
r = 6371000	#地球半径
c = 40030173	#地球周长
m = 8.9932161921958218866553487040888e-6	#一米多少度(纬度=0 时)
def f纬度偏移(a纬度: float, a距离: float):
	return a纬度 + a距离 * m
def f经度偏移(a经度: float, a纬度: float, a距离: float):
	return a经度 + a距离 * m / math.cos(a纬度 / 180 * math.pi)
def f随机偏移(a经度: float, a纬度: float, a距离: float):
	v方向 = random.random() * 2 * math.pi
	v长度 = random.random() * a距离
	x = math.cos(v方向) * v长度
	y = math.sin(v方向) * v长度
	v纬度 = f纬度偏移(a纬度, y)
	v经度 = f经度偏移(a经度, a纬度, x)
	return v经度, v纬度