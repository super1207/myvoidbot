import random

from core.MsgTool import MsgTool as MT
from core.Plugin import Plugin

"""
在下面加入你自定义的插件，自动加载本文件所有的 Plugin 的子类
只需要写一个 Plugin 的子类，重写 match() 和 handle()
match() 返回 True 则自动回调 handle()
"""

url = [
    "/group85/M0B/D7/10/wKg5H18icMrB_sH2ALlyvXP0fIk629.m4a",
    "/group85/M09/CD/6F/wKg5H18hdSigmZ-hALtzOQSvoGQ765.m4a",
    "/group84/M0A/D4/BA/wKg5JF8iOU_CwYUDALcUR4bX0UM588.m4a",
    "/group85/M0B/CD/CD/wKg5JV8hehXA17ZWALtYyaZ20nw130.m4a",
    "/group85/M06/CA/7A/wKg5JV8hURmiKK7GAKkPavHeIt4318.m4a",
    "/storages/2f07-audiofreehighqps/7D/D7/CMCoOSYDKlpTAKHeAQBSFayt.m4a",
    "/group82/M04/CA/72/wKg5HF8hb8_QZVDnAKkj-zsBAHc198.m4a",
    "/group86/M06/CA/7E/wKg5IF8hSk6xgWrXAKy1WOV4YQY436.m4a",
    "/group85/M02/CA/55/wKg5JV8hTh2BQc4bALcFmKegTxE235.m4a",
    "/group86/M05/CA/1C/wKg5Jl8hRLHyPAFWAK8eFv6c_3M969.m4a",
    "/group85/M07/CA/2B/wKg5H18hR5PwTfXXAK28MsKL_x0423.m4a",
    "/group86/M08/AC/81/wKg5Jl8eqeywWbmvAK-Kv90zIJI018.m4a",
    "/group86/M01/AC/95/wKg5IF8eqfChtAlZALEi-WRHKA0734.m4a",
    "/group86/M01/AC/90/wKg5IF8eqdqBOQdqAK0k9Dq4KnQ853.m4a",
    "/group86/M08/AC/7E/wKg5Jl8eqd6TJQFmALBMl_8-i7Y988.m4a",
    "/group86/M0B/AC/8B/wKg5IF8eqcuyYlmuAK3fb-htKtU590.m4a",
    "/group82/M03/1D/D0/wKg5Il8pLy6DKcVeAK6v9i35D1Q027.m4a",
    "/group86/M0B/AC/8B/wKg5IF8eqcyBPL9DALMiViM4gWs908.m4a",
    "/group86/M08/AC/7A/wKg5Jl8eqdLi_mkUAK7vGuy2cXc282.m4a",
    "/storages/ead4-audiofreehighqps/B9/28/CMCoOSMDInUOALiPIwBQUxSg.m4a",
    "/storages/fa96-audiofreehighqps/DE/AA/CMCoOSIDt3p9AKwm5wBzxuTo.m4a",
    "/storages/650d-audiofreehighqps/AA/56/CKwRIDoEMQI8AKps5gCWWVnV.m4a",
    "/storages/6ac7-audiofreehighqps/DC/C7/CKwRIasEm5hLAKtiIQC5Birt.m4a",
    "storages/e84d-audiofreehighqps/A5/55/CKwRIUEE0IkHALAEoQDMnBzk.m4a"
]

class TestPlugin(Plugin):
    def match(self):
        return self.on_full_match("#来套4级听力") or self.on_full_match("#来套四级听力")

    def handle(self):
        
        music_url = "https://fdfs.xmcdn.com" + url[random.randint(0,len(url) - 1)]
        # 音频来自喜马拉雅,有效时间不明
        msg = {"type": "music", "data": {
                    "image":"http://p2.music.126.net/y19E5SadGUmSR8SZxkrNtw==/109951163785855539.jpg",
                    "type": "custom", 
                    "url": "","audio":music_url,
                    "title":"英语听力"
                    }
            }
        return self.send_msg(MT.at(self.context["user_id"]), msg)

