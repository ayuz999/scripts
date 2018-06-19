#!/usr/bin/env python

import ROOT
from ROOT import *
import math
import array

#return calculated cumulants multiplied by events number
class calcCumulant:
    def __init__(self, profileList):
        self.profileList = profileList
        self.c1=0
        self.c2=0
        self.c3=0
        self.c4=0
        self.R21=0
        self.R31=0
        self.R32=0
        self.R42=0
        self.ec1=0
        self.ec2=0
        self.ec3=0
        self.ec4=0
        self.eR21=0
        self.eR31=0
        self.eR32=0
        self.eR42=0
    def calc(self):
        allEntries = self.profileList[0].GetEntries()
        for i in range(1, self.profileList[0].GetNbinsX()+1):
            binEntries = self.profileList[0].GetBinEntries(i)
            if binEntries == 0:
                continue
            m1 = self.profileList[0].GetBinContent(i)
            if m1 == 0:
                continue
            m2 = self.profileList[1].GetBinContent(i)
            m3 = self.profileList[2].GetBinContent(i)
            m4 = self.profileList[3].GetBinContent(i)
            m5 = self.profileList[4].GetBinContent(i)
            m6 = self.profileList[5].GetBinContent(i)
            m7 = self.profileList[6].GetBinContent(i)
            m8 = self.profileList[7].GetBinContent(i)
            cm2 = m2 - m1*m1
            cm3 = m3 - 3*m1*m2 + 2*m1**3
            cm4 = -3*m1**4 + 6*m1*m1*m2 - 4*m1*m3 + m4
            cm5 = 4*m1**5 - 10*m2*m1**3 + 10*m3*m1**2 - 5*m1*m4 + m5
            cm6 = -5*m1**6 + 15*m2*m1**4 - 20*m3*m1**3 + 15*m4*m1*m1 - 6*m1*m5 + m6
            cm7 = 6*m1**7 - 21*m2*m1**5 + 35*m3*m1**4 - 35*m4*m1**3 + 21*m5*m1*m1 - 7*m1*m6 + m7
            cm8 = -7*m1**8 + 28*m2*m1**6 -56*m3*m1**5 + 70*m4*m1**4 -56*m5*m1**3 + 28*m6*m1*m1 - 8*m1*m7 +m8
            sigma = math.sqrt(cm2)
            if sigma == 0:
                continue
            skew = cm3 / (sigma**3)
            kur = (cm4 - 3*cm2*cm2) / (cm2**2)
            ecm2 = cm4 - cm2*cm2 
            ecm3 = cm6 - cm3*cm3 - 6*cm4*cm2 + 9*cm2**3
            self.c1   += ((binEntries / allEntries) * ( m1 ))
            self.c2   += ((binEntries / allEntries) * ( cm2 ))
            self.c3   += ((binEntries / allEntries) * ( cm3 ))
            self.c4   += ((binEntries / allEntries) * ( cm4 - 3*cm2*cm2 ))
            self.R21  += ((binEntries / allEntries) * ( cm2 / m1 ))
            self.R31  += ((binEntries / allEntries) * ( cm3 / m1 ))
            self.R32  += ((binEntries / allEntries) * ( cm3 / cm2 ))
            self.R42  += ((binEntries / allEntries) * (( cm4 - 3*cm2*cm2 ) / cm2 ))
            self.ec1  += ( binEntries ) * math.fabs( cm2 )
            self.ec2  += ( binEntries ) * math.fabs( ecm2 )
            self.ec3  += ( binEntries ) * math.fabs( ecm3 )
            self.ec4  += ( binEntries ) * math.fabs( (cm2**4)*math.fabs(99 + 42*kur - kur*kur - 12*cm6/(sigma**6) + cm8/(sigma**8) - 8*cm5/(sigma**5)*skew + 64*skew*skew) )
            self.eR21 += ( binEntries ) * math.fabs( ecm2 / m1 )
            self.eR31 += ( binEntries ) * math.fabs( ecm3 / m1 )
            self.eR32 += ( binEntries ) * math.fabs( cm2*( -9 + cm6/(sigma**6) - 2*cm5/(sigma**5)*skew + 9*skew*skew + kur*(-6 + skew*skew) ))
            self.eR42 += ( binEntries ) * math.fabs( cm2*cm2*( cm8/(sigma**8) - 2*(kur+6)*cm6/(sigma**6) - 8*skew*cm5/(sigma**5) + 8*skew*skew*(kur+8) + kur**3 + 15*kur*kur + 72*kur + 99) )
        self.ec1 = math.sqrt(self.ec1) / allEntries
        self.ec2 = math.sqrt(self.ec2) / allEntries
        self.ec3 = math.sqrt(self.ec3) / allEntries
        self.ec4 = math.sqrt(self.ec4) / allEntries
        self.eR21 = math.sqrt(self.eR21) / allEntries
        self.eR31 = math.sqrt(self.eR31) / allEntries
        self.eR32 = math.sqrt(self.eR32) / allEntries
        self.eR42 = math.sqrt(self.eR42) / allEntries

## input and output file
infile=TFile("rawmoments.root")
outfile=TFile("full_cumulant.root","recreate")

## netproton
### read in netproton TProfiles which contains raw moments up to 16th order
profileList=[]
kaofileList=[]
chrfileList=[]
fileList=[]
for i in range(0, 20):
    temp1=[]
    temp2=[]
    temp3=[]
    for j in range(0, 16):
        temp1.append(infile.Get('RawMoments_netproton_y_'+str(i)+'_'+str(j)))
        temp2.append(infile.Get('RawMoments_netkaon_y_'+str(i)+'_'+str(j)))
        temp3.append(infile.Get('RawMoments_netcharge_eta_'+str(i)+'_'+str(j)))
    profileList.append(temp1)
    kaofileList.append(temp2)
    chrfileList.append(temp3)
