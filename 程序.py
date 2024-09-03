import asyncio
import async_tkinter_loop	#async-tkinter-loop
import 主窗口
import 地址管理
import 手机
async def main():
	v地址管理 = 地址管理.C地址管理()
	v手机管理 = 手机.C手机管理()
	await v手机管理.f初始化()
	w主窗口 = 主窗口.W主窗口(v地址管理, v手机管理)
	await async_tkinter_loop.main_loop(w主窗口)
	await v手机管理.f关闭()
if __name__ == "__main__":
	asyncio.run(main())