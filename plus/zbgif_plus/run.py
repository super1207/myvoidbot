import os
import logging
import base64
import random
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

def get_tou(qq: str) -> BytesIO:
    # 获取头像
    url = "http://q1.qlogo.cn/g?b=qq&nk=" + qq + "&s=640"
    res = request.urlopen(request.Request(url)).read()
    return BytesIO(res)

def get_pic_path(dir1: str,dir2: str):
    # 获得资源路径
    current_dir = os.path.dirname(__file__)
    pic_dir = os.path.join(current_dir,"sucai",dir1,dir2)
    if os.path.isfile(pic_dir):
        return pic_dir
    # 如果不存在,则下载
    url = "https://cdn.jsdelivr.net/gh/super1207/sucai@main/"+ dir1 +"/" + dir2
    logging.getLogger(__name__).debug( "正在下载:" + url)
    res = request.urlopen(request.Request(url)).read()
    if not os.path.isdir(os.path.dirname(pic_dir)):
        os.makedirs(os.path.dirname(pic_dir))
    with open(pic_dir,"wb+") as f:
        f.write(res)
    return pic_dir
    

def dst_over(sou: Image,tou :Image,w: int,h: int,x: int,y: int) -> Image:
    # 图像叠加
    if w == 0 or h == 0:
        w,h = tou.size
    tou = tou.resize((w,h))
    bg_size = sou.size
    bg = Image.new('RGBA', bg_size, color=(255,255,255,255)) #白色背景
    bg.paste(tou,(x, y, (x + w), (y + h)),mask=tou)
    if sou.mode != "RGBA":
        sou = sou.convert("RGBA")
    return Image.alpha_composite(bg,sou)

def dst_over_c(sou: Image,tou :Image,w: int,h: int,x: int,y: int) -> Image:
    # 图像叠加,x,y是图像的中心点
    if w == 0 or h == 0:
        w,h = tou.size
    return dst_over(sou,tou,w,h,int(-w/2 + 0.5 + x),int(-h/2 + 0.5 + y))

def over(sou: Image,tou :Image,w: int,h: int,x: int,y: int) -> Image:
    if w == 0 or h == 0:
        w,h = tou.size
    tou_t = tou.resize((w,h))
    sou_t = sou.copy()
    if sou_t.mode != "RGBA":
        sou_t = sou.convert("RGBA")
    sou_t.paste(tou_t,(x, y, (x + w), (y + h)),mask = tou_t)
    return sou_t

def img_to_b64(img: Image) -> str:
    buffer = BytesIO()
    img.save(buffer,format="png")
    myimage = buffer.getvalue()
    return "base64://" + base64.b64encode(myimage).decode()

def imgs_to_b64(imgs: Image,duration: int) -> str:
    # 将一组图片合成gif,并输出base64 url
    buffer = BytesIO()
    imgs[0].save(buffer,format="gif",save_all=True, append_images=imgs, duration=duration)
    myimage = buffer.getvalue()
    return "base64://" + base64.b64encode(myimage).decode()

def img_to_circle(img: Image):
    # 将图片变成圆的
    bg = Image.new('RGBA', img.size, color=(255,255,255,0))
    mask = Image.new('RGBA', img.size, color=(0,0,0,0))
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0,0, img.size[0], img.size[1]), fill=(0,0,0,255))
    bg.paste(img, (0, 0, (img.size[0]), (img.size[1])), mask)
    return bg


