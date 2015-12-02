from http import client
import json
import re
from urllib.parse import urlencode, quote

from django.http.response import JsonResponse, HttpResponse


class 轉址佮設定資料:
    全部模式 = {'轉址'}

    def __init__(self):
        self.模式 = None
        self.連線 = None

    def process_request(self, request):
        中介模式 = self.判斷是毋是設定中介模式(request)
        if 中介模式:
            return 中介模式
        if self.模式 == '轉址':
            路徑 = quote(request.path)
            if request.method == 'POST':
                self.連線.request(
                    request.method,
                    路徑,
                    json.dumps(request.POST).encode(encoding='utf_8')
                )
            else:
                if len(request.GET) > 0:
                    路徑 = 路徑 + '?' + urlencode(request.GET)
                self.連線.request(
                    request.method,
                    路徑
                )
            回應 = self.連線.getresponse()
            return HttpResponse(回應.read())

    def 判斷是毋是設定中介模式(self, request):
        try:
            模式 = request.POST['模式']
            if 模式 == '轉址':
                網域 = request.POST['網域']
                協定, 單純網域 = re.match(r'(http://|https://)(.+)', 網域).group(1, 2)
                if 協定 == 'http://':
                    連線 = client.HTTPConnection
                else:
                    連線 = client.HTTPSConnection
                self.模式 = 模式
                self.連線 = 連線(單純網域.encode('idna').decode('utf-8'))
                return JsonResponse({'結果': '成功'})
        except:
            pass
