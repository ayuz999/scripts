#! /usr/bin/env python

import os, mmap, math

src=mmap.mmap(os.open('file.list', os.O_RDONLY), 0, prot=mmap.PROT_READ)
src2=file('file.list')
os.mkdir('Data', 0755)

row=200.
ndirs=int(math.ceil(len(src2.readlines()) / row))
for i in range(1, ndirs+1):
    os.mkdir('Data/TASK'+str(i), 0755)

n=0
while(True):
    line=src.readline()
    if line != "":
        m= n / int(row)
        f=open('Data/TASK'+str(m+1)+'/file.list', 'a')
        f.write(line) 
        f.close()
        n+=1
    else:
        break
