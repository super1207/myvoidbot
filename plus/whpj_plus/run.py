import os
import re
import json
import logging
import base64
from urllib import request
from urllib import parse

from core.MsgTool import MsgTool as MT
from core.Plugin import Plugin

"""
在下面加入你自定义的插件，自动加载本文件所有的 Plugin 的子类
只需要写一个 Plugin 的子类，重写 match() 和 handle()
match() 返回 True 则自动回调 handle()
"""

def getHL(word):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    url = "https://srh.bankofchina.com/search/whpj/search_cn.jsp?" + parse.urlencode({"pjname":word})
    req = request.Request(url,headers=headers)
    res = request.urlopen(req).read().decode() 
    ret = re.compile("<td>(.*\d+\.{0,1}\d*)").findall(res)[2]
    return float(ret) / 100
    
class TestPlugin(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        self.my_text = MT.get_text_from_msg(self.context["message"]).strip()
        try:
            ret = re.compile("^#(\\d+)(.*)等于多少(.*)").findall(self.my_text)[0]
        except:
            return False
        if len(ret) != 3:
            return False
        self.my_ret = ret
        return True

    def handle(self):
        if self.my_ret[1] == '人民币':
            h1 = 1
        else:
            h1 = getHL(self.my_ret[1])
        if self.my_ret[2] == '人民币':
            h2 = 1
        else:
            h2 = getHL(self.my_ret[2])
        return self.send_msg(
                MT.at(self.context["user_id"]), 
                MT.text(str(round(float(self.my_ret[0])*h1/h2,4)))
            ) 
