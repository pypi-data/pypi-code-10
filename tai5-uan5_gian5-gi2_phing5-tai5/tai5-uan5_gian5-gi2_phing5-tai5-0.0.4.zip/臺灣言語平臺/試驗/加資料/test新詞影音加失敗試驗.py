# -*- coding: utf-8 -*-
from unittest.mock import patch
from 臺灣言語平臺.試驗.加資料.試驗基本資料 import 試驗基本資料
from 臺灣言語資料庫.資料模型 import 影音表
import io
import wave
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.關係模型 import 翻譯影音表
import json
from 臺灣言語平臺.項目模型 import 平臺項目表
from django.contrib.auth.models import AnonymousUser


class 新詞影音加失敗試驗(試驗基本資料):

    def setUp(self):
        super(新詞影音加失敗試驗, self).setUp()

        self.登入使用者編號patcher = patch('臺灣言語平臺.使用者模型.使用者表.判斷編號')
        self.登入使用者編號mock = self.登入使用者編號patcher.start()
        self.登入使用者編號mock.return_value = self.鄉民.編號()

        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
                        '外語語言': '華語',
                        '外語資料': '漂亮',
            }
        )
        外語回應資料 = json.loads(外語回應.content.decode("utf-8"))
        self.外語項目編號 = int(外語回應資料['平臺項目編號'])
        self.外語 = 平臺項目表.objects.get(pk=self.外語項目編號).外語

        self.檔案 = io.BytesIO()
        with wave.open(self.檔案, 'wb') as 音檔:
            音檔.setnchannels(1)
            音檔.setframerate(16000)
            音檔.setsampwidth(2)
            音檔.writeframesraw(b'sui2' * 20)
        self.檔案.seek(0)
        self.檔案.name = '試驗音檔'

        self.外語表資料數 = 外語表.objects.all().count()
        self.影音表資料數 = 影音表.objects.all().count()
        self.翻譯影音表資料數 = 翻譯影音表.objects.all().count()
        self.平臺項目表資料數 = 平臺項目表.objects.all().count()

    def tearDown(self):
        # 		後端資料庫檢查不增加資料
        self.assertEqual(外語表.objects.all().count(), self.外語表資料數)
        self.assertEqual(影音表.objects.all().count(), self.影音表資料數)
        self.assertEqual(翻譯影音表.objects.all().count(), self.翻譯影音表資料數)
        self.assertEqual(平臺項目表.objects.all().count(), self.平臺項目表資料數)
        self.登入使用者編號patcher.stop()

    def test_無登入(self):
        self.登入使用者編號mock.return_value = None
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '來源': json.dumps({'名': '自己'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                        '影音資料': self.檔案,
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '無登入',
        })
# 		邏輯檢查
        self.登入使用者編號mock.assert_called_with(AnonymousUser())  # 外語有叫過

    def test_缺編號欄位(self):
        '編號欄位跟其他欄位一樣，缺了會失敗'
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                # 				'外語項目編號':self.外語項目編號,
                '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                        '影音資料': self.檔案,
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '資料欄位有缺',
        })

    def test_編號欄位無佇資料庫(self):
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': '2016',
                '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                        '影音資料': self.檔案,
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '編號號碼有問題',
        })

    def test_編號欄位毋是數字(self):
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': 'self.外語項目編號',
                '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                        '影音資料': self.檔案,
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '編號欄位不是數字字串',
        })

    def test_來源無轉json字串(self):
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '來源': {'名': '自己'},
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                        '影音資料': self.檔案,
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '來源抑是屬性無轉json字串',
        })

    def test_屬性無轉json字串(self):
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '來源': json.dumps({'名': '自己'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': {'詞性': '形容詞', '字數': '1'},
                        '影音資料': self.檔案,
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '來源抑是屬性無轉json字串',
        })

    def test_缺資料欄位(self):
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '來源': {'名': '自己'},
                '種類': '字詞',
                '語言腔口': '閩南語',
                # 				'著作所在地':'花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                        '影音資料': self.檔案,
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '資料欄位有缺',
        })

    def test_來源沒有名的欄位(self):
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '來源': json.dumps({'誰': '自己'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                        '影音資料': self.檔案,
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '來源沒有「名」的欄位',
        })

    def test_無仝的種類(self):
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
                '種類': '語句',  # 外語的種類是「字詞」
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                        '影音資料': self.檔案,
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '種類和外語不一樣',
        })

    def test_種類欄位不符規範(self):
        '若不是資料庫允許的種類，一定和外語不同，可參考`test_無仝的種類`'
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '來源': {'名': '自己'},
                '種類': '漢字',  # 「漢字」無佇資料庫
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                        '影音資料': self.檔案,
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '種類和外語不一樣',
        })

    def test_無仝的語言腔口(self):
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
                '種類': '字詞',
                '語言腔口': '噶哈巫語',  # 外語的語言腔口是「閩南語」
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                        '影音資料': self.檔案,
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '語言腔口和外語不一樣',
        })

    def test_影音資料毋是檔案(self):
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '來源': json.dumps({'名': '自己'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                        '影音資料': b'sui2',
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '影音資料不是檔案',
        })

    def test_影音資料毋是影音檔案(self):
        一般檔案 = io.BytesIO(b'sui2' * 20)
        一般檔案.seek(0)
        一般檔案.name = '試驗音檔'

        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '來源': json.dumps({'名': '自己'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                        '影音資料': 一般檔案,
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '影音資料不是影音檔案',
        })
