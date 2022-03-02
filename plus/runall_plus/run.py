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

def get_lan_info():
    current_dir = os.path.dirname(__file__)
    info_dir = os.path.join(current_dir,"lan.txt")
    with open(info_dir,"r") as f:
        info = f.read()
    info_map = {}
    infovec = info.split('\n\n')
    for its in infovec:
        it = its.split('\n')
        info_map[it[2]] = {"lan":it[0],"file":it[1]}
    return info_map

lan_info = get_lan_info()

class TestPlugin(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        cont = MT.get_text_from_msg(self.context["message"])
        return cont.startswith("#run")

    def handle(self):
        cqmap = {}
        if isinstance(self.context["message"],str):
            str_msg = self.context["message"]
        else:
            str_msg = MT.arr_msg_to_str(self.context["message"])
        lines = str_msg.split('\n')
        line = str_msg.split('\n')[0]
        lan = line[len("#run"):].strip()
        dat_str = '\n'.join(str_msg.split('\n')[1:])
        arr_msg = MT.str_msg_to_arr(dat_str)
        web_msg = ""
        for it in arr_msg:
            if it['type'] == 'text':
                web_msg += it["data"]["text"]
            else:
                u = str(uuid.uuid4())
                cqmap[u] = MT.arr_msg_to_str([it])
                web_msg += u

        if not lan in lan_info.keys():
            return self.send_msg(MT.at(self.context["user_id"]), MT.text("不支持的语言"))
        
        j = {
            "files":[{
                "name":lan_info[lan]["file"] + "." + lan,
                "content":web_msg,
                "stdin": "",
                "command": ""
            }]
        }
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "Content-Type":"application/json",
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "Cache-Control":"no-cache",
            "Cache-Control":"glot.io",
            "X-Requested-With":"XMLHttpRequest",
            "Origin":"https://glot.io"
        }
        url = "https://glot.io/run/" + lan_info[lan]["lan"] + "?version=latest"
        req = request.Request(url,data=bytes(json.dumps(j),"utf8"),headers=headers)
        try:
            res = request.urlopen(req,timeout=30).read().decode()
            j = json.loads(res)
            if "message" in j and isinstance(j["message"],str):
                return self.send_msg(MT.at(self.context["user_id"]), MT.text(j["message"]))
            out_str = j["stdout"] + j["error"] + j["stderr"]
            s = MT.arr_msg_to_str([{"type":"text","data":{"text":out_str}}])
            for k in cqmap:
                s = s.replace(k,cqmap[k])
            params = {"group_id": self.context["group_id"], "message": s}
            self.call_api("send_group_msg", params)
        except Exception as e:
            return self.send_msg(MT.at(self.context["user_id"]), MT.text(str(e)))

