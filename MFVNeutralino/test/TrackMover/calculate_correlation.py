#!/usr/bin/env python


import sys, os
import numpy as np
from JMTucker.Tools.ROOTTools import *
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac

def properfn(eta):
  fns = [os.path.join(os.path.abspath('/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_%sEta_LowdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6' % eta), sn + '_2017p8.root') for sn in ' VHToSSTodddd_tau1mm_M55  '.split()]
  fns += [os.path.join(os.path.abspath('/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_%sEta_LowdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6' % eta), sn + '_2017p8.root') for sn in ' ggHToSSTodddd_tau1mm_M55  mfv_stopdbardbar_tau001000um_M0200  '.split()]
  return fns


def effs(fn):
    
    
    f = ROOT.TFile(fn)

    def get_num(nvtx):
      if (nvtx == 1.0):
          h = f.Get('all_dvv_num')
      else:
          h = f.Get('all_dvv_2vtx_num')
      return h.Integral(0,999)  

    def get_den(nvtx):
      if (nvtx == 1.0):
          h = f.Get('all_dvv_den')
      else:
          h = f.Get('all_dvv_2vtx_den')
      return h.Integral(0,999)  
    
    onenum = get_num(1.0) 
    oneden = get_den(1.0) + 1e-16
    twonum = get_num(2.0)
    twoden = get_den(2.0) + 1e-16
    

    onevtxeff = onenum/oneden
    onevtxeff_err = np.sqrt((onevtxeff * (1.0 -  onevtxeff))/oneden)
    twovtxeff = twonum/twoden
    twovtxeff_err = np.sqrt((twovtxeff * (1.0 -  twovtxeff))/twoden)
    corr = (1.0 - (twovtxeff/(onevtxeff*onevtxeff + (1e-16))))

    row_line = '& $%.3f\pm%.3f$ & $%.3f\pm%.3f$ & $%.2f$' % (onevtxeff, onevtxeff_err, twovtxeff, twovtxeff_err, corr) 
    return row_line

row_lines = ['' for i in range(len(properfn('Low')))]  
for eta in ['Low', 'Mix', 'High']:
  fns = properfn(eta)
  for j in range(len(fns)):
    row_lines[j] += effs(fns[j])

for i in range(len(properfn('Low'))):
  print(properfn('Low')[i])
  print(row_lines[i]+'\\\\')
    
