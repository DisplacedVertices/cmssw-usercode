import sys
from collections import defaultdict
from ROOT import TGraph, TVectorF, TCanvas, TH1F, kRed
from JMTucker.Tools.ROOTTools import *
from itertools import izip
import random
from FWCore.PythonUtilities import LumiList

header = ['Run:Fill', 'LS', 'UTCTime', 'Beam Status', 'E(GeV)', 'Del(/nb)', 'Rec(/nb)', 'avgPU']
ps = plot_saver('plots_lumibyls_V3', size=(600,600))

info = ()

i = 0

this_fill = 0
this_run = 0
this_fill_rec = []
this_fill_apu = []
this_run_pos = []

lumis = []
pileups = []
times = []
fill = 0

sum_luminosity = 0
sum_luminosity2 = 0
max_ls = 167.147
random.seed()

lluminosity = []
lpileup = []
llumisec = []
lrun = []

# All
h_pileup = TH1F("h_pileup","h_pileup",100,0,50)
h_w_pileup = TH1F("h_w_pileup","h_w_pileup",100,0,50)
h_w_pileup.Sumw2()

h_luminosity = TH1F("h_luminosity","h_luminosity",200,0,170)
h_w_luminosity = TH1F("h_w_luminosity","h_w_luminosity",200,0,170)
h_w_luminosity.Sumw2()

# Random Pick
h_pileup_picked = TH1F("h_pileup_picked","h_pileup_picked",100,0,50)
h_w_pileup_picked = TH1F("h_w_pileup_picked","h_w_pileup_picked",100,0,50)
h_w_pileup_picked.Sumw2()

# Shaped distribution
h_shaped_pileup = TH1F("h_shaped_pileup","h_shaped_pileup",100,0,50)
h_w_shaped_pileup = TH1F("h_w_shaped_pileup","h_w_shaped_pileup",100,0,50)
h_w_shaped_pileup.Sumw2()

h_shaped_luminosity = TH1F("h_shaped_luminosity","h_shaped_luminosity",200,0,170)
h_w_shaped_luminosity = TH1F("h_w_shaped_luminosity","h_w_shaped_luminosity",200,0,170)
h_w_shaped_luminosity.Sumw2()

for line in open(sys.argv[1]):
    line = line.split('|')
    #print len(line), line
    if len(line) != 10:
        continue
    line = [x.strip() for x in line if x.strip()]

    run_fill, ls, time, status, energy, delivered, recorded, avgpu = line
    
    if fill != "Fill":
        fill_m1 = int(fill)
         
    try:
        run, fill = run_fill.split(':')
        run = int(run)
        fill = int(fill)
        ls = int(ls.split(':')[0])
        recorded = float(recorded)
        avgpu = float(avgpu)
    except ValueError:
        assert line == header
        continue
    
    #print '%i,%i,%i,%s,%g,%g' % (i,fill,run,time,recorded,avgpu)

    #print "lumi=",ls," pileup=",avgpu
    
    assert fill >= this_fill
    assert run >= this_run

#    if avgpu < 4:
 #       print "Fill with small pileup=",fill
  #      print "Run with small pileup=",run

    lluminosity.append(recorded)
    lpileup.append(avgpu)
    llumisec.append(ls)
    lrun.append(run)
    
    if fill_m1 != fill:
        i = 0
        Luminosity = TVectorF(221878)
        Pileup = TVectorF(221878)
        Time = TVectorF(221878)
        lumis.append(Luminosity)
        pileups.append(Pileup)
        times.append(Time)

    #print i,fill_m1,fill
    
    Luminosity[i] = recorded
    Pileup[i] = avgpu
    zeit = time.split(" ")[1] # FIX TIME
    Zeit = int(int(zeit.split(":")[0])*3600+int(zeit.split(":")[1])*60+int(zeit.split(":")[2]))
    Time[i] = Zeit
    i += 1

for rec,pu in izip(lluminosity,lpileup):
    h_pileup.Fill(pu)
    h_luminosity.Fill(rec)
    h_w_pileup.Fill(pu,rec)

lumi_list =  LumiList.LumiList('Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt')
reduced_lumi_list = LumiList.LumiList()

while sum_luminosity2 < 1000000.:
    x = random.randint(0,221878)
    sum_luminosity2 += lluminosity[x]
    h_pileup_picked.Fill(lpileup[x])
    h_w_pileup_picked.Fill(lpileup[x],lluminosity[x])
    if lumi_list.contains(lrun[x],llumisec[x]):
        reduced_lumi_list = reduced_lumi_list + LumiList.LumiList('',[[lrun[x],llumisec[x]]])

reduced_lumi_list.writeJSON('picked_data_JSON.txt')
    
  
h_pileup.DrawNormalized()
h_pileup_picked.SetLineColor(kRed)
h_pileup_picked.DrawNormalized()
h_pileup.DrawNormalized("same")
ps.save("h_pileup_norm")

h_w_pileup_picked.SetLineColor(kRed)
h_w_pileup_picked.DrawNormalized()
h_w_pileup.DrawNormalized("same")
ps.save("h_w_pileup_norm")

        
#count=0
#print "How many fills? ",len(lumis),len(pileups),len(times)
#for i,j,k in izip(lumis,pileups,times):
#    h1=TGraph(k,i)
#    h1.Draw("AP")
#    ps.save("Lumi"+str(count))
#    h2=TGraph(k,j)
#    h2.Draw("AP")
#    ps.save("Pileup"+str(count))
#    count +=1