fileList.append(profileList)
fileList.append(kaofileList)
fileList.append(chrfileList)
x=array.array('f',[ round(0.2*x, 1) for x in range(1, 21) ])

#          netproton         kaon           charge
c1   = [array.array('f'),array.array('f'),array.array('f')]
c2   = [array.array('f'),array.array('f'),array.array('f')]
c3   = [array.array('f'),array.array('f'),array.array('f')]
c4   = [array.array('f'),array.array('f'),array.array('f')]
R21  = [array.array('f'),array.array('f'),array.array('f')]
R31  = [array.array('f'),array.array('f'),array.array('f')]
R32  = [array.array('f'),array.array('f'),array.array('f')]
R42  = [array.array('f'),array.array('f'),array.array('f')]
ec1  = [array.array('f'),array.array('f'),array.array('f')]
ec2  = [array.array('f'),array.array('f'),array.array('f')]
ec3  = [array.array('f'),array.array('f'),array.array('f')]
ec4  = [array.array('f'),array.array('f'),array.array('f')]
eR21 = [array.array('f'),array.array('f'),array.array('f')]
eR31 = [array.array('f'),array.array('f'),array.array('f')]
eR32 = [array.array('f'),array.array('f'),array.array('f')]
eR42 = [array.array('f'),array.array('f'),array.array('f')]
ex=array.array('f',[0 for i in range(0, 20)])


for k in range(0,3):
    tmplist=[]
    for i in range(0, 20):
        tmplist.append(calcCumulant(fileList[k][i]))
        tmplist[i].calc()
        c1[k].append(tmplist[i].c1)
        c2[k].append(tmplist[i].c2)
        c3[k].append(tmplist[i].c3)
        c4[k].append(tmplist[i].c4)
        R21[k].append(tmplist[i].R21)
        R31[k].append(tmplist[i].R31)
        R32[k].append(tmplist[i].R32)
        R42[k].append(tmplist[i].R42)
        ec1[k].append(tmplist[i].ec1)
        ec2[k].append(tmplist[i].ec2)
        ec3[k].append(tmplist[i].ec3)
        ec4[k].append(tmplist[i].ec4)
        eR21[k].append(tmplist[i].eR21)
        eR31[k].append(tmplist[i].eR31)
        eR32[k].append(tmplist[i].eR32)
        eR42[k].append(tmplist[i].eR42)

tree = TTree("full","full_calcultaion_results")
item = ['pro','kao','chr']
for i in range(0, 3):
    tree.Branch(item[i]+"_c1", c1[i], item[i]+'_c1[20]/F')
    tree.Branch(item[i]+"_c2", c2[i], item[i]+'_c2[20]/F')
    tree.Branch(item[i]+"_c3", c3[i], item[i]+'_c3[20]/F')
    tree.Branch(item[i]+"_c4", c4[i], item[i]+'_c4[20]/F')
    tree.Branch(item[i]+"_ec1", ec1[i], item[i]+'_ec1[20]/F')
    tree.Branch(item[i]+"_ec2", ec2[i], item[i]+'_ec2[20]/F')
    tree.Branch(item[i]+"_ec3", ec3[i], item[i]+'_ec3[20]/F')
    tree.Branch(item[i]+"_ec4", ec4[i], item[i]+'_ec4[20]/F')
    tree.Branch(item[i]+"_R21", R21[i], item[i]+'_R21[20]/F')
    tree.Branch(item[i]+"_R31", R31[i], item[i]+'_R31[20]/F')
    tree.Branch(item[i]+"_R32", R32[i], item[i]+'_R32[20]/F')
    tree.Branch(item[i]+"_R42", R42[i], item[i]+'_R42[20]/F')
    tree.Branch(item[i]+"_eR21", eR21[i], item[i]+'_eR21[20]/F')
    tree.Branch(item[i]+"_eR31", eR31[i], item[i]+'_eR31[20]/F')
    tree.Branch(item[i]+"_eR32", eR32[i], item[i]+'_eR32[20]/F')
    tree.Branch(item[i]+"_eR42", eR42[i], item[i]+'_eR42[20]/F')

tree.Fill()
outfile.Write()
#gROOT.SetBatch(kTRUE)
#gStyle.SetOptStat(kFALSE)
#c=TCanvas("c","",800,600)
#c.cd()
#pad=TPad("pad","",0.01,0.01,0.99,0.99)
#pad.Draw()
#pad.cd()
#C1TGE=[]
#C2TGE=[]
#C3TGE=[]
#C4TGE=[]
#R21TGE=[]
#R31TGE=[]
#R32TGE=[]
#R42TGE=[]
#for i in range(0,3):
#    C1TGE.append(TGraphErrors(20, x, c1[i], ex, ec1[i]))
#    C2TGE.append(TGraphErrors(20, x, c2[i], ex, ec2[i]))
#    C3TGE.append(TGraphErrors(20, x, c3[i], ex, ec3[i]))
#    C4TGE.append(TGraphErrors(20, x, c4[i], ex, ec4[i]))
#    R  TGE.append(TGraphErrors(20, x,))
#    CumTGE[0].SetMarkerStyle(21)
#    CumTGE[0].Draw('alp')
#
#c.Print("fig.pdf")
