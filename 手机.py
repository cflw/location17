import asyncio
import traceback
import threading
import pymobiledevice3.exceptions as pymd3ex
from pymobiledevice3.usbmux import list_devices	#pymobiledevice3=4.11.3
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.osu.os_utils import get_os_utils
from pymobiledevice3.services.dvt.dvt_secure_socket_proxy import DvtSecureSocketProxyService
from pymobiledevice3.services.dvt.instruments.location_simulation import LocationSimulation
from pymobiledevice3.tunneld import TunneldCore
from pymobiledevice3.remote.remote_service_discovery import RemoteServiceDiscoveryService
import 日志
OSUTILS = get_os_utils()
def f修改定位0(a客户端, a经度: float, a纬度: float):	#通用
	#代码参考 pymobiledevice3.cli.developer.dvt_simulate_location_set
	try:
		dvt = DvtSecureSocketProxyService(a客户端)
		dvt.perform_handshake()
		LocationSimulation(dvt).set(latitude = a纬度, longitude = a经度)
		dvt.close()
		return True
	except pymd3ex.PasswordRequiredError as e:
		日志.f错误("有密码保护,请先解锁手机")
	except Exception as e:
		日志.f错误("出现异常", exc_info = e)
	return False
def f还原定位0(a客户端):
	#代码参考 pymobiledevice3.cli.developer.dvt_simulate_location_clear
	#有延迟,可能没那么快生效
	try:
		dvt = DvtSecureSocketProxyService(a客户端)
		dvt.perform_handshake()
		LocationSimulation(dvt).clear()
		dvt.close()
		return True
	except Exception as e:
		日志.f错误("出现异常", exc_info = e)
	return False
class C手机:
	def __init__(self, a隧道服务, a序列号, a连接类型):
		self.m隧道服务 = a隧道服务
		self.m客户端 = create_using_usbmux(serial = a序列号, connection_type = a连接类型)
		self.m远程服务 = None
	def fg显示名称(self):	#在主界面手机列表中显示的名称
		return f"{self.fg设备名称()}({self.fg系统版本()})"
	def fg设备名称(self):
		return self.m客户端.all_values.get("DeviceName")
	def fg连接类型(self):
		return self.m客户端.service.mux_device.connection_type
	def fg系统版本(self):
		return self.m客户端.all_values.get("ProductVersion")
	def fg序列号(self):
		return self.m客户端.udid
	async def f修改定位(self, a经度: float, a纬度: float):
		#ios 17.0~ 使用远程服务
		if await self.f连接远程服务():
			return f修改定位0(self.m远程服务, a经度, a纬度)
		else:
			return False
	async def f还原定位(self):
		#ios 17.0~ 使用远程服务
		if await self.f连接远程服务():
			return f还原定位0(self.m远程服务)
		else:
			return False
	async def f连接远程服务(self):
		if not self.m远程服务:
			if v地址端口 := self.m隧道服务.fg远程服务地址(self.fg序列号()):
				self.m远程服务 = RemoteServiceDiscoveryService(v地址端口)
			else:
				日志.f告警("未发现设备,无法连接远程服务")
				return False
			try:
				日志.f调试(f"连接远程服务: {v地址端口}")
				await self.m远程服务.connect()
				return True
			except Exception as e:
				日志.f错误(f"连接远程服务出现异常: {e}")
				traceback.print_exc()
				self.m远程服务 = None
				return False
		return True
	async def f关闭远程服务(self):
		if self.m远程服务:
			日志.f调试(f"关闭远程服务: {self.m远程服务.service.address}")
			await self.m远程服务.close()
class C手机管理:
	def __init__(self):
		self.ma手机 = []
		self.m隧道服务 = C隧道服务()
	def __getitem__(self, k):
		return self.ma手机[k]
	def __iter__(self):
		return self.ma手机.__iter__()
	async def f初始化(self):
		if not OSUTILS.is_admin:
			日志.f错误("必须使用管理员权限启动程序")
			return
		self.m隧道服务.f启动()
		await asyncio.sleep(0)
	async def f关闭(self):
		for v手机 in self.ma手机:
			await v手机.f关闭远程服务()
		self.m隧道服务.f关闭()
	def fe手机(self):
		日志.f调试("遍历手机")
		va设备 = list_devices()
		for v设备 in va设备:
			if v设备.connection_type != "USB":	#只要usb,不要network
				continue
			yield C手机(self.m隧道服务, v设备.serial, v设备.connection_type)
	def f刷新列表(self):
		self.ma手机 = list(self.fe手机())
	def fe显示名称(self):
		for v手机 in self.ma手机:
			yield v手机.fg显示名称()
	def fi有手机(self):
		return bool(self.ma手机)
class C隧道服务:	#隧道服务必须在另外一个线程运行,不然连接时阻塞会导致连接超时
	def __init__(self):
		self.m隧道核心 = TunneldCore()
		self.m启动标志 = False
		self.m关闭标志 = False
		self.m线程 = threading.Thread(target = asyncio.run, args = (self.f运行(),))
	async def f运行(self):
		while not self.m关闭标志:
			if self.m启动标志:
				日志.f信息("启动隧道服务")
				self.m隧道核心.start()
				self.m启动标志 = False
			await asyncio.sleep(0.01)
		日志.f信息("关闭隧道服务")
		await self.m隧道核心.close()
	def f启动(self):
		self.m启动标志 = True
		self.m线程.start()
	def f关闭(self):
		self.m关闭标志 = True
		if self.m线程.is_alive():	#可能存在线程未启动的情况
			self.m线程.join()
	def fg远程服务地址(self, a序列号: str):
		for k, v in self.m隧道核心.tunnel_tasks.items():
			if a序列号 in k:
				return v.tunnel.address, v.tunnel.port