class TestPluginMo(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        self.my_text = MT.get_text_from_msg(self.context["message"]).strip()
        return self.my_text.startswith("#摸")

    def handle(self):
        try:
            the_at = MT.get_at_from_msg(self.context["message"])
        except:
            the_at = self.my_text[len("#摸"):]
        tou = img_to_circle(Image.open(get_tou(the_at)).resize((100,100)))
        mo = [
            dst_over(Image.open(get_pic_path("mo","0.png")),tou,80, 80, 32, 32),
            dst_over(Image.open(get_pic_path("mo","1.png")),tou,70, 90, 42, 22),
            dst_over(Image.open(get_pic_path("mo","2.png")),tou,75, 85, 37, 27),
            dst_over(Image.open(get_pic_path("mo","3.png")),tou,85, 75, 27, 37),
            dst_over(Image.open(get_pic_path("mo","4.png")),tou,90, 70, 22, 42)
        ]
        out_img_url = imgs_to_b64(mo,10)
        self.send_msg(MT.at(self.context["user_id"]), MT.image(out_img_url))



class TestPluginCuo(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        self.my_text = MT.get_text_from_msg(self.context["message"]).strip()
        return self.my_text.startswith("#搓")

    def handle(self):
        try:
            the_at = MT.get_at_from_msg(self.context["message"])
        except:
            the_at = self.my_text[len("#搓"):]
        tou = Image.open(get_tou(the_at)).resize((110,110))
        m1 = img_to_circle(tou.rotate(72))
        m2 = img_to_circle(tou.rotate(144))
        m3 = img_to_circle(tou.rotate(216))
        m4 = img_to_circle(tou.rotate(288))
        tou = img_to_circle(tou)

        cuo = [
            dst_over_c(Image.open(get_pic_path("cuo","0.png")),tou,0, 0, 75, 130),
            dst_over_c(Image.open(get_pic_path("cuo","1.png")),m1,0, 0, 75, 130),
            dst_over_c(Image.open(get_pic_path("cuo","2.png")),m2,0, 0, 75, 130),
            dst_over_c(Image.open(get_pic_path("cuo","3.png")),m3,0, 0, 75, 130),
            dst_over_c(Image.open(get_pic_path("cuo","4.png")),m4,0, 0, 75, 130)
        ]
        out_img_url = imgs_to_b64(cuo,50)
        self.send_msg(MT.at(self.context["user_id"]), MT.image(out_img_url))

class TestPluginQiao(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        self.my_text = MT.get_text_from_msg(self.context["message"]).strip()
        return self.my_text.startswith("#敲")

    def handle(self):
        try:
            the_at = MT.get_at_from_msg(self.context["message"])
        except:
            the_at = self.my_text[len("#敲"):]
        tou = img_to_circle(Image.open(get_tou(the_at)))

        qiao = [
            over(Image.open(get_pic_path("qiao","0.png")),tou,40, 33, 57, 52),
            over(Image.open(get_pic_path("qiao","1.png")),tou,38, 36, 58, 50)
        ]
        out_img_url = imgs_to_b64(qiao,10)
        self.send_msg(MT.at(self.context["user_id"]), MT.image(out_img_url))

class TestPluginChi(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        self.my_text = MT.get_text_from_msg(self.context["message"]).strip()
        return self.my_text.startswith("#吃")

    def handle(self):
        try:
            the_at = MT.get_at_from_msg(self.context["message"])
        except:
            the_at = self.my_text[len("#吃"):]

        tou = img_to_circle(Image.open(get_tou(the_at))).resize((32,32))

        chi = [
            dst_over(Image.open(get_pic_path("chi","0.png")),tou,0, 0, 1, 38),
            dst_over(Image.open(get_pic_path("chi","1.png")),tou,0, 0, 1, 38),
            dst_over(Image.open(get_pic_path("chi","2.png")),tou,0, 0, 1, 38)
        ]
        out_img_url = imgs_to_b64(chi,10)
        self.send_msg(MT.at(self.context["user_id"]), MT.image(out_img_url))

class TestPluginKen(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        self.my_text = MT.get_text_from_msg(self.context["message"]).strip()
        return self.my_text.startswith("#啃")

    def handle(self):
        try:
            the_at = MT.get_at_from_msg(self.context["message"])
        except:
            the_at = self.my_text[len("#啃"):]

        tou = img_to_circle(Image.open(get_tou(the_at))).resize((100,100))

        chi = [
            dst_over(Image.open(get_pic_path("ken","0.png")),tou,90, 90, 105, 150),
            dst_over(Image.open(get_pic_path("ken","1.png")),tou,90, 83, 96, 172),
            dst_over(Image.open(get_pic_path("ken","2.png")),tou,90, 90, 106, 148),
            dst_over(Image.open(get_pic_path("ken","3.png")),tou,88, 88, 97, 167),
            dst_over(Image.open(get_pic_path("ken","4.png")),tou,90, 85, 89, 179),
            dst_over(Image.open(get_pic_path("ken","5.png")),tou,90, 90, 106, 151),
            Image.open(get_pic_path("ken","6.png")),
            Image.open(get_pic_path("ken","7.png")),
            Image.open(get_pic_path("ken","8.png")),
            Image.open(get_pic_path("ken","9.png")),
            Image.open(get_pic_path("ken","10.png")),
            Image.open(get_pic_path("ken","11.png")),
            Image.open(get_pic_path("ken","12.png")),
            Image.open(get_pic_path("ken","13.png")),
            Image.open(get_pic_path("ken","14.png")),
            Image.open(get_pic_path("ken","15.png"))
        ]
        out_img_url = imgs_to_b64(chi,70)
        self.send_msg(MT.at(self.context["user_id"]), MT.image(out_img_url))

class TestPluginPai(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        self.my_text = MT.get_text_from_msg(self.context["message"]).strip()
        return self.my_text.startswith("#拍")

    def handle(self):
        try:
            the_at = MT.get_at_from_msg(self.context["message"])
        except:
            the_at = self.my_text[len("#拍"):]

        tou = img_to_circle(Image.open(get_tou(the_at))).resize((30,30))

        chi = [
            over(Image.open(get_pic_path("pai","0.png")),tou,0, 0, 1, 47),
            over(Image.open(get_pic_path("pai","1.png")),tou,0, 0, 1, 67),
        ]
        out_img_url = imgs_to_b64(chi,10)
        self.send_msg(MT.at(self.context["user_id"]), MT.image(out_img_url))

class TestPluginChong(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        self.my_text = MT.get_text_from_msg(self.context["message"]).strip()
        return self.my_text.startswith("#冲")

    def handle(self):
        try:
            the_at = MT.get_at_from_msg(self.context["message"])
        except:
            the_at = self.my_text[len("#冲"):]

        tou = img_to_circle(Image.open(get_tou(the_at)))

        chong = [
            over(Image.open(get_pic_path("xqe","0.png")),tou,30, 30, 15, 53),
            over(Image.open(get_pic_path("xqe","1.png")),tou,30, 30, 40, 53),
        ]
        out_img_url = imgs_to_b64(chong,10)
        self.send_msg(MT.at(self.context["user_id"]), MT.image(out_img_url))

class TestPluginDiu(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        self.my_text = MT.get_text_from_msg(self.context["message"]).strip()
        return self.my_text.startswith("#丢")

    def handle(self):
        try:
            the_at = MT.get_at_from_msg(self.context["message"])
        except:
            the_at = self.my_text[len("#丢"):]

        tou = img_to_circle(Image.open(get_tou(the_at)))

        diu  = [
            over(Image.open(get_pic_path("diu","0.png")),tou,32, 32, 108, 36),
            over(Image.open(get_pic_path("diu","1.png")),tou,32, 32, 122, 36),
            Image.open(get_pic_path("diu","2.png")),
            over(Image.open(get_pic_path("diu","3.png")),tou,123, 123, 19, 129),
            over(over(Image.open(get_pic_path("diu","4.png")),tou,123, 123, 19, 129),tou, 33, 33, 289, 70),
            over(Image.open(get_pic_path("diu","5.png")),tou,32, 32, 280, 73),
            over(Image.open(get_pic_path("diu","6.png")),tou,35, 35, 259, 31),
            over(Image.open(get_pic_path("diu","7.png")),tou,175, 175, -50, 220),

        ]
        out_img_url = imgs_to_b64(diu ,70)
        self.send_msg(MT.at(self.context["user_id"]), MT.image(out_img_url))

class TestPluginPa(Plugin):
    def match(self):
        if self.context["post_type"] != "message":
            return False
        self.my_text = MT.get_text_from_msg(self.context["message"]).strip()
        return self.my_text.startswith("#爬")

    def handle(self):
        try:
            the_at = MT.get_at_from_msg(self.context["message"])
        except:
            the_at = self.my_text[len("#爬"):]

        tou = img_to_circle(Image.open(get_tou(the_at)))
        out_img = over(Image.open(get_pic_path("pa",str(random.randint(1,60))+".png")),tou,100, 100, 0, 400)
        out_img_url = img_to_b64(out_img)
        self.send_msg(MT.at(self.context["user_id"]), MT.image(out_img_url))