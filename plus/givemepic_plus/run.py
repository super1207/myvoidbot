import re
import random
from urllib import request
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
        return self.on_reg_match("^#来点.*的图片$")

    def handle(self):
        cont = MT.get_text_from_msg(self.context["message"])
        pt = re.compile("^#来点(.*)的图片$")
        key_word = pt.findall(cont)[0]
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        url = "https://image.baidu.com/search/index?tn=baiduimage&" + parse.urlencode({"word":key_word})
        req = request.Request(url,headers=headers)
        res = request.urlopen(req).read().decode()
        pt2 = re.compile("\"objURL\" {0,1}: {0,1}\"(.*?)\"")
        url_arr = pt2.findall(res)
        send_url = url_arr[random.randint(0,len(url_arr) - 1)]
        self.send_msg(
            MT.at(self.context["user_id"]), 
            MT.text("喵喵喵~{}的涩涩来啦!".format(key_word)),
            MT.image(send_url)
        )