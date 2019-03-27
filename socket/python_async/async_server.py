#!/usr/bin/env python3
# 异步编程, 单进程单线程模式下实现并发  实际测试: 在post请求await time.sleep()  模拟两个请求发送, 并不能同时处理, 还是得等第一个sleep
# 结束后才服务第二个请求
from aiohttp import web
import asyncio
import logging
import uvloop
import time,datetime


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
routes = web.RouteTableDef()


@routes.get('/')
async def hello(request):

    return web.Response(text="Hello, world")


@routes.post('/app')
async def app(request):   # 异步监听，只要一有握手就开始触发
    try:
        print(time.time())
        data = await request.post()   # 等待数据接受完
        print(time.time())
        print(dir(data))
        await time.sleep(20)
    except Exception as e:
        print(e)
        pass

    return web.json_response({"code":1})


if __name__ == '__main__':
    logging.info('server start：%s'% datetime.datetime.now())
    app = web.Application()    # 创建app，设置最大接收图片大小为2M
    app.add_routes(routes)     # 添加路由映射

    web.run_app(app,host='0.0.0.0',port=30303)   # 启动app
    logging.info('server close：%s'% datetime.datetime.now())




