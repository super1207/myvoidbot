import random
import threading

from core.MsgTool import MsgTool as MT
from core.Plugin import Plugin

"""
在下面加入你自定义的插件，自动加载本文件所有的 Plugin 的子类
只需要写一个 Plugin 的子类，重写 match() 和 handle()
match() 返回 True 则自动回调 handle()
"""

percentage = 0.5 # 触发复读的概率为50%

g_mx_map = threading.Lock()
g_map = {}

class TestPlugin(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        if self.context["message_type"] != "group":
            return False
        group_id = self.context["group_id"]
        try:
            g_mx_map.acquire()
            if group_id not in g_map:
                g_map[group_id] = []
            g_map[group_id].append(self.context['raw_message'])
            if len(g_map[group_id]) > 4:
                g_map[group_id].pop(0)
            if len(g_map[group_id]) == 3:
                if g_map[group_id][0] == g_map[group_id][1] and g_map[group_id][0] == g_map[group_id][2]:
                    if random.random() < percentage:
                        return True
            if len(g_map[group_id]) == 4:
                if g_map[group_id][1] == g_map[group_id][2] and g_map[group_id][2] == g_map[group_id][3]:
                    if g_map[group_id][0] != g_map[group_id][1]:
                        if random.random() < percentage:
                            return True
        finally:
            g_mx_map.release()
        return False

    def handle(self):
        self.call_api('send_group_msg', {'group_id': self.context["group_id"], 'message': self.context['message']})

