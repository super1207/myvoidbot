import json
from urllib import request

from core.MsgTool import MsgTool as MT
from core.Plugin import Plugin

"""
在下面加入你自定义的插件，自动加载本文件所有的 Plugin 的子类
只需要写一个 Plugin 的子类，重写 match() 和 handle()
match() 返回 True 则自动回调 handle()
"""

# 请自己到 `https://www.alapi.cn` 注册账号并获取token
g_token = 'EmY3BKCuiYrt4BBS'

class TestPlugin(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        text = MT.get_text_from_msg(self.context["message"]).strip()
        if text.startswith('#快递查询'):
            self.my_number = text[len("#快递查询"):].strip()
            return True
        return False

    def handle(self):
        url = "https://v2.alapi.cn/api/kd?token={}&number={}&order=desc".format(g_token,self.my_number)
        req = request.Request(url)
        res = request.urlopen(req).read().decode()
        js = json.loads(res)
        code = js['code']
        if code != 200:
            self.send_msg(MT.at(self.context["user_id"]), MT.text('单号{}查询失败:{}'.format(self.my_number,code)))
            return
        js_data = js['data']
        com = js_data['com']
        state_str = ['未知','正常','派送中','已签收','退回','其他问题'][js_data['state']]
        tm = js_data['info'][0]['time']
        cont = js_data['info'][0]['content']
        ret_text = '单号{}查询成功！\n快递公司:{}\n状态:{}\n时间:{}\n{}'.format(self.my_number,com,state_str,tm,cont)
        if self.context["message_type"] != 'group':
            self.send_msg(MT.text(ret_text))
        else:
            self.send_msg(MT.at(self.context["user_id"]), MT.text('\n'), MT.text(ret_text))
