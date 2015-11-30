from pprint import pprint
from .kwick import Kwick
from .kwick import KwickError
import time

kwick = Kwick()
kwick.mobile_host = 'https://kwick.de'

try:
    kwick.kwick_login('epicmuffin', '14041987xanth!?!')
except Exception as m:
    pprint(m)

visited = []

while True:
    kwick.mobile_host = 'http://m.kwick.de'
    community = kwick.kwick_index(page=0, community=True)

    for obj in community['socialstream']:

        objectid = obj['socialObjectId']
        objecttype = obj['socialObjectType']
        gender = obj['vcard']['sex']

        uid = obj['from_id']
        user_name = obj['from_name']

        pprint(objecttype)
        if objecttype == 'Profile_Change_Registration':
            pprint(kwick.kwick_like(objecttype, objectid))

        """
        if objectid not in visited and gender == 1:
            kwick.mobile_host = 'https://kwick.de'
            print(user_name)
            kwick.kwick_user(username=user_name + '/portrait', json=True)
        """
        visited.append(objectid)

    time.sleep(10)
