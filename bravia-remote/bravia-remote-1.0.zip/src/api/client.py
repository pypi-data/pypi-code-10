import json
import requests


def do_req(path, data):
    enc_data = json.dumps(data)
    req = requests.request('POST', 'http://192.168.1.34/sony/%s/' % path,
                          data=enc_data)
    return req

def do_ircc(data):
    sony_xml = \
"""<?xml version="1.0"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1">
      <IRCCCode>%s</IRCCCode>
    </u:X_SendIRCC>
  </s:Body>
</s:Envelope>"""
    req = requests.request('POST', 'http://192.168.1.34/sony/IRCC/',
                           headers={'SOAPAction': "urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"},
                           data=sony_xml % data)
    return req


if __name__ == '__main__':

    a = json.loads('{"id":10,"result":[{"bundled":true,"type":"RM-J1100"},[{"name":"PowerOff","value":"AAAAAQAAAAEAAAAvAw=="},{"name":"Input","value":"AAAAAQAAAAEAAAAlAw=="},{"name":"GGuide","value":"AAAAAQAAAAEAAAAOAw=="},{"name":"EPG","value":"AAAAAgAAAKQAAABbAw=="},{"name":"Favorites","value":"AAAAAgAAAHcAAAB2Aw=="},{"name":"Display","value":"AAAAAQAAAAEAAAA6Aw=="},{"name":"Home","value":"AAAAAQAAAAEAAABgAw=="},{"name":"Options","value":"AAAAAgAAAJcAAAA2Aw=="},{"name":"Return","value":"AAAAAgAAAJcAAAAjAw=="},{"name":"Up","value":"AAAAAQAAAAEAAAB0Aw=="},{"name":"Down","value":"AAAAAQAAAAEAAAB1Aw=="},{"name":"Right","value":"AAAAAQAAAAEAAAAzAw=="},{"name":"Left","value":"AAAAAQAAAAEAAAA0Aw=="},{"name":"Confirm","value":"AAAAAQAAAAEAAABlAw=="},{"name":"Red","value":"AAAAAgAAAJcAAAAlAw=="},{"name":"Green","value":"AAAAAgAAAJcAAAAmAw=="},{"name":"Yellow","value":"AAAAAgAAAJcAAAAnAw=="},{"name":"Blue","value":"AAAAAgAAAJcAAAAkAw=="},{"name":"Num1","value":"AAAAAQAAAAEAAAAAAw=="},{"name":"Num2","value":"AAAAAQAAAAEAAAABAw=="},{"name":"Num3","value":"AAAAAQAAAAEAAAACAw=="},{"name":"Num4","value":"AAAAAQAAAAEAAAADAw=="},{"name":"Num5","value":"AAAAAQAAAAEAAAAEAw=="},{"name":"Num6","value":"AAAAAQAAAAEAAAAFAw=="},{"name":"Num7","value":"AAAAAQAAAAEAAAAGAw=="},{"name":"Num8","value":"AAAAAQAAAAEAAAAHAw=="},{"name":"Num9","value":"AAAAAQAAAAEAAAAIAw=="},{"name":"Num0","value":"AAAAAQAAAAEAAAAJAw=="},{"name":"Num11","value":"AAAAAQAAAAEAAAAKAw=="},{"name":"Num12","value":"AAAAAQAAAAEAAAALAw=="},{"name":"VolumeUp","value":"AAAAAQAAAAEAAAASAw=="},{"name":"VolumeDown","value":"AAAAAQAAAAEAAAATAw=="},{"name":"Mute","value":"AAAAAQAAAAEAAAAUAw=="},{"name":"ChannelUp","value":"AAAAAQAAAAEAAAAQAw=="},{"name":"ChannelDown","value":"AAAAAQAAAAEAAAARAw=="},{"name":"SubTitle","value":"AAAAAgAAAJcAAAAoAw=="},{"name":"ClosedCaption","value":"AAAAAgAAAKQAAAAQAw=="},{"name":"Enter","value":"AAAAAQAAAAEAAAALAw=="},{"name":"DOT","value":"AAAAAgAAAJcAAAAdAw=="},{"name":"Analog","value":"AAAAAgAAAHcAAAANAw=="},{"name":"Teletext","value":"AAAAAQAAAAEAAAA/Aw=="},{"name":"Exit","value":"AAAAAQAAAAEAAABjAw=="},{"name":"Analog2","value":"AAAAAQAAAAEAAAA4Aw=="},{"name":"*AD","value":"AAAAAgAAABoAAAA7Aw=="},{"name":"Digital","value":"AAAAAgAAAJcAAAAyAw=="},{"name":"Analog?","value":"AAAAAgAAAJcAAAAuAw=="},{"name":"BS","value":"AAAAAgAAAJcAAAAsAw=="},{"name":"CS","value":"AAAAAgAAAJcAAAArAw=="},{"name":"BSCS","value":"AAAAAgAAAJcAAAAQAw=="},{"name":"Ddata","value":"AAAAAgAAAJcAAAAVAw=="},{"name":"PicOff","value":"AAAAAQAAAAEAAAA+Aw=="},{"name":"Tv_Radio","value":"AAAAAgAAABoAAABXAw=="},{"name":"Theater","value":"AAAAAgAAAHcAAABgAw=="},{"name":"SEN","value":"AAAAAgAAABoAAAB9Aw=="},{"name":"InternetWidgets","value":"AAAAAgAAABoAAAB6Aw=="},{"name":"InternetVideo","value":"AAAAAgAAABoAAAB5Aw=="},{"name":"Netflix","value":"AAAAAgAAABoAAAB8Aw=="},{"name":"SceneSelect","value":"AAAAAgAAABoAAAB4Aw=="},{"name":"Mode3D","value":"AAAAAgAAAHcAAABNAw=="},{"name":"iManual","value":"AAAAAgAAABoAAAB7Aw=="},{"name":"Audio","value":"AAAAAQAAAAEAAAAXAw=="},{"name":"Wide","value":"AAAAAgAAAKQAAAA9Aw=="},{"name":"Jump","value":"AAAAAQAAAAEAAAA7Aw=="},{"name":"PAP","value":"AAAAAgAAAKQAAAB3Aw=="},{"name":"MyEPG","value":"AAAAAgAAAHcAAABrAw=="},{"name":"ProgramDescription","value":"AAAAAgAAAJcAAAAWAw=="},{"name":"WriteChapter","value":"AAAAAgAAAHcAAABsAw=="},{"name":"TrackID","value":"AAAAAgAAABoAAAB+Aw=="},{"name":"TenKey","value":"AAAAAgAAAJcAAAAMAw=="},{"name":"AppliCast","value":"AAAAAgAAABoAAABvAw=="},{"name":"acTVila","value":"AAAAAgAAABoAAAByAw=="},{"name":"DeleteVideo","value":"AAAAAgAAAHcAAAAfAw=="},{"name":"PhotoFrame","value":"AAAAAgAAABoAAABVAw=="},{"name":"TvPause","value":"AAAAAgAAABoAAABnAw=="},{"name":"KeyPad","value":"AAAAAgAAABoAAAB1Aw=="},{"name":"Media","value":"AAAAAgAAAJcAAAA4Aw=="},{"name":"SyncMenu","value":"AAAAAgAAABoAAABYAw=="},{"name":"Forward","value":"AAAAAgAAAJcAAAAcAw=="},{"name":"Play","value":"AAAAAgAAAJcAAAAaAw=="},{"name":"Rewind","value":"AAAAAgAAAJcAAAAbAw=="},{"name":"Prev","value":"AAAAAgAAAJcAAAA8Aw=="},{"name":"Stop","value":"AAAAAgAAAJcAAAAYAw=="},{"name":"Next","value":"AAAAAgAAAJcAAAA9Aw=="},{"name":"Rec","value":"AAAAAgAAAJcAAAAgAw=="},{"name":"Pause","value":"AAAAAgAAAJcAAAAZAw=="},{"name":"Eject","value":"AAAAAgAAAJcAAABIAw=="},{"name":"FlashPlus","value":"AAAAAgAAAJcAAAB4Aw=="},{"name":"FlashMinus","value":"AAAAAgAAAJcAAAB5Aw=="},{"name":"TopMenu","value":"AAAAAgAAABoAAABgAw=="},{"name":"PopUpMenu","value":"AAAAAgAAABoAAABhAw=="},{"name":"RakurakuStart","value":"AAAAAgAAAHcAAABqAw=="},{"name":"OneTouchTimeRec","value":"AAAAAgAAABoAAABkAw=="},{"name":"OneTouchView","value":"AAAAAgAAABoAAABlAw=="},{"name":"OneTouchRec","value":"AAAAAgAAABoAAABiAw=="},{"name":"OneTouchStop","value":"AAAAAgAAABoAAABjAw=="}]]}')

    test_code = 'AAAAA'
    do_ircc('AAAAAQAAAAEAAAAQAw==')
    #req = requests.request('GET', 'http://192.168.1.34/register?name=VirtualRemote_00237db81833&registrationType=initial&deviceId=TVSideView%3A00-23-7d-b8-18-33')

    #                        params=sony_xml % test_code)

    info_data = {"method":"getRemoteControllerInfo","params":[],"id":10, "version":"1.0"}
    do_req('system', info_data)
    # req = requests.request('POST', 'http://192.168.1.34/sony/system',
    #                        headers={'Content-Type': 'text/xml',
    #                                 'SOAPAction': "urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"},
    #                        params=info_data)

    acc_list = json.dumps({"id":13,"method":"actRegister","version":"1.0","params":[{"clientid":"iRule:1","nickname":"iRule"},[{"clientid":"iRule:1","value":"yes","nickname":"iRule","function":"WOL"}]]})
    do_req('accessControl', acc_list)
    # req = requests.request('POST', 'http://192.168.1.34/sony/system/',
    #                        params={"id":1,"method":"getVersions","version":"1.0","params":[]})

    print(req)