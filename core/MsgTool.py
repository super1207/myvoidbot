import json as json_

class MsgTool:
    def text(string: str) -> dict:
        # https://github.com/botuniverse/onebot-11/blob/master/message/segment.md#%E7%BA%AF%E6%96%87%E6%9C%AC
        return {"type": "text", "data": {"text": string}}


    def image(file: str, cache=True) -> dict:
        # https://github.com/botuniverse/onebot-11/blob/master/message/segment.md#%E5%9B%BE%E7%89%87
        return {"type": "image", "data": {"file": file, "cache": cache}}


    def record(file: str, cache=True) -> dict:
        # https://github.com/botuniverse/onebot-11/blob/master/message/segment.md#%E8%AF%AD%E9%9F%B3
        return {"type": "record", "data": {"file": file, "cache": cache}}


    def at(qq: int) -> dict:
        # https://github.com/botuniverse/onebot-11/blob/master/message/segment.md#%E6%9F%90%E4%BA%BA
        return {"type": "at", "data": {"qq": qq}}


    def xml(data: str) -> dict:
        # https://github.com/botuniverse/onebot-11/blob/master/message/segment.md#xml-%E6%B6%88%E6%81%AF
        return {"type": "xml", "data": {"data": data}}


    def json(data: str) -> dict:
        # https://github.com/botuniverse/onebot-11/blob/master/message/segment.md#json-%E6%B6%88%E6%81%AF
        return {"type": "json", "data": {"data": data}}


    def music(data: str) -> dict:
        # https://github.com/botuniverse/onebot-11/blob/master/message/segment.md#%E9%9F%B3%E4%B9%90%E5%88%86%E4%BA%AB-
        return {"type": "music", "data": {"type": "qq", "id": data}}

    def cq_text_encode(data: str) -> str:
        ret_str = ""
        for ch in data:
            if ch == "&":
                ret_str += "&amp;"
            elif ch == "[":
                ret_str += "&#91;"
            elif ch == "]":
                ret_str += "&#93;"
            else:
                ret_str += ch
        return ret_str

    def cq_params_encode(data: str) -> str:
        ret_str = ""
        for ch in data:
            if ch == "&":
                ret_str += "&amp;"
            elif ch == "[":
                ret_str += "&#91;"
            elif ch == "]":
                ret_str += "&#93;"
            elif ch == ",":
                ret_str += "&#44;"
            else:
                ret_str += ch
        return ret_str

    def get_at_from_msg(message) -> str:
        msg_arr = message
        if isinstance(message,str):
            msg_arr = MsgTool.str_msg_to_arr(message)
        for it in msg_arr:
            if it["type"] == "at":
                return it["data"]["qq"]
        raise Exception("can't get at from message")

    def get_pic_from_msg(message) -> str:
        msg_arr = message
        if isinstance(message,str):
            msg_arr = MsgTool.str_msg_to_arr(message)
        for it in msg_arr:
            if it["type"] == "image":
                return it["data"]["url"]
        raise Exception("can't get img from message")

    def get_text_from_msg(message) -> str:
        msg_arr = message
        if isinstance(message,str):
            msg_arr = MsgTool.str_msg_to_arr(message)
        ret_str = ""
        for it in msg_arr:
            if it["type"] == "text":
                ret_str += it["data"]["text"]
        return ret_str

        
    def arr_msg_to_str(jsonarr: list) -> str:
        # 将 array 格式的 message 转化为 string 格式
        # https://github.com/botuniverse/onebot-11/blob/master/message/README.md
        ret_str = ""
        for it in jsonarr:
            type_ = it["type"]
            if type_ == "text":
                ret_str += MsgTool.cq_text_encode(it["data"]["text"])
            else:
                ret_str += "[CQ:" + type_
                kv = []
                for k,v in it["data"].items():
                    kv.append(k + "=" + MsgTool.cq_params_encode(v))
                if len(kv) == 0:
                    ret_str += "]"
                else:
                    ret_str += "," + ",".join(kv) + "]"
        return ret_str

    def str_msg_to_arr(cqstr: str) -> list:
        # 将 string 格式的 message 转化为 array 格式
        # https://github.com/botuniverse/onebot-11/blob/master/message/README.md
        text = ""
        type_ = ""
        key = ""
        val = ""
        jsonarr = []
        cqcode = {}
        stat = 0
        i = 0
        while i < len(cqstr):
            cur_ch = cqstr[i]
            if stat == 0:
                if cur_ch == '[':
                    t = ""
                    if i + 4 > len(cqstr):
                        t = ""
                    else:
                        t = cqstr[i:i+4]
                    if t == "[CQ:":
                        if len(text) != 0:
                            node = {}
                            node["type"] = "text"
                            node["data"] = {"text": text}
                            jsonarr.append(node)
                            text = ""
                        stat = 1
                        i += 3
                    else:
                        text += cqstr[i]
                elif cur_ch == '&':
                    t = ""
                    if i + 5 > len(cqstr):
                        t = ""
                    else:
                        t = cqstr[i : i+5]
                    if t == "&#91;":
                        text += '['
                        i += 4
                    elif t == "&#93;":
                        text += ']'
                        i += 4
                    elif t == "&amp;":
                        text += '&'
                        i += 4
                    else:
                        text += cqstr[i]
                else:
                    text += cqstr[i]
            elif stat == 1:
                if cur_ch == ',':
                    stat = 2
                elif cur_ch == '&':
                    t = ""
                    if i + 5 > len(cqstr):
                        t = ""
                    else:
                        t = cqstr[i : i+5]
                    if t == "&#91;":
                        type_ += '['
                        i += 4
                    elif t == "&#93;":
                        type_ += ']'
                        i += 4
                    elif t == "&amp;":
                        type_ += '&'
                        i += 4
                    elif t == "&#44;":
                        type_ += ','
                        i += 4
                    else:
                        type_ += cqstr[i]
                else:
                    type_ += cqstr[i]
            elif stat == 2:
                if cur_ch == '=':
                    stat = 3
                elif cur_ch == '&':
                    t = ""
                    if i + 5 > len(cqstr):
                        t = ""
                    else:
                        t = cqstr[i : i+5]
                    if t == "&#91;":
                        key += '['
                        i += 4
                    elif t == "&#93;":
                        key += ']'
                        i += 4
                    elif t == "&amp;":
                        key += '&'
                        i += 4
                    elif t == "&#44;":
                        key += ','
                        i += 4
                    else:
                        key += cqstr[i]
                else:
                    key += cqstr[i]
            elif stat == 3:
                if cur_ch == ']':
                    node = {}
                    cqcode[key] = val
                    node["type"] = type_
                    node["data"] = cqcode
                    jsonarr.append(node)
                    key = ""
                    val = ""
                    type_ = ""
                    cqcode = {}
                    stat = 0
                elif cur_ch == ',':
                    cqcode[key] = val
                    key = ""
                    val = ""
                    stat = 2
                elif cur_ch == '&':
                    t = ""
                    if i + 5 > len(cqstr):
                        t = ""
                    else:
                        t = cqstr[i : i+5]
                    if t == "&#91;":
                        val += '['
                        i += 4
                    elif t == "&#93;":
                        val += ']'
                        i += 4
                    elif t == "&amp;":
                        val += '&'
                        i += 4
                    elif t == "&#44;":
                        val += ','
                        i += 4
                    else:
                        val += cqstr[i]
                else:
                    val += cqstr[i]
            i += 1
        if len(text) != 0:
            node = {}
            node["type"] = "text"
            node["data"] = {"text": text}
            jsonarr.append(node)
        return jsonarr
                
