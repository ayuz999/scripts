#!/usr/bin/env python
import ROOT
from ROOT import *
import array
from array import array

DataList=[]

'''
    DataList Map  [i][j][k]
    
          i    full    nodecay    noscat
       j     
    k            

    c1    NetProton
    c2      
    c3       
    c4        
    ec1       NetKaon
    ec2         
    ec3          
    ec4           
    R21           NetCharge
    R31
    R32
    R42
    eR21
    eR31
    eR32
    eR42
'''

for j in range(0, 3):
    jList=[]
    for k in range(0, 3):
        kList=[]
        for item in range(0, 16):
            kList.append(array('f', [ 0 for i in range(0,20) ]))
        jList.append(kList)
    DataList.append(jList)

files=[]
trees=[]

iitem=['full','nodecay','noscat']
jitem=['pro','kao','chr']
kitem=['c1','c2','c3','c4','ec1','ec2','ec3','ec4','R21','R31','R32','R42','eR21','eR31','eR32','eR42']

for i in range(3):
    files.append( TFile(iitem[i]+'/'+iitem[i]+'_cumulant.root') )    
    trees.append( files[i].Get(iitem[i]) )
    for j in range(3):
        for k in range(16):
            trees[i].SetBranchAddress(jitem[j]+'_'+kitem[k], DataList[i][j][k])
    trees[i].GetEntry(0)
ex=array('f', [0 for i in range(20)])

### cumulants c1-c4
CumTGE=[]
for i in range(3):
    ilist=[]
    for j in range(3):
        if j == 2:
            x=array('f',[ round(0.05*x, 2) for x in range(1, 21) ])
        else:
            x=array('f',[ round(0.2*x, 1) for x in range(1, 21) ])
        jlist=[]
        for k in range(4):
            jlist.append( TGraphErrors(20, x, DataList[i][j][k], ex, DataList[i][j][k+4] ))
        ilist.append(jlist)
    CumTGE.append(ilist)
### ratios R21 R31 R32 R42
RatTGE=[]
for i in range(3):
    ilist=[]
    for j in range(3):
        if j == 2:
            x=array('f',[ round(0.05*x, 2) for x in range(1, 21) ])
        else:
            x=array('f',[ round(0.2*x, 1) for x in range(1, 21) ])
        jlist=[]
        for k in range(4):
            jlist.append( TGraphErrors(20, x, DataList[i][j][k+8], ex, DataList[i][j][k+12] ))
        ilist.append(jlist)
    RatTGE.append(ilist)
##  
gROOT.SetBatch(kTRUE)
gStyle.SetOptStat(kFALSE)
for i in range(3):
    for j in range(3):
        for k in range(4):
            CumTGE[i][j][k].SetMarkerColor(2**i)
            CumTGE[i][j][k].SetLineColor(2**i)
            CumTGE[i][j][k].SetMarkerStyle(24+i)
            RatTGE[i][j][k].SetMarkerColor(2**i)
            RatTGE[i][j][k].SetLineColor(2**i)
            RatTGE[i][j][k].SetMarkerStyle(24+i)
            if i == 1:
                CumTGE[i][j][k].SetMarkerColor(4)
                CumTGE[i][j][k].SetLineColor(4)
                CumTGE[i][j][k].SetMarkerStyle(26)
                RatTGE[i][j][k].SetMarkerColor(4)
                RatTGE[i][j][k].SetLineColor(4)
                RatTGE[i][j][k].SetMarkerStyle(26)
            if i == 2:
                CumTGE[i][j][k].SetMarkerColor(2)
                CumTGE[i][j][k].SetLineColor(2)
                CumTGE[i][j][k].SetMarkerStyle(25)
                RatTGE[i][j][k].SetMarkerColor(2)
                RatTGE[i][j][k].SetLineColor(2)
                RatTGE[i][j][k].SetMarkerStyle(25)
            
## draw cumulants
c=TCanvas("c","",800,600)
c.cd()
pad=TPad("pad","",0.03,0.03,0.99,0.95)
pad.Draw()
pad.Divide(3,4,0,0)
pad.cd(1)
gPad.SetRightMargin(0.15)
pad.cd(4)
gPad.SetRightMargin(0.15)
pad.cd(7)
gPad.SetRightMargin(0.15)
pad.cd(10)
gPad.SetRightMargin(0.15)
pad.cd(2)
gPad.SetLeftMargin(0.07)
gPad.SetRightMargin(0.07)
pad.cd(5)
gPad.SetLeftMargin(0.07)
gPad.SetRightMargin(0.07)
pad.cd(8)
gPad.SetLeftMargin(0.07)
gPad.SetRightMargin(0.07)
pad.cd(11)
gPad.SetLeftMargin(0.07)
gPad.SetRightMargin(0.07)
pad.cd(3)
gPad.SetLeftMargin(0.15)
pad.cd(6)
gPad.SetLeftMargin(0.15)
pad.cd(9)
gPad.SetLeftMargin(0.15)
pad.cd(12)
gPad.SetLeftMargin(0.15)

