# create the input file with e.g.
#  comparehists.py /uscms_data/d2/tucker/crab_dirs/HistosV15/qcdht{0500,0700,1000,1500,2000}sum.root mfvEventHistosPreSel $asdf/plots/qcd_ht --nice 500 700 1000 1500 2000 --skip 'name != "h_jet_ht_40" and name != "h_jet_ht"' --scaling '-{"500": 19.346633, "700": 5.767810, "1000": 3.054774, "1500": 0.390518, "2000": 0.161415}[curr]'

import sys
from JMTucker.Tools.ROOTTools import *
set_style()

f = ROOT.TFile("h_jet_ht_40.root")
c = f.Get('c0')

hts = 500, 700, 1000, 1500, 2000
hs = [c.FindObject(str(ht)) for ht in hts]

nbins = hs[0].GetNbinsX()
xax = hs[0].GetXaxis()

min_frac = 1e99
max_on = 0

for ibin in xrange(hs[0].FindBin(1000), nbins+1):
    for jbin in xrange(ibin, nbins+1):
        integs = {ht : get_integral(h, ibin, jbin, x_are_bins=True) for ht,h in zip(hts,hs)}
        off = integs[500][0] + integs[700][0] + integs[2000][0]
        offe = (integs[500][1]**2 + integs[700][1]**2 + integs[2000][1]**2)**0.5
        on = integs[1000][0] + integs[1500][0]
        one = (integs[1000][1]**2 + integs[1500][1]**2)**0.5
        frac = off / (on + off)
        prnt = 0
        if frac < min_frac:
            min_frac = frac
            prnt = 1
        if on > max_on:
            max_on = on
            prnt = 1
        if prnt:
            print '%.0f-%.0f  %10.1f +- %6.1f  %10.1f +- %6.1f -> %.3f' % (xax.GetBinLowEdge(ibin), xax.GetBinLowEdge(jbin+1), off, offe, on, one, frac)
