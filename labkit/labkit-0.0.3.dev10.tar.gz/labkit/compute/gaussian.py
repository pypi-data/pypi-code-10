#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import sh

import  tempfile
from labkit.conformer.conformer import Conformer
import  re
from general import gs
log=gs.get_logger(__name__,debug=False)

# # from labkit.labdist import *
#
# from rq import Queue, use_connection
# use_connection()
# q = Queue()
#
# # from my_module import count_words_at_url

# def run_in_rq(func):
#     def send_to_rq(conformer,method='pm3 opt',charge=0,mutiplicity=1):
#         result = q.enqueue(func, (conformer))
#
#
#     return send_to_rq
#
import requests
import subprocess
import time

def count1():
    """Just an example function that's called async."""
    return 1

def count_words_at_url(url):
    """Just an example function that's called async."""
    resp = requests.get(url)
    time.sleep(10)
    return len(resp.text.split())

def gaussian_conformer(conformer,method='pm3 opt',charge=0,mutiplicity=1):
    try:
        new_conformer= conformer.collection.__getattr__(conformer.__class__.__name__)()
    except:
        new_conformer=Conformer()



    xyz=conformer['xyz']
    txt_file= tempfile.NamedTemporaryFile()
    out_file = tempfile.NamedTemporaryFile()
    first_line_re=re.compile(r'^.*?\n.*?\n',re.S)
    txt='#'+method+'\n\n'+'gaussian'+'\n'+first_line_re.sub('\n'+str(charge)+' '+str(mutiplicity)+'\n',xyz)
    new_conformer['from_method']=method
    txt_file.write(txt)
    txt_file.seek(0)
    sh.fake90(txt_file.name,out_file.name)

    out_file.seek(0)

    mp2_re=re.compile(r'\\MP2=(.*?)\\',re.S)
    hf_re=re.compile(r'\\HF=(.*?)\\',re.S)
    xyz_re=re.compile(r'Standard orientation:.*?\n -*\n.*? -*\n(.*?) -*\n',re.S)
    origin_text=out_file.read()
    text=origin_text.replace(' ','').replace('\n','')
    mp2_find=mp2_re.findall(text)
    hf_find=hf_re.findall(text)
    xyz_find=xyz_re.findall(origin_text)


    if xyz_find:
        xyzcontent=xyz_find.pop()

    pattern=re.compile(r'[ \t]+.+?[ \t]+(.+?)[ \t]+.+?[ \t]+(.+?)[ \t]+(.+?)[ \t]+?(.+?)\n')
    xyz=pattern.findall(xyzcontent)


    # function get_symbol(number) {
    # if(number==1) return "H";
    # else if(number==6) return "C";
    # else if(number==8) return "O";
    # else if(number==7) return "N";
    # else if(number==16) return "S";
    # else return "X";

    new=[]
    for j,i in enumerate(xyz):
        i=list(i)
        if i[0]=='1':
            i[0]='H'
        elif i[0]=='6':
            i[0]='C'
        elif i[0]=='8':
            i[0]='O'
        elif i[0]=='7':
            i[0]='N'
        elif i[0]=='16':
            i[0]='S'

        new.append(' '.join(i))
    atom_count=len(xyz)

    xyz=str(atom_count)+'\n'+'XXX\n'+'\n'.join(new)


    new_conformer['xyz']=xyz

    if mp2_find:
        hf=float(mp2_find[0])
    else:
        hf=float(hf_find[0])


    new_conformer['energy']=hf

    # out_file.seek(0)
    # sh.out2xyz(out_file.name,txt_file.name)
    # txt_file.seek(0)
    # conformer['xyz']=txt_file.read()
    # print conformer['xyz']

    # out_file.seek(0)
    # out= out_file.read()
    txt_file.close()
    out_file.close()

    # new_conformer['father']=str(conformer['_id'])

    return new_conformer


