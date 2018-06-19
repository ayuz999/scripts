#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include "TFile.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TTree.h"
#include "TProfile.h"
#include <algorithm>
#include "PDGData.h"
using namespace std;

void calc()
{

    ifstream input("test.list");//.19.6.ful");
    string line;
    vector<string> InputList;
    while(input >> line) {
        InputList.push_back(line);
    }

    TFile *output = new TFile("rawmoments.root","recreate");
    TFile* file;
    TTree* tree;
    PDGData pdg;
    int Entries = 0;
    float px[10000];
    float py[10000];
    float pz[10000];
    int pid[10000];
    int mul=0;
    int proton[20], kaon[20], charge[20] = {0};// 20: abs(y) range(0.1:2) *10  20 : abs(eta) range(0.025:0.5) *40
    int aproton[20], akaon[20], ncharge[20] = {0};
    int netproton[20], netkaon[20], netcharge[20] = {0};
    int refmult2, refmult3, refmult4=0;
    float mass=0;
    //raw moments [y or eta range][16 order]
    TProfile *RawMoments_netproton[20][16];
    TProfile *RawMoments_netkaon[20][16];
    TProfile *RawMoments_netcharge[20][16];
    for(int i=0; i< 20; i++)
        for(int j=0; j<16; j++)
            RawMoments_netproton[i][j] = new TProfile(Form("RawMoments_netproton_y_%d_%d",i,j),"",1500,0,1500,-5e30,5e30);
    for(int i=0; i< 20; i++)
        for(int j=0; j<16; j++)
            RawMoments_netkaon[i][j] = new TProfile(Form("RawMoments_netkaon_y_%d_%d",i,j),"",1500,0,1500,-5e30,5e30);
    for(int i=0; i< 20; i++)
        for(int j=0; j<16; j++)
            RawMoments_netcharge[i][j] = new TProfile(Form("RawMoments_netcharge_eta_%d_%d",i,j),"",1500,0,1500,-5e30,5e30);

    //histograms
    //event by event distribution
    TH1D*  Net_Proton_Dist = new TH1D("netproton_dist","",60,-20,40);
    TH1D*  Net_Kaon_Dist = new TH1D("netkaon_dist","",80,0,80);
    TH1D*  Net_Charge_Dist = new TH1D("netcharge_dist","",60,-20,40);

    // dndy or dndeta distribution
    TH1D* dndy_netproton = new TH1D("net_proton_dndy",";y;dN/dy",60,-3,3);
    TH1D* dndy_netkaon = new TH1D("net_kaon_dndy",";y;dN/dy",100,-5,5);
    TH1D* dndeta_netcharge = new TH1D("net_charge_dndeta",";#eta;dN/d#eta",100,-5,5);


    TH1D *refMult2= new TH1D("refMult2",";RefMult2;Event counts",600,600,1200);
    TH1D *refMult3= new TH1D("refMult3",";RefMult3;Event counts",600,400,1000);
    TH1D *refMult4= new TH1D("refMult4",";RefMult4;Event counts",600,400,1000);

    // root file loop
    for(int i = 0; i<InputList.size(); i++) {

        file = TFile::Open(InputList[i].c_str());
        file->GetObject("jam", tree);
        tree->SetBranchAddress("px",px);
        tree->SetBranchAddress("py",py);
        tree->SetBranchAddress("pz",pz);
        tree->SetBranchAddress("mul",&mul);
        tree->SetBranchAddress("pid",pid);

        // event loop
        Entries = tree->GetEntries();
        for (int j = 0; j< Entries; j++) {
            tree->GetEntry(j);

            //track loop
            refmult2=refmult3=refmult4=0;
            for(int i=0; i<20; i++) {
                proton[i]=0;
                aproton[i]=0;
                kaon[i]=0;
                akaon[i]=0;
                charge[i]=0;
                ncharge[i]=0;
                netcharge[i]=0;
                netkaon[i]=0;
                netproton[i]=0;

            }

            for(int k=0; k<=mul; k++) {

                float p=sqrt(px[k]*px[k]+py[k]*py[k]+pz[k]*pz[k]);
                float pt=sqrt(px[k]*px[k]+py[k]*py[k]);
                float eta=0.5*log((p+pz[k])/(p-pz[k]));
                float aeta=fabs(eta);
                int apid=abs(pid[k]);
                mass = pdg[apid].m0;
                int charge = (pdg[apid].charge)/3 *( pid[k]>0 ? 1: -1);
                float E=sqrt(p*p+mass*mass);
                float y=0.5*log((E+pz[k])/(E-pz[k]));
                float ay=fabs(y);

                //refmult2,3,4
                if( aeta > 0.5 && aeta < 2 && (charge != 0) ) refmult2++;
                if( aeta < 1 && (apid == 211 || apid == 321) ) refmult3++;
                if( aeta < 1 && (apid == 2212 || apid == 211) ) refmult4++;

                if(apid == 2212)
                    dndy_netproton->Fill(y, charge *10);
                if(apid == 321)
                    dndy_netkaon->Fill(y, charge *10);
                if( charge != 0)
                    dndeta_netcharge->Fill(eta, charge *10);

                if( apid == 2212 && pt > 0.4 && pt < 2 ) {
                    if(ay < 2)
                        for(double i=2; ay < i; i-=0.1){
                            netproton[int(ceil(i*10))-1] += (charge > 0 ? 1 : -1);
                        }
                }
                /////////////

                if( apid == 321 && pt > 0.2 && pt < 1.6 ) 
                {
                    if(ay < 2)
                        for(double i=2; ay < i; i-=0.1){
                            netkaon[int(ceil(i*10))-1] += (charge > 0 ? 1 : -1);
                        }
                }
                ////////////////////
                if( (apid == 2212 || apid == 211 || apid == 321 ) && pt > 0.2 && pt < 2 ) {
                    if(aeta < 0.5)
                        for(double i=0.5; aeta < i; i-=0.025){
                            netcharge[int(ceil(i*40))-1] += (charge > 0 ? 1 : -1);
                        }
                }

            }
            // track loop ends
            
            // fill refmult2,3,4 histograms
            refMult2->Fill(refmult2);
            refMult3->Fill(refmult3);
            refMult4->Fill(refmult4);

            Net_Proton_Dist->Fill(netproton[15]); //|y|<0.5
            Net_Kaon_Dist->Fill(netkaon[15]);        //|y|<0.5
            Net_Charge_Dist->Fill(netcharge[0]);    //|eta|<0.5


            for(int i=0; i<20; i++) {

                double NETP, NETK, NETQ;
                NETP = netproton[i];
                NETK =   netkaon[i];
                NETQ = netcharge[i];
                for (int j=0; j<16; j++) {
                    RawMoments_netproton[i][j]->Fill(refmult3, NETP);
                    RawMoments_netkaon[i][j]  ->Fill(refmult4, NETK);
                    RawMoments_netcharge[i][j]->Fill(refmult2, NETQ);
                    NETP = NETP * netproton[i];
                    NETK = NETK * netkaon[i];
                    NETQ = NETQ * netcharge[i];
                }
            }




        } //event loop ends

    }// root file loop ends

    output->cd();
    output->Write();

}

int main()
{

    calc();
    return 0;
}
