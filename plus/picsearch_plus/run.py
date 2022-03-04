from urllib import parse

from core.MsgTool import MsgTool as MT
from core.Plugin import Plugin

"""
在下面加入你自定义的插件，自动加载本文件所有的 Plugin 的子类
只需要写一个 Plugin 的子类，重写 match() 和 handle()
match() 返回 True 则自动回调 handle()
"""

class TestPlugin(Plugin):
    def match(self):  # 说 今日新闻 则回复
        cont  = ""
        if self.context["post_type"] == "message":
            cont = MT.get_text_from_msg(self.context["message"]).strip()
        return cont == "#搜图"

    def handle(self):
        pic_url = MT.get_pic_from_msg(self.context["message"])
        url = "https://yandex.com/images/search?family=yes&rpt=imageview&" + parse.urlencode({"url":pic_url})
        self.send_msg(
            MT.at(self.context["user_id"]), 
            MT.text("搜索结果:(自己在浏览器中打开)\n{}".format(url))
        )