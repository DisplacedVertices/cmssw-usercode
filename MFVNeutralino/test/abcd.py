#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *

def abcd(A, eA, B, eB, C, eC, D, eD, s=1):
    if A == 0:
        Dpred = 1e9
    else:
        Dpred = B/A*C

    if A == 0 or B == 0 or C == 0:
        eDpred = 1e9
    else:
        eDpred = Dpred * ((eA/A)**2 + (eB/B)**2 + (eC/C)**2)**0.5

    return s*A, s*eA, s*B, s*eB, s*C, s*eC, s*D, s*eD, s*Dpred, s*eDpred
    
def abcd_from_file(filename, histpath, xcut, ycut, s=1):
    file = ROOT.TFile(filename)
    hist = file.Get(histpath)

    xbin = hist.GetXaxis().FindBin(xcut)
    ybin = hist.GetYaxis().FindBin(ycut)

    nbinsx = hist.GetNbinsX()
    nbinsy = hist.GetNbinsY()

    eA = ROOT.Double(0)
    eB = ROOT.Double(0)
    eC = ROOT.Double(0)
    eD = ROOT.Double(0)
    A = hist.IntegralAndError(0, xbin-1, 0, ybin-1, eA)
    B = hist.IntegralAndError(0, xbin-1, ybin, nbinsy+1, eB)
    C = hist.IntegralAndError(xbin, nbinsx+1, 0, ybin-1, eC)
    D = hist.IntegralAndError(xbin, nbinsx+1, ybin, nbinsy+1, eD)

    return abcd(A, eA, B, eB, C, eC, D, eD, s)

def to_raw(A, eA, B, eB, C, eC, D, eD):
    NA = (A/eA)**2
    NB = (B/eB)**2
    NC = (C/eC)**2
    ND = (D/eD)**2
    return NA, NA**0.5, NB, NB**0.5, NC, NC**0.5, ND, ND**0.5

def write_datacard(filename, n_obs, n_bkg, sig_eff, n_side, alpha):
    template = '''
imax 1  number of channels
jmax 1  number of backgrounds 
kmax 3  number of nuisance parameters (sources of systematical uncertainties)
------------
bin         1
observation %(n_obs)i
------------
bin             1      1
process       Sig  Bkg 
process         0      1
rate           %(n_sig_1fb)g     %(n_bkg)g
------------
lumi    lnN    1.022    -
xs_sig  lnN    1.33     -
#bg_sig  lnN    -        1.30
bg_ext  gmN %(n_side)i -        %(alpha)g
'''

    int_lumi = 20.
    n_sig_1fb = sig_eff*int_lumi
    open(filename, 'wt').write(template % locals())

def poisson_ratio_sigma(num, den):
    r,l,h = clopper_pearson_poisson_means(num, den)
    return (h-l)/2

def print_abcd(bn):
    A,eA,B,eB,C,eC,D,eD,Dpred,eDpred = abcd_from_file('/uscms/home/tucker/jen/crab/ABCDHistosV17_5/%s.root' % bn, 'mfvAbcdHistosTrksJets/h_svdist2d_ntracks01', 16, 0.04)
    NA, eNA, NB, eNB, NC, eNC, ND, eND = to_raw(A,eA,B,eB,C,eC,D,eD)
    NDpred, eNDpred = abcd(NA, eNA, NB, eNB, NC, eNC, ND, eND)[-2:]

    print bn
    print 'A    : %9.2f +- %9.2f  (%9.2f +- %9.2f)' % (A, eA, NA, eNA)
    print 'B    : %9.2f +- %9.2f  (%9.2f +- %9.2f)' % (B, eB, NB, eNB)
    print 'C    : %9.2f +- %9.2f  (%9.2f +- %9.2f)' % (C, eC, NC, eNC)
    print 'D    : %9.2f +- %9.2f  (%9.2f +- %9.2f)' % (D, eD, ND, eND)
    print 'Dpred: %9.2f +- %9.2f  (%9.2f +- %9.2f)' % (Dpred, eDpred, NDpred, eNDpred)
    print 'B/A  : %9.2f +- %9.2f  (%9.2f +- %9.2f)' % (B/A, poisson_ratio_sigma(B, A), NB/NA, poisson_ratio_sigma(NB, NA))
    print 'C/A  : %9.2f +- %9.2f  (%9.2f +- %9.2f)' % (C/A, poisson_ratio_sigma(C, A), NC/NA, poisson_ratio_sigma(NC, NA))
    print 'D/20 : %9.2f +- %9.2f' % (D/20, eD/20)
    print

    write_datacard(bn + '.txt', 23, 23, round(D/20/20*100)/100, 25, 0.92)

bns = [
    'ttbar_sq_qcdht1000_scaled',
#    'mfv_neutralino_tau0100um_M0200_scaled',
#    'mfv_neutralino_tau0100um_M0300_scaled',
#    'mfv_neutralino_tau0100um_M0400_scaled',
#    'mfv_neutralino_tau0100um_M0600_scaled',
#    'mfv_neutralino_tau0100um_M0800_scaled',
#    'mfv_neutralino_tau0100um_M1000_scaled',
#    'mfv_neutralino_tau0300um_M0200_scaled',
#    'mfv_neutralino_tau0300um_M0300_scaled',
#    'mfv_neutralino_tau0300um_M0400_scaled',
#    'mfv_neutralino_tau0300um_M0600_scaled',
#    'mfv_neutralino_tau0300um_M0800_scaled',
#    'mfv_neutralino_tau0300um_M1000_scaled',
#    'mfv_neutralino_tau1000um_M0200_scaled',
#    'mfv_neutralino_tau1000um_M0300_scaled',
    'mfv_neutralino_tau1000um_M0400_scaled',
#    'mfv_neutralino_tau1000um_M0600_scaled',
#    'mfv_neutralino_tau1000um_M0800_scaled',
#    'mfv_neutralino_tau1000um_M1000_scaled',
#    'mfv_neutralino_tau9900um_M0200_scaled',
#    'mfv_neutralino_tau9900um_M0300_scaled',
#    'mfv_neutralino_tau9900um_M0400_scaled',
#    'mfv_neutralino_tau9900um_M0600_scaled',
#    'mfv_neutralino_tau9900um_M0800_scaled',
#    'mfv_neutralino_tau9900um_M1000_scaled',
    ]

for bn in bns:
    print_abcd(bn)
