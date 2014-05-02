#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import ROOT

def abcd(filename, histpath, xcut, ycut, s=1):
    file = ROOT.TFile(filename)
    hist = file.Get(histpath)

    xbin = hist.GetXaxis().FindBin(xcut)
    ybin = hist.GetYaxis().FindBin(ycut)

    nbinsx = hist.GetNbinsX()
    nbinsy = hist.GetNbinsY()

    errA = ROOT.Double(0)
    errB = ROOT.Double(0)
    errC = ROOT.Double(0)
    errD = ROOT.Double(0)
    A = hist.IntegralAndError(0, xbin-1, 0, ybin-1, errA)
    B = hist.IntegralAndError(0, xbin-1, ybin, nbinsy+1, errB)
    C = hist.IntegralAndError(xbin, nbinsx+1, 0, ybin-1, errC)
    D = hist.IntegralAndError(xbin, nbinsx+1, ybin, nbinsy+1, errD)

    if A == 0:
        Dpred = 1e9
    else:
        Dpred = B/A*C
    if A == 0 or B == 0 or C == 0:
        errDpred = 1e9
    else:
        errDpred = Dpred * (errA/A * errA/A + errB/B * errB/B + errC/C * errC/C)**0.5

    return s*A, s*errA, s*B, s*errB, s*C, s*errC, s*D, s*errD, s*Dpred, s*errDpred

print abcd('crab/ABCDHistosV17_0/background_scaled.root', 'abcdHistosTrksJets/h_svdist2d_ntracks01', 15, 0.04)
