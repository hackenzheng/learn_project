
import aiohttp
import asyncio
import logging
import uvloop
import socket
import time,datetime
from aiohttp.web import middleware

from aiohttp import web
from util.prometheus_util import Promethus
from util.config import *
import prometheus_client
from prometheus_client import Counter,Gauge
from prometheus_client.core import CollectorRegistry
from prometheus_client import CollectorRegistry, Gauge


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()  # 获取全局轮训器


hostName = socket.gethostname()
routes = web.RouteTableDef()
promethus=Promethus()


@middleware
async def check_project(request, handler):
    return await handler(request)

# 推送数据
@routes.post('/metrics')
async def post_data(request):
    try:
        data = await request.json()
    except Exception as e:
        logging.error("image file too large or cannot convert to json")
        return web.json_response(write_response(1,"image file too large or cannot convert to json",{}))

    logging.info('receive metrics data %s' % datetime.datetime.now())
    status = await promethus.label_data(data['metrics'])     # 包含记录信息，处理图片，存储图片，token过期以后要请求license服务器

    logging.info('save metrics data finish %s, %s' % (datetime.datetime.now(),str(status)))
    header = {"Access-Control-Allow-Origin": "*", 'Access-Control-Allow-Methods': 'GET,POST'}
    if status:
        return web.json_response(write_response(0,"success",{}),headers=header)
    else:
        return web.json_response(write_response(1, "error", {}), headers=header)



# 读取数据
@routes.get('/')
async def default(request):
    data = await promethus.get_metrics_prometheus(onlyread=True)
    return web.Response(body=data, content_type="text/plain")  # 将计数器的值返回

@routes.get('/metrics')
async def get_data(request):
    data = await promethus.get_metrics_prometheus()
    return web.Response(body=data, content_type="text/plain")  # 将计数器的值返回


if __name__ == '__main__':

    # init_logger(module_name="face_det")   # 初始化日志配置
    init_console_logger()

    app = web.Application(client_max_size=int(LOCAL_SERVER_SIZE)*1024**2,middlewares=[check_project])    # 创建app，设置最大接收图片大小为2M
    app.add_routes(routes)     # 添加路由映射

    logging.info('server start,port is %s, datetime is %s'%(str(LOCAL_SERVER_PORT),str(datetime.datetime.now())))
    web.run_app(app,host=LOCAL_SERVER_IP,port=LOCAL_SERVER_PORT)   # 启动app
    logging.info('server close：%s'% datetime.datetime.now())



