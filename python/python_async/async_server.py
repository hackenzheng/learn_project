#!/usr/bin/env python3

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
async def app(request):   #request只是个变量名
    try:
        print(time.time())
        data = await request.post()   # 这种方式是表单数据
        print(time.time())
        print(data)

        """
        # contenttype/application.json类型的处理
        data = await request.json()
        print(data.items())
        print(data.values())
        print(data.keys())
        """

    except Exception as e:
        print(e)
        pass

    return web.json_response({"code":1})


if __name__ == '__main__':
    logging.info('server start：%s'% datetime.datetime.now())
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app,host='0.0.0.0',port=30303)





