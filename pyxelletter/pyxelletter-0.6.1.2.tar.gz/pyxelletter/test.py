from pprint import pprint
from datetime import datetime


from pyxelletter import Pyxelletter
if __name__ == '__main__':
    p = Pyxelletter('mseibert@seibert-media.net','Vxj6jjvssp7JUTg')

    print p.send_letter([open('Testbrief.pdf')],test_environment=True)