# coding: utf8

import threading
import subprocess
import operator

from consts import YUNTI_VPNS as vpns

ping_vpns = []

class MyThread(threading.Thread) :

    def __init__(self, vpn) :
        super(MyThread, self).__init__()
        self.vpn = vpn

    def run(self) :
        cmd = "ping -c5 -t1 %s" % (self.vpn[0])
        try:
            result = subprocess.check_output(cmd, shell=True)
        except Exception, e:
            return
        ns = result.split("\n")
        re = [0, 0, '']
        for n in ns:
            if 'packet loss' in n:
                re[0] = float(n.split("% ")[0].split(",")[-1].strip())
            if ' = ' in n:
                re[1] = float(n.split(" = ")[-1].split("/")[2].strip())
            if 'ping statistics' in n:
                re[2] = n.split(" ping")[0].strip()[4:]
                re.append(self.vpn[1])

        ping_vpns.append(re)

def test_run():
    threads = []
    for vpn in vpns:
        thread = MyThread(vpn)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    res = sorted(ping_vpns, key=operator.itemgetter(0, 1))

    headers = ['Packet loss', 'TTL', 'VPN server', 'Name']

    row_format = u"{:<0}{:<13}{:<15}{:<20}{:<10}"
    print row_format.format(u"", *headers)
    row_format = u"{:<0}{:<13}{:<15}{:<20}{:<10}"
    for re in res[:5]:
        re[1] = "{0:.2f}".format(re[1])
        print row_format.format(u"", *re)

if __name__ == "__main__":
    test_run()
