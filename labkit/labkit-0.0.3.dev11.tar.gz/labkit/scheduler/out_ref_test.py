#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry



from push_task_file import rq_gaussian
from labkit.conformer.base_conformer import Conformer




def test():
    coll=Conformer.get_coll('tmp','tmp')
    conformer=coll.Conformer()
    # conformer.collection=get_coll('tmp','ttmp')
    # conformer.set_coll('ttmp','tttmp')
    conformer.load(filename='/Users/lhr/lhrkits/labkit/test/cggg1.xyz')
    # cc=gaussian_conformer(conformer)
    # result = q.enqueue(count_words_at_url, "www.baidu.com")

    # cc.save()


    cc=pep_from_seq('CGGGG')

    rq_gaussian(cc)

if __name__=='__main__':
    test()

