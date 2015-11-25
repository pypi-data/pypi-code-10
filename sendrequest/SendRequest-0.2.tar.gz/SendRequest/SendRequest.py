#encoding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2, re

class SendRequest(object):
    '''封装发送请求'''

    @staticmethod
    def do_request(url=None, headers=None, proxys=None, timeout=10, auto_decode=False, unzip=False, retry=3):
        '''请求发送http，可用于请求图片。
            默认会请求时出异常会重试2次，一共请求3次
            params：
                url (str): 请求地址
                headers (dict): 请求header
                proxys (dict): 请求代理
                timeout (int): 超时时间秒
                auto_decode (bool): http页面是否需要解码
                unzip (bool): 是否需要解压
            return:
                请求成功返回html源码，请求失败返回false
        '''
        if not url: return {'status': 0, 'msg': 'url empty'}

        if proxys: 
            proxy_support = urllib2.ProxyHandler({"http" : "http://%s:%s" % proxys})
            opener = urllib2.build_opener(proxy_support)
        else:
            opener = urllib2.build_opener()

        if headers: opener.addheaders = headers.items()

        #请求retry次数
        for i in range(retry):
            try:
                if i != 0:
                    print 'SendRequest do', i+1,
                resp = opener.open(url, timeout=timeout)
            except Exception, e:
                print 'SendRequest HTTP ERROR', e,
                if i == retry-1:
                    return {'status': 0, 'msg': str(e)}
                else:
                    continue
            else:
                break

        try:
            html = resp.read()
        except:
            print 'SendRequest Read Content Error',
            return {'status': 0, 'msg': 'response error'}


        #检测是否需要解压
        if unzip:
            import StringIO, gzip
            compresseddata = html
            compressedstream = StringIO.StringIO(compresseddata)
            gzipper = gzip.GzipFile(fileobj=compressedstream)
            data = gzipper.read()
            html = data


        #检测html编码
        if auto_decode:
            charset_reg_result = re.findall(r"<meta.*?charset=(.*?)/?>", html)
            html_charset = ''
            if charset_reg_result:
                html_charset = charset_reg_result.pop().lower()
       
            if html_charset and 'gbk' in html_charset:
                # print 'Decode gbk To UTF8',
                try:
                    html = html.decode('gbk', 'ignore').encode('utf-8')
                except Exception, e:
                    print 'SendRequest Decode ERROR', e,

            html = html.replace(r"\"", "\"")

        return {'status': 1, 'html': html}

if __name__ == '__main__':
    html = SendRequest.do_request('http://item.taobao.com/item.htm?id=17062191582', auto_decode=False, unzip=False)
    print html



