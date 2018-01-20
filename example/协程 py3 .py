#coding:utf-8
#第一种用法
##import asyncio
##@asyncio.coroutine
##def test(i):
##	print("test_1",i)
##	r=yield from asyncio.sleep(1)
##	print("test_2",i)
##	
##loop=asyncio.get_event_loop()
##tasks=[test(i) for i in range(5)]
##loop.run_until_complete(asyncio.wait(tasks))
##loop.close()

#第二种用法
import asyncio,time
async def test(i):
	print("test_1",i)
	await asyncio.sleep(1)
	print("test_2",i)
loop=asyncio.get_event_loop()
tasks=[test(i) for i in range(3)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
