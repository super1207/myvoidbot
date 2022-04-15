import os
import json
import uuid
from urllib import request

from core.MsgTool import MsgTool as MT
from core.Plugin import Plugin

"""
在下面加入你自定义的插件，自动加载本文件所有的 Plugin 的子类
只需要写一个 Plugin 的子类，重写 match() 和 handle()
match() 返回 True 则自动回调 handle()
"""

def get_txt_info(fname):
    current_dir = os.path.dirname(__file__)
    info_dir = os.path.join(current_dir,fname)
    with open(info_dir,"r") as f:
        info = f.read()
    info_map = {}
    infovec = info.split('\n')
    for its in infovec:
        it = its.split('\t')
        info_map[it[0]] = it[1]
    return info_map

cpp_info = get_txt_info("devhelp-index-cpp.txt")
c_info = get_txt_info("devhelp-index-c.txt")

class TestPlugin(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        cont = MT.get_text_from_msg(self.context["message"])
        if cont.startswith("#cpp") or cont.startswith("#c"):
            self.my_cont = cont
            return True
        else:
            return False

    def handle(self):
        url = "https://zh.cppreference.com/w/"
        if self.my_cont.startswith("#cpp"):
            url += cpp_info[''.join(self.my_cont.split(" ")[1:])]
        else:
            url += c_info[''.join(self.my_cont.split(" ")[1:])]
        self.send_msg(MT.at(self.context["user_id"]), MT.text(url))

