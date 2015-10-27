# -*- coding: utf-8 -*-
from io import BufferedReader
import json
import os

import requests

from ebcloudstore.util import is_cn_char, cn2char


class EbStore(object):
    def __init__(self, token, action="response", callback_url=None, referer=None):
        """
        init the EbStore
        :param token:
        :param action: response|callback|redirect
        :param callback_url:when the action is callback,this params is must
        :param referer:
        :return:
        """
        self.token = token
        self.code = None
        self.file_type = None
        self.ip_list = None
        self.disk = None
        self.action = action
        self.callback_url = callback_url
        self.referer = referer
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
            self.disk = int(ret["data"]["disk"])
            pass
        else:
            raise Exception(ret["msg"])

    def check_ext(self, file_ext):
        ext_arr = json.loads(self.file_type.replace("'", '"'))
        if "*" in ext_arr:
            return True
        for i in ext_arr:
            if i.lower() == file_ext.lower():
                return True
        return False

    def check_size(self, file_size):
        size = self.disk * 1024
        if size > file_size:
            return True
        else:
            return False
        pass

    def check_ip(self, ip):
        ip_arr = json.loads(self.ip_list.replace("'", '"'))
        if "*" in ip_arr:
            return True
        for i in ip_arr:
            if i.lower() == ip.lower():
                return True
        return False

    def upload(self, args, filename=None, file_type=None):
        """
        upload file
        todo:check size
        todo:check ip
        :param args: a full file path or file bytes
        :param filename:
        :param file_type:
        :return:
        """
        if isinstance(args, str):
            if os.path.isfile(args):
                ext_split = os.path.splitext(args)
                if len(ext_split) >= 2 and self.check_ext(ext_split[1][1:]):

                    files = {'file': open(args, "rb")}
                else:
                    raise Exception("file extension not supported")
            else:
                raise Exception("args not file path")
        elif isinstance(args, BufferedReader) or isinstance(args, bytes):
            if filename is None:
                filename = "untitled"
            else:
                ext_split = os.path.splitext(filename)
                if len(ext_split) >= 2 and self.check_ext(ext_split[1][1:]):
                    if is_cn_char(filename):
                        filename = cn2char(filename)
                else:
                    raise Exception("file extension not supported")

            if file_type is None:
                file_type = "application/octet-stream"

            files = {'file': (filename, args, file_type)}
            pass
        else:
            raise Exception("args must be string or BufferedReader or bytes! can't be %s" % (type(filename)))

        data = {"code": self.code}
        headers = None
        if self.action == "callback" and self.callback_url is not None:
            data["action"] = self.action
            data["callback_url"] = self.callback_url
        elif self.action == "redirect" and self.referer is not None:
            headers["Referer"] = self.referer
        if headers:
            r = requests.post(url="http://cloud.53iq.com/api/file", files=files, data=data, headers=headers)
        else:
            r = requests.post(url="http://cloud.53iq.com/api/file", files=files, data=data)
        return r.text

    def upload_img(self,):
        """
        todo:image upload
        :return:
        """
        pass

