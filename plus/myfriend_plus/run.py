import os
import base64
from io import BytesIO
from urllib import request

from core.MsgTool import MsgTool as MT
from core.Plugin import Plugin

from PIL import Image, ImageDraw,ImageFont

"""
在下面加入你自定义的插件，自动加载本文件所有的 Plugin 的子类
只需要写一个 Plugin 的子类，重写 match() 和 handle()
match() 返回 True 则自动回调 handle()
"""

class TestPlugin(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        self.my_text = MT.get_text_from_msg(self.context["message"])
        return self.my_text.startswith("#朋友")

    def handle(self):
        cont = self.my_text[len("#朋友"):]
        the_at = MT.get_at_from_msg(self.context["message"])
        url = "http://q1.qlogo.cn/g?b=qq&nk=" + the_at + "&s=640"
        req = request.Request(url)
        res = request.urlopen(req).read()
        temp_tou = BytesIO(res)
        bg_size = (600, 253)
        bg = Image.new('RGB', bg_size, color=(245,245,245))
        current_dir = os.path.dirname(__file__) # 获得当前目录
        avatar_size = (155, 155) 
        avatar = Image.open(temp_tou)
        avatar = avatar.resize(avatar_size)
        mask = Image.new('RGBA', avatar_size, color=(0,0,0,0))
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0,0, avatar_size[0], avatar_size[1]), fill=(0,0,0,255))
        x, y = 45,45
        box = (x, y, (x + avatar_size[0]), (y + avatar_size[1]))
        bg.paste(avatar, box, mask)
        # path_to_ttf = os.path.join(current_dir,"fz.ttf")
        path_to_ttf = "simsun.ttc"
        font = ImageFont.truetype(path_to_ttf, size=38)
        font2 = ImageFont.truetype(path_to_ttf, size=36)
        draw = ImageDraw.Draw(bg)
        draw.text(xy=(210,110-38),text='朋友',font=font,fill = (0, 0, 0))
        draw.text(xy=(210,170-35),text = cont,font=font,fill = (190, 190, 190))
        img_path = os.path.join(current_dir,"out.jpg")
        buffer = BytesIO()
        bg.save(buffer,format="JPEG")
        myimage = buffer.getvalue()
        self.send_msg(MT.at(self.context["user_id"]), MT.image("base64://" + base64.b64encode(myimage).decode()))
        
