import os
import sys
import glob
import time
import queue
import logging
import threading
import traceback
import collections
import json as json_
import importlib.util

from core.MsgTool import MsgTool
from core.Plugin import Plugin

import websocket


WS_URL = "ws://127.0.0.1:6700?access_token=77156"   # WebSocket 地址
NICKNAME = ["BOT", "ROBOT"]         # 机器人昵称
SUPER_USER = [12345678, 23456789]   # 主人的 QQ 号
# 日志设置  level=logging.DEBUG -> 日志级别为 DEBUG
logging.basicConfig(level=logging.DEBUG, format="[void] %(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def plugin_pool(context: dict):
    # 遍历所有的 Plugin 的子类，执行匹配
    for P in Plugin.__subclasses__():
        try:
            plugin = P(context,echo,WS_APP,NICKNAME,SUPER_USER,logger)
            if plugin.match():
                plugin.handle()
        except:
            logger.error("模块抛出异常 -> " + traceback.format_exc())
            
class Echo:
    def __init__(self):
        self.echo_num = 0
        self.echo_list = collections.deque(maxlen=20)

    def get(self):
        self.echo_num += 1
        q = queue.Queue(maxsize=1)
        self.echo_list.append((self.echo_num, q))
        return self.echo_num, q

    def match(self, context: dict):
        for obj in self.echo_list:
            if context["echo"] == obj[0]:
                obj[1].put(context)

def deal_arr_msg():
    pass

def on_message(_, message):
    # https://github.com/botuniverse/onebot-11/blob/master/event/README.md
    context = json_.loads(message)
    if "echo" in context:
        logger.debug("调用返回 -> " + message)
        # 响应报文通过队列传递给调用 API 的函数
        echo.match(context)
    elif "meta_event_type" in context:
        logger.debug("心跳事件 -> " + message)
    else:
        logger.info("收到事件 -> " + message)
        # 将消息事件中的array格式的message转化为string格式
        if context["post_type"] == "message" and isinstance(context["message"],list):
            context["message"] = MsgTool.arr_msg_to_str(context["message"])
        # 消息事件，开启线程
        t = threading.Thread(target=plugin_pool, args=(context, ))
        t.start()

def read_txt_to_list(fpath):
    with open(fpath,"r") as f:
        l = f.readlines()
    out_list = []
    for it in l:
        t = it.strip()
        if t != "":
            out_list.append(t)
    return out_list

def plus_is_enable(cfg_list,plus_name):
    if cfg_list == None:
        return True
    for it in cfg_list:
        t = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"plus",it,"run.py")
        if plus_name == t:
            return True
    return False


if __name__ == "__main__":

    # 载入Plus目录下的插件
    dirname = os.path.dirname(os.path.abspath(__file__))
    plus_dir = os.path.join(os.path.dirname(dirname),"plus")
    enable_plus_dir = os.path.join(plus_dir,"enable_plus.txt")
    enable_plus = None
    if os.path.isfile(enable_plus_dir):
        enable_plus = read_txt_to_list(enable_plus_dir)
    py_file_list = [py_file for py_file in glob.glob("{}{}plus{}*{}run.py".format(os.path.dirname(dirname),os.sep,os.sep,os.sep,os.sep))]
    for script_module_name in py_file_list:
        if not plus_is_enable(enable_plus,script_module_name):
            continue
        logger.info("加载插件 -> " + script_module_name)
        spec = importlib.util.spec_from_file_location(script_module_name, script_module_name)
        script_module = importlib.util.module_from_spec(spec)
        sys.modules[script_module_name] = script_module 
        spec.loader.exec_module(script_module)
        logger.info("加载插件 -> " + script_module_name + " 成功")

    echo = Echo()

    WS_APP = websocket.WebSocketApp(
        WS_URL,
        on_message=on_message,
        on_open=lambda _: logger.debug("连接成功......"),
        on_close=lambda _: logger.debug("重连中......"),
    )

    while True:  # 掉线重连
        WS_APP.run_forever()
        time.sleep(5)
