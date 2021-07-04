import asyncio
import logging
from aiohttp import web

# 设置日志级别
logging.basicConfig(level=logging.INFO)

# handler的request参数不能少
def index(request):
    return web.Response(body=b'<h1>Index</h1>',content_type="text/html",charset="utf-8")

async def init():
    # 定义路由信息
    app = web.Application()
    app.router.add_route('GET','/',index)
    # 等待runner启动
    runner = web.AppRunner(app)
    await runner.setup()
    # 启动服务器
    serv = web.TCPSite(runner, "127.0.0.1", 9000)
    await serv.start()
    logging.info("http://127.0.0.1:9000/")
    return serv

loop = asyncio.get_event_loop()
loop.run_until_complete(init())
loop.run_forever()