import random

from core.MsgTool import MsgTool as MT
from core.Plugin import Plugin

"""
在下面加入你自定义的插件，自动加载本文件所有的 Plugin 的子类
只需要写一个 Plugin 的子类，重写 match() 和 handle()
match() 返回 True 则自动回调 handle()
"""

class TestPlugin(Plugin):
    def match(self):  # 说 随机图片 则回复
        return self.on_full_match("随机图片")

    def handle(self):
        url = "https://iw233.cn/api/Random.php?" + str(random.random())
        self.send_msg(MT.at(self.context["user_id"]), MT.image(url))
