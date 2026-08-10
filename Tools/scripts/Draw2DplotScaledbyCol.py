
'''
This script draws 2D histograms from histos.py
It will scale the histogram to make every column sum up to be 1
'''
import ROOT as R
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input',dest='input',default="")
parser.add_argument('--plot',dest='plot',default="")
parser.add_argument('--norm',action='store_true')
args = parser.parse_args()

f = R.TFile(args.input)
h = f.Get(args.plot)
xbins = h.GetNbinsX()
ybins = h.GetNbinsY()
nentries = h.GetEntries()

if(args.norm):
  for i in range(1,xbins+1):
    if h.Integral(i,i,1,ybins)==0:
      continue
    factor = 1.0/h.Integral(i,i,1,ybins)
    for j in range(1,ybins+1):
      cur = h.GetBinContent(i,j)
      h.SetBinContent(i,j,(cur*factor))
h.SetEntries(nentries)
h.GetYaxis().SetRangeUser(0,0.5)
h.Draw("colz")

input("Press <Enter> to quit...")


