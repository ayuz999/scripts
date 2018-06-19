#!/usr/bin/env python

import os, mmap

src=mmap.mmap(os.open('file.list', os.O_RDONLY), 0, prot=mmap.PROT_READ)
os.mkdir('Data', 0755)
runs=set()
while True:
    line=src.readline()
    if line!='':
        runs.add(line.split('/')[12])
    else:
        break

for item in runs:
    os.mkdir('Data/'+item, 0755)

src.seek(0)
while True:
    line=src.readline()
    if line!='':
        currRun=line.split('/')[12]
        f=open('Data/'+currRun+'/file.list', 'a')
        f.write(line)
        f.close()
    else:
        break
