# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import json

import requests

from ebcloudstore.util import is_cn_char, cn2char


class EbStore(object):
    def __init__(self, token):
        self.token = token
        self.code = None
        self.file_type = None
        self.ip_list = None
        self.get_code()
        pass

    def get_code(self):
        url = "http://cloud.53iq.com/api/auth"
        r = requests.get(url=url, params={"token": self.token}, timeout=5)
        ret = json.loads(r.text)
        if ret["code"] == 0:
            self.code = ret["data"]["code"]
            self.file_type = ret["data"]["file_type"]
            self.ip_list = ret["data"]["ip_list"]
            pass
        else:
            raise Exception(ret["msg"])

    def upload(self, file_stream, filename=None, file_type=None):
        """
        普通文件上传
        :param file_stream:
        :param filename:
        :param file_type:
        :return:
        """
        url = "http://cloud.53iq.com/api/file"

        if filename is None:
            filename = "untitled"

        # 解决文件名中文无法上传问题
        elif is_cn_char(filename):
            filename = cn2char(filename)
            pass
        if file_type is None:
            file_type = "application/octet-stream"
        # 判断文件类型是否允许上传
        # 文件大小限制判断
        # 上传后续动作的处理
        files = {'file': (filename, file_stream, file_type)}
        data = {"code": self.code}
        r = requests.post(url=url, files=files, data=data)
        return r.text

    def upload_img(self):
        pass


if __name__ == "__main__":
    a = open("/home/tsengdavid/Pictures/3-140311095F9.jpg", "rb")
    store = EbStore("562e18936f43f6597cecb9d3")
    rs = store.upload(a, "hello.jpg", "image/jpeg")
    print(rs)