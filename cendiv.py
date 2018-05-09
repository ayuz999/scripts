#! /usr/bin/env python

import ROOT
from ROOT import *

f=TFile('RefMult3.root')
output=file("Centrality.txt","w")
refMult=f.Get('RefMult3')
entries=refMult.GetEntries()
bins=refMult.GetNbinsX()
centPercent=[0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]
sums=0
centFlag=1
a=range(1,bins+1)
for bin in reversed(a):
    for flag in range(1,len(centPercent)+1):
        if(centFlag==flag):
            if(sums<=entries*centPercent[flag-1]):
                if(refMult.GetBinContent(bin)>=1):
                    sums+=refMult.GetBinContent(bin)
            else:
                centFlag+=1
                print(('%.0f%%' % round(centPercent[flag-1]*100))+' : '+str(bin))
                output.write(('%.0f%%' % round(centPercent[flag-1]*100))+':'+str(bin)+'\n')
