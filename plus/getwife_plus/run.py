import time as time_
import os
import sqlite3
import threading
import random
import datetime

from matplotlib import image
from core.MsgTool import MsgTool as MT
from core.Plugin import Plugin

# 数据库加锁
sql_lock = threading.Lock()


"""
在下面加入你自定义的插件，自动加载本文件所有的 Plugin 的子类
只需要写一个 Plugin 的子类，重写 match() 和 handle()
match() 返回 True 则自动回调 handle()
"""


def get_tou(qq: str):
    # 获取头像
    url = "http://q1.qlogo.cn/g?b=qq&nk=" + str(qq) + "&s=640"
    return url

# 创建数据库
def create_sqlite():
    sql_conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),"dat.db"))
    c = sql_conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS MYTABLE 
    (
        [group_id]   INTEGER                       NOT NULL,
        [user_id]   INTEGER                       NOT NULL,
        [time]    INTEGER                       NOT NULL,
        [wife_id]    INTEGER                     NOT NULL,
        [wife_time]    INTEGER                     NOT NULL,
        primary key([group_id],[user_id])
    );''')
    # c.execute("INSERT INTO MYTABLE([time], [group], [data]) values(?, ?, ?)", (time,group," ".join(data)))
    sql_conn.commit()
    c.close()
    sql_conn.close()


# 获得本群三天内发过言的人
def get_three_sqlite(group_id:int) -> list[int]:
    sql_conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),"dat.db"))
    c = sql_conn.cursor()
    today = datetime.date.today()
    today_start_time = int(time_.mktime(time_.strptime(str(today), '%Y-%m-%d')))
    three_start_time = today_start_time - 60*60*24*2
    sql = '''
        SELECT [user_id] FROM MYTABLE
        WHERE 
            [time]>{} AND 
            [group_id]={} 
    '''.format(three_start_time,group_id)
    cursor  = c.execute(sql)
    user_ids = [row[0] for row in cursor]
    c.close()
    sql_conn.close()
    return user_ids

# 获得本群有老婆或者已经是别人老婆的人(老婆有效期1天)
def get_wife_sqlite(group_id:int) -> list[int]:
    sql_conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),"dat.db"))
    c = sql_conn.cursor()
    today = datetime.date.today()
    today_start_time = int(time_.mktime(time_.strptime(str(today), '%Y-%m-%d')))
    sql = '''
        SELECT [user_id],[wife_id] FROM MYTABLE
        WHERE
            [group_id]={} AND 
            [wife_time]>{} 
    '''.format(group_id,today_start_time)
    cursor  = c.execute(sql)
    user_ids = []
    for row in cursor:
        user_ids.append(row[0])
        user_ids.append(row[1])
    c.close()
    sql_conn.close()
    return list(set(user_ids))

def get_bachelor_sqlite(group_id:int):
    wifes = get_wife_sqlite(group_id)
    people = get_three_sqlite(group_id)
    return [i for i in people if i not in wifes]

# 数据库里面有没有记录
def exist_sqlite(group_id:int,user_id:int):
    sql_conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),"dat.db"))
    c = sql_conn.cursor()
    cursor  = c.execute("SELECT [user_id] FROM MYTABLE WHERE [group_id]=" + str(group_id) + " AND [user_id]=" + str(user_id))
    user_ids = [row[0] for row in cursor]
    if len(user_ids) == 0:
        return False
    return True

# 查询一个人的老婆
def search_sqlite(group_id:int,user_id:int):
    sql_conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),"dat.db"))
    c = sql_conn.cursor()
    today = datetime.date.today()
    today_start_time = int(time_.mktime(time_.strptime(str(today), '%Y-%m-%d')))
    sql = '''
        SELECT [user_id],[wife_id] FROM MYTABLE 
        WHERE 
            [group_id]={} AND 
            [user_id]={} AND 
            [wife_time]>{} 
    '''.format(group_id,user_id,today_start_time)
    cursor  = c.execute(sql)
    user_ids = [row[0] for row in cursor]
    if len(user_ids) == 0:
        return 0
    return user_ids[0]


# 设置一个人的老婆
def set_sqlite(group_id:int,user_id:int,wife_id:int):
    sql_conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),"dat.db"))
    c = sql_conn.cursor()
    tm = int(time_.time())
    sql = '''UPDATE MYTABLE 
            SET 
            [wife_id] = {} ,
            [wife_time] = {} 
            WHERE 
            [group_id]={} AND 
            [user_id]={}
            '''.format(wife_id,tm,group_id,user_id)
    c.execute(sql)
    sql_conn.commit()
    c.close()
    sql_conn.close()

# 有人发言啦
def update_sqlite(group_id:int,user_id:int):
    is_exist = exist_sqlite(group_id,user_id)
    sql_conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),"dat.db"))
    c = sql_conn.cursor()
    tm = int(time_.time())
    if is_exist:
        sql = '''UPDATE MYTABLE
              SET 
                [time]=? 
              WHERE 
                [group_id]={} AND 
                [user_id]={}
              '''.format(group_id,user_id)
        c.execute(sql,(tm,))
    else:
        sql = '''INSERT INTO MYTABLE(
                    [group_id], 
                    [user_id], 
                    [time],
                    [wife_id],
                    [wife_time]
                ) 
                values(?, ?, ?, ?, ?)'''
        c.execute(sql,(group_id,user_id,tm,0,0))
    sql_conn.commit()
    c.close()
    sql_conn.close()



    
class TestPlugin(Plugin):
    def get_group_member_card(self,group_id:int,user_id:int):
        params = {"group_id": self.context["group_id"], "user_id": self.context["user_id"]}
        ret = self.call_api("get_group_member_info", params)['data']
        # print(ret)
        if ret.get('card') == None:
            return ret['nickname']
        return ret['card']
        
    def match(self): 
        if self.context["post_type"] != "message":
            return False
        if self.context["message_type"] != "group":
            return False
        # 插入数据库
        try:
            sql_lock.acquire()
            create_sqlite()
            update_sqlite(self.context["group_id"],self.context["user_id"])
        finally:
            sql_lock.release()
        # 识别关键字
        cont = MT.get_text_from_msg(self.context["message"]).strip()
        if cont in ["#今天我老婆是谁","#今天谁是我老婆","#我老婆今天是谁"]:
            self.my_cont = "随机老婆"
            return True
        if cont in ["#换个老婆","#换一个老婆"]:
            self.my_cont = "换老婆"
            return True
        return False

    def handle(self):
        if self.my_cont == "随机老婆":
            try:
                sql_lock.acquire()
                wife_id = search_sqlite(self.context["group_id"],self.context["user_id"])
            finally:
                sql_lock.release()
            is_self = (self.context["user_id"] == wife_id)
            if  is_self:
                is_self = MT.text("\n今天你的老婆是你自己\n")
            else:
                is_self = MT.text("\n今天你的老婆是\n")
            if wife_id != 0: # 有老婆
                self.send_msg(
                    MT.at(self.context["user_id"]), 
                    is_self,
                    MT.image(get_tou(wife_id)),
                    MT.text("【{}】({})哒！\n".format(self.get_group_member_card(self.context["group_id"],self.context["user_id"]),wife_id)),
                    MT.at(wife_id), 
                    MT.text("尽情享用吧(笑"),
                )
            else: #没有老婆
                # print("没老婆")
                try:
                    sql_lock.acquire()
                    # 获得单身的人
                    people:list[int] = get_bachelor_sqlite(self.context["group_id"])
                finally:
                    sql_lock.release()
                # 候选老婆加上自己，选自己的的概率略高一点
                people.append(self.context['user_id'])
                # 随机选一个老婆
                wife_id = random.choice(people)
                try:
                    sql_lock.acquire()
                    set_sqlite(self.context["group_id"],self.context["user_id"],wife_id)
                finally:
                    sql_lock.release()
                is_self = (self.context["user_id"] == wife_id)
                if  is_self:
                    is_self = MT.text("\n今天你的老婆是你自己\n")
                else:
                    is_self = MT.text("\n今天你的老婆是\n")
                self.send_msg(
                    MT.at(self.context["user_id"]), 
                    is_self,
                    MT.image(get_tou(wife_id)),
                    MT.text("【{}】({})哒！\n".format(self.get_group_member_card(self.context["group_id"],self.context["user_id"]),wife_id)),
                    MT.at(wife_id), 
                    MT.text("尽情享用吧(笑"),
                )
        else:
            try:
                sql_lock.acquire()
                # 先删除自己的老婆
                set_sqlite(self.context["group_id"],self.context["user_id"],0)
                # 获得单身的人
                people:list[int] = get_bachelor_sqlite(self.context["group_id"])
            finally:
                sql_lock.release()
            # 候选老婆加上自己，选自己的的概率略高一点
            people.append(self.context['user_id'])
            # 随机选一个老婆
            wife_id = random.choice(people)
            try:
                sql_lock.acquire()
                set_sqlite(self.context["group_id"],self.context["user_id"],wife_id)
            finally:
                sql_lock.release()
            is_self = (self.context["user_id"] == wife_id)
            if  is_self:
                is_self = MT.text("尽情享用你自己吧(笑")
            else:
                is_self = MT.text("尽情享用吧(笑")
            self.send_msg(
                    MT.at(self.context["user_id"]), 
                    MT.text("\n你可真是个负心汉呀，那就给你换一个吧\n呐，你的新老婆\n"),
                    MT.image(get_tou(wife_id)),
                    MT.text("【{}】({})哒！\n".format(self.get_group_member_card(self.context["group_id"],self.context["user_id"]),wife_id)),
                    MT.at(wife_id), 
                    is_self,
                )

