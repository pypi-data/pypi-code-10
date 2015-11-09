# coding=u8
# Copyright 2014-2015 Secken, Inc.  All Rights Reserved.
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
#
# NOTICE:  All information contained herein is, and remains
# the property of Secken, Inc. and its suppliers, if any.
# The intellectual and technical concepts contained
# herein are proprietary to Secken, Inc. and its suppliers
# and may be covered by China and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Secken, Inc..
#
# 注意：此处包含的所有信息，均属于Secken, Inc.及其供应商的私有财产。
# 此处包含的所有知识、专利均属于Secken, Inc.及其供应商，属于商业秘密，
# 并受到中国和其他国家的法律保护。这些信息及本声明，除非事先得到
# Secken, Inc.的书面授权，否则严禁复制或传播。
#
# @author     xupengjie (pengjiexu@secken.com)
# @version    1.169.6
#

import time
import struct
from uuid import uuid1

MAGIC = "ATPP"


class FactoryException(Exception):

    NONE_EXCEPTION = 0
    IS_NOT_ATPPFACTORY = 1

    def __init__(self, type):
        if type == FactoryException.NONE_EXCEPTION:
            super(Exception, self).__init__("factory must not None!")
        elif type == FactoryException.IS_NOT_ATPPFACTORY:
            super(Exception, self).__init__("factory must be AtppFactory!")
        else:
            super(Exception, self).__init__(
                "unkow exception from FactoryException type : %d!", type)


class DataException(Exception):

    HAS_DATA_BUT_DO_NOT_HAVE_TOKEN = 0
    CAN_NOT_DECODE_DATA = 1
    NOT_ATPP_PROTOCOL = 2
    BROKE_DATA = 3

    def __init__(self, type):
        if type == DataException.HAS_DATA_BUT_DO_NOT_HAVE_TOKEN:
            super(Exception, self).__init__(
                "broke data cause can't find handshake package!")
        elif type == DataException.CAN_NOT_DECODE_DATA:
            super(Exception, self).__init__("can't unpack data!")
        elif type == DataException.NOT_ATPP_PROTOCOL:
            super(Exception, self).__init__("data isn't atpp protocol!")
        elif type == DataException.BROKE_DATA:
            super(Exception, self).__init__("broke data!")
        else:
            super(Exception, self).__init__(
                "unkow exception from DataException type : %d!", type)


class AtppStartPackage(object):

    TYPE = 1

    def __init__(self, timestamp, total_size, slice_count, slice_pre_size):
        self.type = 1
        self.slice_count = slice_count
        self.slice_pre_size = slice_pre_size
        self.total_size = total_size
        self.timestamp = timestamp

    def pack(self, token):
        return struct.pack("!%dsBQ32sQii" % len(MAGIC), MAGIC, self.type, self.timestamp, token, self.total_size, self.slice_count, self.slice_pre_size)


class AtppDataPackage(object):

    TYPE = 2

    def __init__(self, timestamp, slice_index, slice_size, data):
        self.type = 2
        self.data = data
        self.slice_index = slice_index
        self.slice_size = slice_size
        self.timestamp = timestamp

    def pack(self, token):
        return struct.pack("!%dsBQ32sii%ds" % (len(MAGIC), len(self.data)), MAGIC, self.type, self.timestamp, token, self.slice_index, self.slice_size, self.data)


class AtppEndPackage(object):

    TYPE = 3

    def __init__(self, timestamp):
        self.type = 3
        self.timestamp = timestamp

    def pack(self, token):
        return struct.pack("!%dsBQ32s" % len(MAGIC), MAGIC, self.type, self.timestamp, token)


