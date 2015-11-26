#encoding:utf-8
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests, re

class SendRequest(object):
    '''封装发送http请求
        SendRequest.do_request(url) 
    '''

    @staticmethod
    def do_request(url=None, headers=None, proxys=None, timeout=10, auto_decode=False, unzip=False, retry=3, is_pic=False):
        '''请求发送http，可用于请求图片。
            默认请求时出异常时会重试2次，也就是一共会请求3次
            params：
                url (str): 请求地址
                headers (dict): 请求header
                proxys (dict): 请求代理
                timeout (int): 超时时间秒
                auto_decode (bool): http页面是否需要解码
                unzip (bool): 是否需要解压
                is_pic (bool): 请求的是否是图片，如果是True，则会返回r.content，False返回r.text。区别在于，text会自动转码，content是原封不动的数据流 
            return:
                请求成功返回html源码，请求失败返回false
        '''
        if not url: return {'status': 0, 'msg': 'url empty'}

        #请求retry次数
        for i in range(retry):
            try:
                if i != 0:
                    print 'SendRequest do', i+1,
                resp = requests.get(url, headers=headers, proxies=proxys, timeout=timeout)
            except Exception, e:
                print 'SendRequest HTTP ERROR', e,
                if i == retry-1:
                    return {'status': 0, 'msg': str(e)}
                else:
                    continue
            else:
                break

        try:
            if is_pic:
                html = resp.content
            else:
                html = resp.text
        except:
            print 'SendRequest Read Content Error',
            return {'status': 0, 'msg': 'response error'}


        #如果不是图片，且需要处理特殊字符时，替换一下特殊字符
        if not is_pic and auto_decode:
            html = html.replace(r"\"", "\"")


        return {'status': 1, 'html': html}

if __name__ == '__main__':
    html = SendRequest.do_request('https://item.taobao.com/item.htm?id=17062191585', auto_decode=False, unzip=False)
    # html = SendRequest.do_request('https://gd4.alicdn.com/imgextra/i4/109398470/TB2U48vaXXXXXauXXXXXXXXXXXX_!!109398470.jpg', auto_decode=False, is_pic=True, unzip=False)
    # print html
    with open('/Users/lisong/Desktop/ds.html', 'wb') as f:
        f.write(html['html'])



