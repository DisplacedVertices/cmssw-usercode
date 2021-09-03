import sys
from DVCode.Tools.ROOTTools import ROOT
from binning import binning

def book(out_name, hs=[]):
    bins = binning()
    h = ROOT.TH1F(out_name, '', len(bins)-1, bins)
    hs.append(h)
    return h

f = ROOT.TFile('export.root', 'recreate')

execfile(sys.argv[1])

f.Write()
f.Close()
