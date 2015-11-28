from django.http.response import JsonResponse, HttpResponseRedirect
from urllib.parse import urljoin
import re


class 轉址佮設定資料:
    全部模式 = {'轉址'}

    def __init__(self):
        self.模式 = None
        self.網域 = None

    def process_request(self, request):
        中介模式 = self.判斷是毋是設定中介模式(request)
        if 中介模式:
            return 中介模式
        if self.模式 == '轉址':
            return HttpResponseRedirect(urljoin(self.網域, request.path))

    def 判斷是毋是設定中介模式(self, request):
        try:
            模式 = request.POST['模式']
            if 模式 in '轉址':
                網域 = request.POST['網域']
                協定, 單純網域 = re.match(r'(http://|https://)(.+)', 網域).group(1, 2)
                最後網域 = 協定 + 單純網域.encode('idna').decode('utf-8')
                self.模式 = 模式
                self.網域 = 最後網域
                return JsonResponse({'結果': '成功'})
        except:
            pass
