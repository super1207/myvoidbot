from core.MsgTool import MsgTool as MT
from core.Plugin import Plugin

"""
在下面加入你自定义的插件，自动加载本文件所有的 Plugin 的子类
只需要写一个 Plugin 的子类，重写 match() 和 handle()
match() 返回 True 则自动回调 handle()
"""

class TestPlugin(Plugin):
    def match(self):
        return self.on_full_match("#来套4级听力") or self.on_full_match("#来套四级听力")

    def handle(self):
        music_url = "https://fdfs.xmcdn.com///group86/M08/AC/7E/wKg5Jl8eqd6TJQFmALBMl_8-i7Y988.m4a"
        # 暂时就一套,有空再补充,音频可能来自喜马拉雅,有效时间不明
        msg = {"type": "music", "data": {
                    "image":"http://p2.music.126.net/y19E5SadGUmSR8SZxkrNtw==/109951163785855539.jpg",
                    "type": "custom", 
                    "url": "","audio":music_url,
                    "title":"英语听力"
                    }
            }
        return self.send_msg(MT.at(self.context["user_id"]), msg)

