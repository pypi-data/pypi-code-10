# coding: utf-8
import urllib2
import re
import random
import os

urls = [
    "http://referats.yandex.ru/astronomy.xml",
    "http://referats.yandex.ru/geology.xml",
    "http://referats.yandex.ru/gyroscope.xml",
    "http://referats.yandex.ru/marketing.xml",
    "http://referats.yandex.ru/mathematics.xml",
    "http://referats.yandex.ru/polit.xml",
    "http://referats.yandex.ru/agrobiologia.xml",
    "http://referats.yandex.ru/law.xml",
    "http://referats.yandex.ru/psychology.xml",
    "http://referats.yandex.ru/physics.xml",
    "http://referats.yandex.ru/geography.xml",
    "http://referats.yandex.ru/philosophy.xml",
    "http://referats.yandex.ru/estetica.xml",
    "http://referats.yandex.ru/chemistry.xml",
]

fp_p = open(os.path.join(os.path.dirname(__file__), 'result', 'result/paragraphs.txt'), 'a+')
fp_s = open(os.path.join(os.path.dirname(__file__), 'result', 'result/subjects.txt'), 'a+')


def make():
    try:
        url = random.choice(urls)
        re_main_search = re.compile(ur'color:black; margin-left:0;"\>([^\<]+)\<\/h1\>\s*\<p\>(.*?)\<\/div\>', re.MULTILINE | re.DOTALL | re.UNICODE)
        re_replace_linebreaks = re.compile(r"[\n\t\r]", re.MULTILINE | re.DOTALL | re.UNICODE)
        re_split_p = re.compile(r"<p>(.*?)</p>", re.MULTILINE | re.DOTALL | re.UNICODE)
        r = urllib2.urlopen(url)
        cnt = r.read()

        r = re.search(re_main_search, cnt)
        title = r.group(1).decode("utf-8")[7:-1].encode("utf-8")
        text = "<p>" + re.sub(re_replace_linebreaks, "", r.group(2))

        for t in re.finditer(re_split_p, text):
            fp_p.write(t.group(1) + "\n")

        fp_s.write(title + "\n")
    except:
        print 'err'
        return

