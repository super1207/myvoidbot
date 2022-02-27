import re
import queue
import json as json_

class Plugin:
    def __init__(self, context: dict,echo,WS_APP,NICKNAME,SUPER_USER,logger):
        self.ws = WS_APP
        self.echo = echo
        self.context = context
        self.NICKNAME = NICKNAME
        self.SUPER_USER = SUPER_USER
        self.logger = logger

    def match(self) -> bool:
        return False

    def handle(self):
        pass

    def on_message(self) -> bool:
        return self.context["post_type"] == "message"

    def on_full_match(self, keyword="") -> bool:
        return self.on_message() and self.context["message"] == keyword

    def on_reg_match(self, pattern="") -> bool:
        return self.on_message() and re.search(pattern, self.context["message"])

    def only_to_me(self) -> bool:
        flag = False
        for nick in self.NICKNAME + [f"[CQ:at,qq={self.context['self_id']}] "]:
            if self.on_message() and nick in self.context["message"]:
                flag = True
                self.context["message"] = self.context["message"].replace(nick, "")
        return flag

    def super_user(self) -> bool:
        return self.context["user_id"] in self.SUPER_USER

    def admin_user(self) -> bool:
        return self.super_user() or self.context["sender"]["role"] in ("admin", "owner")

    def call_api(self, action: str, params: dict) -> dict:
        echo_num, q = self.echo.get()
        data = json_.dumps({"action": action, "params": params, "echo": echo_num})
        self.logger.info("发送调用 <- " + data)
        self.ws.send(data)
        try:    # 阻塞至响应或者等待30s超时
            return q.get(timeout=30)
        except queue.Empty:
            self.logger.error("API调用[{echo_num}] 超时......")

    def send_msg(self, *message) -> int:
        # https://github.com/botuniverse/onebot-11/blob/master/api/public.md#send_msg-%E5%8F%91%E9%80%81%E6%B6%88%E6%81%AF
        if "group_id" in self.context and self.context["group_id"]:
            return self.send_group_msg(*message)
        else:
            return self.send_private_msg(*message)

    def send_private_msg(self, *message) -> int:
        # https://github.com/botuniverse/onebot-11/blob/master/api/public.md#send_private_msg-%E5%8F%91%E9%80%81%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF
        params = {"user_id": self.context["user_id"], "message": message}
        ret = self.call_api("send_private_msg", params)
        return 0 if ret is None or ret["status"] == "failed" else ret["data"]["message_id"]

    def send_group_msg(self, *message) -> int:
        # https://github.com/botuniverse/onebot-11/blob/master/api/public.md#send_group_msg-%E5%8F%91%E9%80%81%E7%BE%A4%E6%B6%88%E6%81%AF
        params = {"group_id": self.context["group_id"], "message": message}
        ret = self.call_api("send_group_msg", params)
        return 0 if ret is None or ret["status"] == "failed" else ret["data"]["message_id"]