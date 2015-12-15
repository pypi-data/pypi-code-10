#!/usr/bin/python
import sys
import os


def tail(f, n, offset=0):
    """Reads a n lines from f with an offset of offset lines."""
    avg_line_length = 74
    to_read = n + offset
    while 1:
        try:
            f.seek(-(avg_line_length * to_read), 2)
        except IOError:
            # woops.  apparently file is smaller than what we want
            # to step back, go to the beginning instead
            f.seek(0)
        pos = f.tell()
        lines = f.read().splitlines()
        if len(lines) >= to_read or pos == 0:
            return lines[-to_read:offset and -offset or None]
        avg_line_length *= 1.3



if not(os.path.isfile('list')):exit
filelist=open('list','r')
for pdbfilename in filelist.readlines():
    pdbfilename=pdbfilename.strip()
    xvgfilename=pdbfilename.replace('.pdb','.xvg')
    pdbfilename='m'+pdbfilename
    if not (os.path.isfile(pdbfilename)):continue
    pdbfile=open(pdbfilename,'r')
    if not (os.path.isfile(xvgfilename)):continue
    xvgfile=open(xvgfilename,'r')
    pdb=pdbfile.readlines()
    #xvg=tail(xvgfile,2)
    xvg=xvgfile.readline()
    if len(xvg)==0:continue
#    xvg=xvg[-1]
    
    xyz=[]
    #print xvgfilename
    for pdbline in pdb:
        tmp=pdbline.split()
        if len(tmp)>0 and tmp[0]=='ATOM':xyz.append(tmp)
    for i in range(len(xyz)):
        if xyz[i][2][0].isdigit():xyz[i][2]=xyz[i][2].replace(xyz[i][2][0],'')
        tmp=xyz[i][2][0]
        n=0
        if tmp=='H': n=1;
        elif tmp== 'C': n=6
        elif tmp== 'N': n=7
        elif tmp== 'O': n=8
        elif tmp== 'S': n=16
        elif tmp== 'P': n=15
        elif tmp== 'K': n=19
        elif tmp== 'B': n=5
        elif tmp== 'F': n=9
        elif tmp== 'I': n=53
        elif tmp== 'W': n=74
        elif tmp== 'U': n=92
        elif tmp== 'V': n=23
        elif tmp== 'Y': n=39
        xyz[i][2]=str(n)
        
    outfilename=xvgfilename.replace('.xvg','.out')
    outfile=open(outfilename,'w')
    outfile.write('''                         Standard orientation:                         
 ---------------------------------------------------------------------
 Center     Atomic     Atomic              Coordinates (Angstroms)
 Number     Number      Type              X           Y           Z
 ---------------------------------------------------------------------  \n''')
    for xyzline in xyz:
        outfile.write(xyzline[1]+'\t'+xyzline[2]+'\t0\t'+xyzline[5]+'\t'+xyzline[6]+'\t'+xyzline[7]+'\n')
    xvg=xvg.split()

    outfile.write(''' ---------------------------------------------------------------------  \n''')
    outfile.write(' Rotational constants \n')
    outfile.write('\HF='+str(float(xvg[9])/2625.49962)+'\Dipole='+xvg[-4]+','+xvg[-3]+','+xvg[-2]+'\n')
#    outfile.write('\HF='+str(float(xvg[9])/2625.49962)+'\Dipole=1,1,1'+'\n')
    outfile.close()
        

    