def gaussian(xyz,conf,energy_cut=3000000000,database='gaussian',collection='default',method='pm3 ',charge=0,mutiplicity=1):
# def gaussian(conf):

    # xyz=conf['xyz']
    # energy_cut=conf['energy_cut']
    # database=conf['labkit']
    # collection=conf['ensemble']
    # method=conf['method']
    # method=conf['method']
    #
    # charge=0
    # mutiplicity=1


    first_line_re=re.compile(r'^.*?\n.*?\n',re.S)
    txt='#'+method+'\n\n'+'gaussian'+'\n'+first_line_re.sub('\n'+str(charge)+' '+str(mutiplicity)+'\n',xyz)

    p=subprocess.Popen(['g09'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    output=p.communicate(input=txt)[0]

    mp2_re=re.compile(r'\\MP2=(.*?)\\',re.S)
    hf_re=re.compile(r'\\HF=(.*?)\\',re.S)
    xyz_re=re.compile(r'Standard orientation:.*?\n -*\n.*? -*\n(.*?) -*\n',re.S)
    # origin_text=out_file.read()
    origin_text=output
    text=origin_text.replace(' ','').replace('\n','')
    mp2_find=mp2_re.findall(text)
    hf_find=hf_re.findall(text)
    xyz_find=xyz_re.findall(origin_text)
    if xyz_find:
        xyzcontent=xyz_find.pop()

    pattern=re.compile(r'[ \t]+.+?[ \t]+(.+?)[ \t]+.+?[ \t]+(.+?)[ \t]+(.+?)[ \t]+?(.+?)\n')
    xyz=pattern.findall(xyzcontent)

    new=[]
    for j,i in enumerate(xyz):
        i=list(i)
        if i[0]=='1':
            i[0]='H'
        elif i[0]=='6':
            i[0]='C'
        elif i[0]=='8':
            i[0]='O'
        elif i[0]=='7':
            i[0]='N'
        elif i[0]=='16':
            i[0]='S'

        new.append(' '.join(i))
    atom_count=len(xyz)

    xyz=str(atom_count)+'\n'+'Energy:\n'+'\n'.join(new)

    if mp2_find:
        hf=float(mp2_find[0])
    else:
        hf=float(hf_find[0])

    xyz= re.sub(r'Energy:', 'Energy:  '+str(hf)+' ',xyz)


    coll=Conformer.get_coll(database,collection)
    new=coll.Conformer()
    # new.set_coll(database,collection)
    new.loads(xyz)
    print (new.dumps())

    # 内部可以用Conformer, 因此可以算完了直接入数据库. 另外回调函数可以再执行响应的连接和通知操作.
    # print new.collection
    # 重载save函数, 插入的时候就判重
    # new.save()
    # return True
    # todo: 分离判重复? 以及同时操作数据库的问题, 是否需要设置tryout的次数
    if new.is_needed_in_pool(energy_cut=energy_cut):
        print '=============='
        new.save()
    #
    # tryout=0
    # while tryout<5:
    #     try:
    #         new.save()
    #         break
    #     except:
    #         # time.sleep(1)
    #         tryout=tryout+1


    return True


def run(args):

    xyz=args['xyz']
    energy_cut=args['energy_cut']
    database=args['labkit']
    collection=args['current_ensemble']
    method=args['method']

    charge=0
    mutiplicity=1
    #
    gaussian(xyz=xyz,energy_cut=energy_cut,database=database,collection=collection,method=method,charge=charge,mutiplicity=mutiplicity)

    return True



def test():



    # 类和的模块的区别. 用类把



    coll=Conformer.get_coll('tmp','tmp')
    conformer=Conformer()
    # conformer.collection=get_coll('tmp','ttmp')
    # todo: set_coll不管用, 但是gaussian_conformer里面根据set_coll之后的conformer信息新建的conformer却是可以用的. 目前暂时使用get_coll做
    # conformer.set_coll('ttmp','tttmp')
    conformer.load(filename='/Users/lhr/lhrkits/labkit/test/cggg1.xyz')
    conformer.save()
    return
    print conformer.collection

    # print conformer.dumps()
    # print zmatrix
    # conformer.load_from_zmatrix(zmatrix)
    # print conformer.get_zmatrix()
    # print conformer.get_xyz()


    new_c = gaussian( conformer)
    #
    print new_c
    #

    # new_c.save()





def selfrun():
    import labkit.init_gs
    from general.interpreter.loader import callrun
    callrun(__file__)
if __name__ == '__main__':
    # test()
    selfrun()
