import os
import sys
import string
import sqlite3
import base64
import random
import time as time_
import datetime

from core.MsgTool import MsgTool as MT
from core.Plugin import Plugin

import jieba
from zhon import hanzi
import wordcloud


"""
在下面加入你自定义的插件，自动加载本文件所有的 Plugin 的子类
只需要写一个 Plugin 的子类，重写 match() 和 handle()
match() 返回 True 则自动回调 handle()
"""

def deal_sqlite(time,group,data):
    current_dir = os.path.dirname(__file__)
    dat_dir = os.path.join(current_dir,"dat.db")
    conn = sqlite3.connect(dat_dir)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS MYTABLE 
       (
           [id]      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
           [time]    INTEGER                       NOT NULL,
           [group]   INTEGER                       NOT NULL,
           [data]    TEXT                          NOT NULL
       );''')
    c.execute("INSERT INTO MYTABLE([time], [group], [data]) values(?, ?, ?)", (time,group," ".join(data)))
    conn.commit()
    
class TestPlugin(Plugin):
    def match(self): 
        if self.context["post_type"] != "message":
            return False
        if self.on_full_match("#今日词云"):
            return True
        cont = MT.get_text_from_msg(self.context["message"]).strip()
        jieba_word=jieba.cut(cont)
        data=[]
        for word in jieba_word:
            # 去标点和空白字符
            if word not in hanzi.punctuation + string.punctuation + '\t\n \r\f\v':
                data.append(word)
        data = {}.fromkeys(data).keys() # 去重
        if len(data) == 0:
            return False
        # 插入数据库
        deal_sqlite(self.context["time"],self.context["group_id"],data)
        return False

    def handle(self):
        current_dir = os.path.dirname(__file__)
        dat_dir = os.path.join(current_dir,"dat.db")
        conn = sqlite3.connect(dat_dir)
        c = conn.cursor()
        today = datetime.date.today()
        today_start_time = int(time_.mktime(time_.strptime(str(today), '%Y-%m-%d')))
        cursor  = c.execute("SELECT [data] from MYTABLE WHERE [time]>" + str(today_start_time) + " AND [group]=" + str(self.context["group_id"]))
        word = []
        for row in cursor:
            t = row[0]
            word += t.split(' ')
        if len(word) == 0:
            return self.send_msg(MT.at(self.context["user_id"]), MT.text("今日本群没有词语"))
        word = ' '.join(word)
        if sys.platform == "win32":
            font_path = "simsun.ttc"
        else:
            font_path = "/usr/share/fonts/font/simsun.ttc"
        wc = wordcloud.WordCloud(font_path = font_path,scale = 6,max_words=50)
        wc.generate(word)
        file_name = str(random.random())+".png"
        current_dir = os.path.dirname(__file__)
        dat_dir = os.path.join(current_dir,file_name)
        wc.to_file(dat_dir)
        try:
            with open(dat_dir,"rb") as f:
                self.send_msg(MT.at(self.context["user_id"]), MT.image("base64://" + base64.b64encode(f.read()).decode()))
        except Exception as err:
            raise err
        finally:
            os.remove(dat_dir)
        
        # cont = MT.get_text_from_msg(self.context["message"]).strip()
        # jieba_word=jieba.cut(cont,cut_all=False)
        # print(jieba_word)