gStyle.SetLabelSize(0.09,'xy')
pad.cd(1)
#gPad.SetGrid()
gPad.DrawFrame(0,-1.8,2.5,22.4)
gStyle.SetLabelSize(0.09,'xy')
pad.cd(4)
#gPad.SetGrid()
gPad.DrawFrame(0,-1.8,2.5,22.4)
gStyle.SetLabelSize(0.09,'xy')
pad.cd(7)
#gPad.SetGrid()
gPad.DrawFrame(0,-1.8,2.5,22.4)
gStyle.SetLabelSize(0.09,'xy')
pad.cd(10)
#gPad.SetGrid()
gPad.DrawFrame(0,-1.8,2.5,22.4)
gStyle.SetLabelSize(0.09,'xy')
pad.cd(2)
#gPad.SetGrid()
gPad.DrawFrame(0,-3.80,2.5,23.3)
gStyle.SetLabelSize(0.09,'xy')
pad.cd(5)
#gPad.SetGrid()
gPad.DrawFrame(0,-3.80,2.5,53.3)
gStyle.SetLabelSize(0.09,'xy')
pad.cd(8)
#gPad.SetGrid()
gPad.DrawFrame(0,-3.80,2.5,13.3)
gStyle.SetLabelSize(0.09,'xy')
pad.cd(11)
#gPad.SetGrid()
gPad.DrawFrame(0,-19.80,2.5,53.3)
gStyle.SetLabelSize(0.09,'xy')
pad.cd(3)
#gPad.SetGrid()
gPad.DrawFrame(0,-4.80,1.15,28.3)
gStyle.SetLabelSize(0.09,'xy')
pad.cd(6)
#gPad.SetGrid()
gPad.DrawFrame(0,-24.80,1.15,253.3)
gStyle.SetLabelSize(0.09,'xy')
pad.cd(9)
#gPad.SetGrid()
gPad.DrawFrame(0,-24.80,1.15,56.3)
gStyle.SetLabelSize(0.09,'xy')
pad.cd(12)
#gPad.SetGrid()
gPad.DrawFrame(0,-1457,1.15,696)
gStyle.SetLabelSize(0.09,'xy')

for i in range(3):
    for j in range(4):
        for k in range(3):
            pad.cd(i+j*3+1)
            CumTGE[k][i][j].SetTitle()
            CumTGE[k][i][j].Draw("PSAME")

le=TLegend()
le.AddEntry(CumTGE[0][0][0],'Full Calc.','p')
le.AddEntry(CumTGE[1][0][0],'No Decay','p')
le.AddEntry(CumTGE[2][0][0],'No Scat.','p')
le.SetX1(0.21)
le.SetX2(0.68)
le.SetY1(0.60)
le.SetY2(0.98)
le.SetLineColor(0)
pad.cd(3)
le.Draw()

la1=TLatex(0.12,0.95,"Net-Proton")
la1.SetNDC()
la1.SetTextSize(0.035)
la2=TLatex(0.46,0.95,"Net-Kaon")
la2.SetNDC()
la2.SetTextSize(0.035)
la3=TLatex(0.77,0.95,"Net-Charge")
la3.SetNDC()
la3.SetTextSize(0.035)
c.cd()
la1.Draw()
la2.Draw()
la3.Draw()
l1=TLatex(0.03,0.79,"C_{1}")
l1.SetNDC()
l1.SetTextSize(0.031)
l1.SetTextAngle(90)
l2=TLatex(0.03,0.59,"C_{2}")
l2.SetNDC()
l2.SetTextSize(0.031)
l2.SetTextAngle(90)
l3=TLatex(0.03,0.37,"C_{3}")
l3.SetNDC()
l3.SetTextSize(0.031)
l3.SetTextAngle(90)
l4=TLatex(0.03,0.16,"C_{4}")
l4.SetNDC()
l4.SetTextAngle(90)
l4.SetTextSize(0.031)
c.cd()
l1.Draw()
l2.Draw()
l3.Draw()
l4.Draw()

yt1=TLatex(0.18,0.01,"#Delta y")
yt1.SetNDC()
yt1.SetTextSize(0.027)
yt2=TLatex(0.51,0.01,"#Delta y")
yt2.SetNDC()
yt2.SetTextSize(0.027)
yt3=TLatex(0.83,0.01,"#Delta #eta")
yt3.SetNDC()
yt3.SetTextSize(0.027)
yt1.Draw()
yt2.Draw()
yt3.Draw()



