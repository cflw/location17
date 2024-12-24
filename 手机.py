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
	#ios17.x定位恢复时间较短,需要不断修改定位
	try:
		with DvtSecureSocketProxyService(a客户端) as dvt:
			LocationSimulation(dvt).set(latitude = a纬度, longitude = a经度)
		return True
	except pymd3ex.PasswordRequiredError as e:
		日志.f错误("有密码保护,请先解锁手机")
	except Exception as e:
		日志.f错误(f"出现异常: {e.__class__.__name__}: {e}", exc_info = False)	#前端只显示异常名称
		日志.f调试("异常信息:", exc_info = e)
	return False
def f还原定位0(a客户端):
	#代码参考 pymobiledevice3.cli.developer.dvt_simulate_location_clear
	#有延迟,可能没那么快生效
	try:
		with DvtSecureSocketProxyService(a客户端) as dvt:
			LocationSimulation(dvt).clear()
		return True
	except Exception as e:
		日志.f错误(f"出现异常: {e.__class__.__name__}: {e}", exc_info = False)	#前端只显示异常名称
		日志.f调试("异常信息:", exc_info = e)
	return False
class C手机:
	def __init__(self, a隧道服务, a序列号, a连接类型):
		self.m隧道服务 = a隧道服务
		self.m客户端 = create_using_usbmux(serial = a序列号, connection_type = a连接类型)
		self.m持续修改定位 = None
	def fg显示名称(self):	#在主界面手机列表中显示的名称
		return f"{self.fg设备名称()} ({self.fg系统版本()})"
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
		if rsd := self.fg远程服务():
			async with rsd:
				return f修改定位0(rsd, a经度, a纬度)
		return False
	async def f还原定位(self):
		#ios 17.0~ 使用远程服务
		if rsd := self.fg远程服务():
			async with rsd:
				return f还原定位0(rsd)
		return False
	async def f持续修改定位(self, a经度: float, a纬度: float):
		if self.m持续修改定位:
			self.m持续修改定位.f关闭()
		if rsd := self.fg远程服务():
			async with rsd:
				self.m持续修改定位 = C持续修改定位(rsd, a经度, a纬度)
				return self.m持续修改定位.f启动()
		return False
	async def f持续还原定位(self):
		if self.m持续修改定位:
			v还原结果 = self.m持续修改定位.f关闭()
			self.m持续修改定位 = None
			return v还原结果
		else:	#没有持续修改定位,则还原一次
			return await self.f还原定位()
	def fg远程服务(self):
		if v地址端口 := self.m隧道服务.fg远程服务地址(self.fg序列号()):
			日志.f调试(f"连接远程服务: {v地址端口}")
			return RemoteServiceDiscoveryService(v地址端口)
		else:
			日志.f告警("未发现设备,无法连接远程服务")
			return None
class C手机管理:
	def __init__(self):
		self.ma手机 = []
		self.m上次列出设备数 = 0	#刷新手机时用
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
		self.m隧道服务.f关闭()
		await asyncio.sleep(0)
	def f刷新手机(self):
		va设备 = list_devices()
		v这次列出设备数 = len(va设备)
		if self.m上次列出设备数 == v这次列出设备数:
			return False	#数量一样,说明没变化
		self.m上次列出设备数 = v这次列出设备数
		va已有 = list(v手机.fg序列号() for v手机 in self.ma手机)	#缓存,只记序列号
		va保留 = set()
		va待添加 = dict()	#序列号: 连接类型
		for v设备 in va设备:
			if v设备.serial in va已有:
				va保留.add(v设备.serial)
			else:
				va待添加.setdefault(v设备.serial, v设备.connection_type)
		va新手机 = list(filter(lambda a手机: a手机.fg序列号() in va保留, self.ma手机))
		va新手机 += list(map(lambda a设备: C手机(self.m隧道服务, a设备[0], a设备[1]), va待添加.items()))
		self.ma手机 = va新手机
		return True
	def fe手机名称(self):
		for v手机 in self.ma手机:
			yield v手机.fg显示名称()
	def fi有手机(self):
		return bool(self.ma手机)
	def fg手机数量(self):
		return len(self.ma手机)
class C隧道服务:	#隧道服务必须在另外一个线程运行,不然连接时阻塞会导致连接超时
	def __init__(self):
		self.m隧道核心 = TunneldCore()
		self.m启动标志 = False
		self.m关闭标志 = False
		self.m线程 = threading.Thread(target = asyncio.run, args = (self.f运行(),))
		self.m抛过的异常 = set()	#重复的异常只记录一次日志
	async def f运行(self):
		while not self.m关闭标志:
			if self.m启动标志:
				日志.f信息("启动隧道服务")
				self.m隧道核心.start()
				self.m启动标志 = False
				#隧道任务可能因异常而中断,需要重新启动
				await self.f守护()
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
	async def f守护(self):
		for v任务 in self.m隧道核心.tasks:
			if v任务.get_name() == "monitor-usbmux-task" and v任务.done():
				if v异常 := v任务.exception():
					if v异常 not in self.m抛过的异常:
						if type(v异常) == pymd3ex.PasswordRequiredError:
							日志.f告警("有密码保护,请先解锁手机")
						else:
							日志.f告警(v异常)
						self.m抛过的异常.add(v异常)
					v任务 = asyncio.create_task(self.m隧道核心.monitor_usbmux_task(), name='monitor-usbmux-task')
					await asyncio.sleep(1)
					return
	def fg远程服务地址(self, a序列号: str):
		for k, v in self.m隧道核心.tunnel_tasks.items():
			if a序列号 in k:
				return v.tunnel.address, v.tunnel.port
class C持续修改定位:	#解决ios17修改定位秒恢复的问题,通过一个无限循环来不断修改定位
	def __init__(self, a客户端, a经度: float, a纬度: float):
		self.m关闭标志 = False
		self.m客户端 = a客户端	#rsd
		self.m经度 = a经度
		self.m纬度 = a纬度
		self.m线程 = threading.Thread(target = asyncio.run, args = (self.f运行(),))
		self.m还原结果 = None	#线程返回值
	async def f运行(self):
		while not self.m关闭标志:
			if not f修改定位0(self.m客户端, self.m经度, self.m纬度):
				return False	#出现异常,提前结束
			await asyncio.sleep(0.1)
		#正常结束,还原定位
		self.m还原结果 = f还原定位0(self.m客户端)
	def f启动(self):
		v结果 = f修改定位0(self.m客户端, self.m经度, self.m纬度)	#首次修改,根据结果决定是否持续修改
		if v结果:
			self.m线程.start()
		return v结果
	def f关闭(self):
		if self.m线程.is_alive():	#可能存在线程异常结束的情况
			self.m关闭标志 = True
			self.m线程.join()
			return self.m还原结果
		return False