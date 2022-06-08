import re
import json
from urllib import parse
from urllib import request

from core.MsgTool import MsgTool as MT
from core.Plugin import Plugin

"""
在下面加入你自定义的插件，自动加载本文件所有的 Plugin 的子类
只需要写一个 Plugin 的子类，重写 match() 和 handle()
match() 返回 True 则自动回调 handle()
"""

class TestPlugin(Plugin):
    def match(self):
        cont  = ""
        if self.context["post_type"] == "message":
            cont = MT.get_text_from_msg(self.context["message"]).strip()
        if cont.startswith("#点歌"):
            self.my_cont = cont[len("#点歌"):]
            return True
        return False

    # 自定义音乐
    # def handle(self):
    #     url = "https://api.iyk0.com/wymusic/?" + parse.urlencode({"msg":self.my_cont}) + "&n=1&format=json"
    #     req = request.Request(url)
    #     res = request.urlopen(req).read().decode()
    #     resp = json.loads(res)
    #     music_title = resp['song']
    #     singer = resp['singer']
    #     url_url = resp['url']
    #     image = resp['img']
    #     msg = {"type": "music",
    #             "data": {
    #                 "image":image,
    #                 "type": "custom", 
    #                 "content": singer,
    #                 "audio":url_url,
    #                 "title":music_title
    #             }
    #     }
    #     return self.send_msg(msg)

    # 网易音乐
    def handle(self):
        url = "https://api.iyk0.com/wymusic/?" + parse.urlencode({"msg":self.my_cont}) + "&n=1&format=json"
        req = request.Request(url)
        res = request.urlopen(req).read().decode()
        resp = json.loads(res)
        id = nums = re.findall(".*id=(\\d+)", resp['url'])[0]
        image = resp['img']
        msg = {"type": "music",
                "data": {
                    "type":"163", 
                    "id":id
                }
        }
        return self.send_msg(msg)