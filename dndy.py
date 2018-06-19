#!/usr/bin/env python

import ROOT
from ROOT import *

files=[]
files.append(TFile('full/rawmoments.root'))
files.append(TFile('nodecay/rawmoments.root'))
files.append(TFile('noscat/rawmoments.root'))

proton=[]
kaon=[]
charge=[]
for i in range(3):
    proton.append( files[i].Get('net_proton_dndy') )
    kaon.append( files[i].Get('net_kaon_dndy') )
    charge.append( files[i].Get('net_charge_dndeta') )
gROOT.SetBatch(kTRUE)
gStyle.SetOptStat(kFALSE)
c=TCanvas('c','',800,400)
c.cd()
pad=TPad('pad','',0.01,0.01,0.99,0.99)
pad.Draw()
pad.Divide(3,1,0,0)
pad.cd(1)

proton[0].SetLineColor(1)
kaon[0].SetLineColor(1)
charge[0].SetLineColor(1)
proton[1].SetLineColor(4)
kaon[1].SetLineColor(4)
charge[1].SetLineColor(4)
proton[2].SetLineColor(2)
kaon[2].SetLineColor(2)
charge[2].SetLineColor(2)


for i in range(3):
    bins2=proton[i].GetNbinsX()
    for j in range(1, bins2+1):
        proton[i].SetBinContent(j, proton[i].GetBinContent(j)/600000 )

    bins3=kaon[i].GetNbinsX()
    for j in range(1, bins3+1):
        kaon[i].SetBinContent(j, kaon[i].GetBinContent(j)/600000 )

    bins4=charge[i].GetNbinsX()
    for j in range(1, bins4+1):
        charge[i].SetBinContent(j, charge[i].GetBinContent(j)/600000 )

pad.cd(1)
gPad.SetRightMargin(0.11)
pad.cd(2)
gPad.SetLeftMargin(0.10)
gPad.SetRightMargin(0.07)
pad.cd(3)
gPad.SetLeftMargin(0.18)


pad.cd(1)
proton[2].Draw('SAME')
proton[0].Draw('SAME')
proton[1].Draw('SAME')
pad.cd(2)
kaon[0].Draw('SAME')
kaon[2].Draw('SAME')
kaon[1].Draw('SAME')
pad.cd(3)
charge[0].Draw('SAME')
charge[1].Draw('SAME')
charge[2].Draw('SAME')

c.cd()
t1=TLatex(0.134,0.93,"Net-Proton")
t1.SetTextSize(0.045)
t1.SetNDC()
t1.Draw()
t2=TLatex(0.454,0.93,"Net-Kaon")
t2.SetTextSize(0.045)
t2.SetNDC()
t2.Draw()
t3=TLatex(0.771,0.93,"Net-Charge")
t3.SetTextSize(0.045)
t3.SetNDC()
t3.Draw()


pad.cd(1)
l=TLegend()
l.AddEntry(proton[0],'Full','l')
l.AddEntry(proton[1],'No decay','l')
l.AddEntry(proton[2],'No scat.','l')
l.SetTextSize(0.04)
l.SetX1(0.35)
l.SetX2(0.55)
l.SetY1(0.25)
l.SetY2(0.38)
l.SetLineColor(0)
l.Draw()

c.Print('DNDY.pdf')


