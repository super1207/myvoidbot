import os
import json
import logging
import base64
from urllib import request

from core.MsgTool import MsgTool as MT
from core.Plugin import Plugin

"""
在下面加入你自定义的插件，自动加载本文件所有的 Plugin 的子类
只需要写一个 Plugin 的子类，重写 match() 和 handle()
match() 返回 True 则自动回调 handle()
"""

def get_json_path():
    # 获得资源路径
    current_dir = os.path.dirname(__file__)
    json_dir = os.path.join(current_dir,"emojiData.json")
    if os.path.isfile(json_dir):
        return json_dir
    # 如果不存在,则下载
    url = "https://cdn.jsdelivr.net/gh/xsalazar/emoji-kitchen@main/src/Components/emojiData.json"
    logging.getLogger(__name__).debug( "正在下载:" + url)
    res = request.urlopen(request.Request(url)).read()
    if not os.path.isdir(os.path.dirname(json_dir)):
        os.makedirs(os.path.dirname(json_dir))
    with open(json_dir,"wb+") as f:
        f.write(res)
    return json_dir

def emoji_to_int(emoji: str) -> int:
    code = emoji.encode('utf-8')
    if len(code) == 1:
        return code[0]
    elif len(code) == 2:
        return int((code[0] & 0x1F)) << 6
    elif len(code) == 3:
        t = (int)(code[0] & 0x0F) << 12
        t = t | (int)(code[1] & 0x3F) << 6
        t = t | (int)(code[2] & 0x3F)
        return t
    elif len(code) == 4:
        t = (int)(code[0] & 0x07) << 18
        t = t | (int)(code[1] & 0x3F) << 12
        t = t | (int)(code[2] & 0x3F) << 6
        t = t | (int)(code[3] & 0x3F)
        return t
    elif len(code) == 5:
        t = (int)(code[0] & 0x03) << 24
        t = t | (int)(code[1] & 0x3F) << 18
        t = t | (int)(code[2] & 0x3F) << 12
        t = t | (int)(code[3] & 0x3F) << 6
        t = t | (int)(code[4] & 0x3F)
        return t
    elif len(code) == 6:
        t = (int)(code[0] & 0x03) << 30
        t = t | (int)(code[1] & 0x3F) << 24
        t = t | (int)(code[2] & 0x3F) << 18
        t = t | (int)(code[3] & 0x3F) << 12
        t = t | (int)(code[4] & 0x3F) << 6
        t = t | (int)(code[5] & 0x3F)
        return t


class TestPlugin(Plugin):
    def match(self):  # 说 今日新闻 则回复
        if self.context["post_type"] != "message":
            return False
        self.my_text = MT.get_text_from_msg(self.context["message"]).strip()
        if not self.my_text.startswith("#mix"):
            return False
        cont = self.my_text[len("#mix"):]
        self.my_emoji1 = cont[0]
        self.my_emoji2 = cont[1]
        return True

    def handle(self):
        code1 = emoji_to_int(self.my_emoji1)
        code2 = emoji_to_int(self.my_emoji2)
        json_path = get_json_path()
        with open(json_path,"rb") as f:
            json_str = f.read().decode('utf8')
        json_dat = json.loads(json_str)
        json_arr = json_dat[hex(code1)[2:]]
        flag = False
        for it in json_arr:
            if it["rightEmoji"] == hex(code1)[2:] or it["leftEmoji"] == hex(code1)[2:]:
                flag = True
                emoji_left = it["leftEmoji"]
                emoji_right = it["rightEmoji"]
                date = it["date"]
                break
        if not flag:
            return self.send_msg(MT.text(self.my_emoji1 + "+" + self.my_emoji2 + "=?"))
        url = "https://www.gstatic.com/android/keyboard/emojikitchen/{date}/u{emojiLeft}/u{emojiLeft}_u{emojiRight}.png".format(
            date = date,
            emojiLeft = emoji_left,
            emojiRight = emoji_right
        )
        req = request.Request(url)
        res = request.urlopen(req).read()
        b64_url = "base64://" + base64.b64encode(res).decode()
        return self.send_msg(MT.image(b64_url))