c.Print('cum.pdf')

c1=TCanvas("c1","",800,600)
c1.cd()
pad1=TPad("pad","",0.037,0.03,0.99,0.95)
pad1.Draw()
pad1.Divide(3,4,0,0)
pad1.cd(1)
gPad.SetRightMargin(0.15)
pad1.cd(4)
gPad.SetRightMargin(0.15)
pad1.cd(7)
gPad.SetRightMargin(0.15)
pad1.cd(10)
gPad.SetRightMargin(0.15)
pad1.cd(2)
gPad.SetLeftMargin(0.07)
gPad.SetRightMargin(0.07)
pad1.cd(5)
gPad.SetLeftMargin(0.07)
gPad.SetRightMargin(0.07)
pad1.cd(8)
gPad.SetLeftMargin(0.07)
gPad.SetRightMargin(0.07)
pad1.cd(11)
gPad.SetLeftMargin(0.07)
gPad.SetRightMargin(0.07)
pad1.cd(3)
gPad.SetLeftMargin(0.15)
pad1.cd(6)
gPad.SetLeftMargin(0.15)
pad1.cd(9)
gPad.SetLeftMargin(0.15)
pad1.cd(12)
gPad.SetLeftMargin(0.15)

gStyle.SetLabelSize(0.09,'xy')
pad1.cd(1)
#gPad.SetGrid()
gPad.DrawFrame(0,0.855,2.5,1.215)
gStyle.SetLabelSize(0.09,'xy')
pad1.cd(4)
#gPad.SetGrid()
gPad.DrawFrame(0,0.78,2.5,1.13)
gStyle.SetLabelSize(0.09,'xy')
pad1.cd(7)
#gPad.SetGrid()
gPad.DrawFrame(0,0.8,2.5,1.1)
gStyle.SetLabelSize(0.09,'xy')
pad1.cd(10)
#gPad.SetGrid()
gPad.DrawFrame(0,0.48,2.5,1.2)
gStyle.SetLabelSize(0.09,'xy')
pad1.cd(2)
#gPad.SetGrid()
gPad.DrawFrame(0,2.07,2.5,7.3)
gStyle.SetLabelSize(0.09,'xy')
pad1.cd(5)
#gPad.SetGrid()
gPad.DrawFrame(0,0.3,2.5,1.7)
gStyle.SetLabelSize(0.09,'xy')
pad1.cd(8)
#gPad.SetGrid()
gPad.DrawFrame(0,0.02,2.5,0.43)
gStyle.SetLabelSize(0.09,'xy')
pad1.cd(11)
#gPad.SetGrid()
gPad.DrawFrame(0,-1.10,2.5,2.5)
gStyle.SetLabelSize(0.09,'xy')
pad1.cd(3)
#gPad.SetGrid()
gPad.DrawFrame(0,8.80,1.15,14.3)
gStyle.SetLabelSize(0.09,'xy')
pad1.cd(6)
#gPad.SetGrid()
gPad.DrawFrame(0,-2.50,1.15,4.9)
gStyle.SetLabelSize(0.09,'xy')
pad1.cd(9)
#gPad.SetGrid()
gPad.DrawFrame(0,-0.120,1.15,0.3)
gStyle.SetLabelSize(0.09,'xy')
pad1.cd(12)
#gPad.SetGrid()
gPad.DrawFrame(0,-5,1.15,7)
gStyle.SetLabelSize(0.09,'xy')

for i in range(3):
    for j in range(4):
        for k in range(3):
            pad1.cd(i+j*3+1)
            RatTGE[k][i][j].SetTitle()
            RatTGE[k][i][j].Draw("PSAME")

pad1.cd(11)
le.Draw()
c1.cd()
la1.Draw()
la2.Draw()
la3.Draw()
t1=TLatex(0.03,0.79,"C_{2}/C_{1}")
t1.SetNDC()
t1.SetTextSize(0.031)
t1.SetTextAngle(90)
t2=TLatex(0.03,0.59,"C_{3}/C_{1}")
t2.SetNDC()
t2.SetTextSize(0.031)
t2.SetTextAngle(90)
t3=TLatex(0.03,0.37,"s#sigma")
t3.SetNDC()
t3.SetTextSize(0.031)
t3.SetTextAngle(90)
t4=TLatex(0.03,0.16,"#kappa#sigma^{2}")
t4.SetNDC()
t4.SetTextAngle(90)
t4.SetTextSize(0.031)
t1.Draw()
t2.Draw()
t3.Draw()
t4.Draw()

yt1.Draw()
yt2.Draw()
yt3.Draw()

c1.Print('ratio.pdf')

