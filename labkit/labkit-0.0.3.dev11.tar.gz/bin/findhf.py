#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry




import os, re


def format_to_xyz(filename):
    filename = str(filename)
    filename = filename.replace('.xyz', '')
    filename = filename.replace('.out', '')
    filename = filename + '.xyz'
    return filename


def main():
    file_name_list=os.popen("ls|grep \.out").read().strip().split('\n')

    output_file=open('all.csv','w')
    mp2_re=re.compile(r'\\MP2=(.*?)\\',re.S)
    hf_re=re.compile(r'\\HF=(.*?)\\',re.S)
    out=[]
    method_re=re.compile(r'----\#(.*?)----',re.S)


    filename=file_name_list[0]
    file=open(filename)
    text=file.read().replace(' ','').replace('\n','')
    mp2_find=mp2_re.findall(text)
    hf_find=hf_re.findall(text)
    method_find=method_re.findall(text)
    method=method_find[0]
    if mp2_find:
        for filename in file_name_list:
            file=open(filename)
            text=file.read().replace(' ','').replace('\n','')

            mp2_find=mp2_re.findall(text)
            hf_find=hf_re.findall(text)
            method_find=method_re.findall(text)
            out.append((filename,float(mp2_find[0])))
    elif hf_find:
        for filename in file_name_list:
            file=open(filename)
            text=file.read().replace(' ','').replace('\n','')
            mp2_find=mp2_re.findall(text)
            hf_find=hf_re.findall(text)
            method_find=method_re.findall(text)
            out.append((filename,float(hf_find[0])))

    sorted_out=sorted(out,key=lambda item:item[1])


    zero_energy_hf=sorted_out[0][1]
    output_file.write('Name\tOrder\t'+method+' (a.u)\tdelt_E (kcal/mol)\n')
    for i,line in enumerate(sorted_out):
        delt_e=(line[1]-zero_energy_hf)*627.5095

        output_file.write(str(line[0])+'\t'+str(i+1)+'\t'+str(line[1])+'\t'+str(delt_e)+'\n')


    output_file.close()


    # xlsx_file_name = os.popen("ls *.xls*").read().strip()




    # for i in range(1, nrows):
    #     before = str(table.cell(i, 0).value).replace('.0','')
    #     after = i

    #     before_file_name = os.path.join(curpath, format_to_xyz(before))
    #     after_file_name = os.path.join(curpath, format_to_xyz(after))

    #     os.rename(before_file_name, after_file_name)


    # os.system("open %s" % xlsx_file_name)



if __name__ == '__main__':
    main()