class AtppProtocol(object):

    def __init__(self, factory=None):
        self.factory = factory
        self.last_package = None
        self.head_length = 45

    def __append_last_package__(self, recv):
        if self.last_package:
            self.last_package = self.last_package + recv
        else:
            self.last_package = recv

    def recv_data(self, data):
        if data:
            if self.last_package:
                data = self.last_package + data
                self.last_package = None

            size = len(data)
            offset = 0
            while 1:
                # 取4位
                magic = None
                if size - offset >= self.head_length:
                    try:
                        magic, type, timestamp, token = struct.unpack(
                            "!%dsBQ32s" % len(MAGIC), data[offset:offset + self.head_length])
                    except:
                        raise DataException(DataException.BROKE_DATA)
                    offset += self.head_length

                    if magic == MAGIC:
                        # read type
                        if type == AtppStartPackage.TYPE:
                            if size - offset >= 16:
                                package_total_size = None
                                slice_count = None
                                slice_pre_size = None
                                try:
                                    package_total_size, slice_count, slice_pre_size = struct.unpack(
                                        "!Qii", data[offset:offset + 16])
                                    offset += 16
                                except:
                                    raise DataException(
                                        DataException.BROKE_DATA)
                                if package_total_size and slice_count and slice_pre_size:
                                    package = AtppStartPackage(
                                        timestamp, package_total_size, slice_count, slice_pre_size)
                                    self.factory.on_start(token, package)
                            else:
                                self.last_package = data[
                                    offset - self.head_length:]
                                break
                        elif type == AtppDataPackage.TYPE:
                            if size - offset >= 8:
                                slice_index = None
                                slice_size = None
                                try:
                                    slice_index, slice_size = struct.unpack(
                                        "!ii", data[offset:offset + 8])
                                    offset += 8
                                except:
                                    raise DataException(
                                        DataException.BROKE_DATA)
                                if slice_index and slice_size:
                                    if slice_size <= len(data[offset:]):
                                        slice_data = data[
                                            offset:offset + slice_size]
                                        package = AtppDataPackage(
                                            timestamp, slice_index, slice_size, slice_data)
                                        offset += slice_size
                                        self.factory.on_data(token, package)
                                    else:
                                        self.last_package = data[
                                            offset - self.head_length - 8:]
                                        break
                            else:
                                self.last_package = data[
                                    offset - self.head_length:]
                                break

                        elif type == AtppEndPackage.TYPE:
                            pkg = AtppEndPackage(timestamp)
                            self.factory.on_end(token, pkg)
                    else:
                        raise DataException(DataException.BROKE_DATA)
                else:
                    self.last_package = data[offset:]
                    break
        else:
            # 如果接收结果为null
            raise DataException(DataException.BROKE_DATA)

    def send_data(self, data, slice_size, token=None):
        if data:
            if slice_size > 0:
                if not token:
                    token = self.get_token()

                data_length = len(data)
                slice_count = (data_length + (slice_size - 1)) / slice_size
                # 数据定下后 生成起始包
                start_pack = AtppStartPackage(
                    int(time.time() * 1000),
                    data_length,
                    slice_count,
                    slice_size)
                yield start_pack.pack(token)
                offset = 0
                for x in xrange(slice_count):
                    data_pack = None
                    if offset + slice_size > data_length:
                        data_pack = AtppDataPackage(
                            int(time.time() * 1000),
                            x + 1,
                            data_length - offset,
                            data[offset:])
                    else:
                        data_pack = AtppDataPackage(
                            int(time.time() * 1000),
                            x + 1,
                            slice_size,
                            data[offset:offset + slice_size])
                        offset = offset + slice_size
                    yield data_pack.pack(token)
                end_pack = AtppEndPackage(
                    int(time.time() * 1000)
                )
                yield end_pack.pack(token)
            else:
                # 分片大小小于等于0处理
                yield None
        else:
            # 数据为空处理
            yield None

    def get_token(self):
        return str(uuid1()).replace('-', '')

    def get_start_package(self, data_length, slice_size):
        slice_count = (data_length + (slice_size - 1)) / slice_size
        # 数据定下后 生成起始包
        return AtppStartPackage(
            int(time.time() * 1000),
            data_length,
            slice_count,
            slice_size)

    def get_data_package(self, package_index, slice_size, data):
        return AtppDataPackage(
            int(time.time() * 1000),
            package_index,
            slice_size,
            data)

    def get_end_package(self):
        return AtppEndPackage(
            int(time.time() * 1000)
        )


class AtppFactory(object):

    # def __init__(self, protocol):
    #     self.protocol = protocol

    def on_data(self, token, package):
        pass

    def on_start(self, token, package):
        pass

    def on_end(self, token, packages):
        pass
