#! /usr/bin/env python                                                                                                                                                                  

import os, mmap, math

src=mmap.mmap(os.open('filelist.19.6.ful', os.O_RDONLY), 0, prot=mmap.PROT_READ)
src2=file('filelist.19.6.ful')
os.mkdir('data', 0755)

row=100.
ndirs=int(math.ceil(len(src2.readlines()) / row))
for i in range(1, ndirs+1):
        os.mkdir('data/task'+str(i), 0755)

n=0
while(True):
    line=src.readline()
    if line != "": 
        m= n / int(row)
        f=open('data/task'+str(m+1)+'/file.list', 'a')
        f.write(line) 
        f.close()
        n+=1    
    else:
        break
