#!/usr/bin/env python

import ROOT
from ROOT import *

files=[]
files.append(TFile('full/rawmoments.root'))
files.append(TFile('nodecay/rawmoments.root'))
files.append(TFile('noscat/rawmoments.root'))

refmult2=[]
refmult3=[]
refmult4=[]
for i in range(3):
    refmult2.append( files[i].Get('refMult2') )
    refmult3.append( files[i].Get('refMult3') )
    refmult4.append( files[i].Get('refMult4') )
gROOT.SetBatch(kTRUE)
gStyle.SetOptStat(kFALSE)
c=TCanvas('c','',800,400)
c.cd()
pad=TPad('pad','',0.01,0.01,0.99,0.99)
pad.Draw()
pad.Divide(3,1,0,0)
pad.cd(1)

for i in range(3):
    entries2=refmult2[i].GetEntries()
    bins2=refmult2[i].GetNbinsX()
    for j in range(1, bins2+1):
        refmult2[i].SetBinContent(j, refmult2[i].GetBinContent(j)/600000 )

    entries3=refmult2[i].GetEntries()
    bins3=refmult2[i].GetNbinsX()
    for j in range(1, bins3+1):
        refmult2[i].SetBinContent(j, refmult2[i].GetBinContent(j)/600000 )

    entries4=refmult2[i].GetEntries()
    bins4=refmult2[i].GetNbinsX()
    for j in range(1, bins4+1):
        refmult2[i].SetBinContent(j, refmult2[i].GetBinContent(j)/600000 )

for i in range(3):
    if i == 1:
        refmult2[i].Draw()
    else:
        refmult2[i].Draw('SAME')
pad.cd(2)
for i in range(3):
    if i == 1:
        refmult3[i].Draw()
    else:
        refmult3[i].Draw('SAME')
pad.cd(3)
for i in range(3):
    if i == 1:
        refmult4[i].Draw()
    else:
        refmult4[i].Draw('SAME')
c.Print('ref.pdf')


