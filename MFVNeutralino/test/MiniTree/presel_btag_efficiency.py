from JMTucker.Tools.ROOTTools import *

year = 2018
version = 'V25m'

f_btageff = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/BTagEff%sv1/background_%s.root' % (version, year) )
f_presel = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/PreselHistos%s/background_%s.root' % (version, year))

def njets(hname):
  h = f_btageff.Get(hname)
  return h.Integral(0, h.GetNbinsX()+1, 0, h.GetNbinsY()+1)

def btag_eff_per_jet(jet_flavor, bdisc):
  num = njets('JMTBTagEfficiency/num_%s_%s' % (jet_flavor, bdisc))
  den = njets('JMTBTagEfficiency/den_%s' % jet_flavor)
  return num/den

def scale_factor(jet_flavor, bdisc):
  h = f_btageff.Get('JMTBTagEfficiency/scalefactor_%s_%s' % (jet_flavor, bdisc))
  return h.GetMean()

def btag_eff_per_event_from_btag_eff_per_jet(event_flavor, effb, effc, effl):
  num = 0
  den = 0
  h_nlcb = f_btageff.Get('JMTBTagEfficiency/h_nlcb')
  for nl in range(0, h_nlcb.GetNbinsX()):
    for nc in range(0, h_nlcb.GetNbinsY()):
      for nb in range(0, 1) if event_flavor == 'nobjets' else range(1, h_nlcb.GetNbinsZ()):
        nlcb = h_nlcb.GetBinContent(nl+1, nc+1, nb+1)
        num += nlcb * (1 - (1-effb)**nb * (1-effc)**nc * (1-effl)**nl)
        den += nlcb
  return num/den

def btag_eff_per_event(event_flavor, bdisc):
  (firstxbin,lastxbin) = (3,3) if event_flavor == 'bquarks' else (1,2)
  h = f_presel.Get('mfvEventHistosJetPreSel/h_nbtags_v_bquark_code_%s' % bdisc).ProjectionY('h_nbtags', firstxbin, lastxbin)
  return h.Integral(2,4)/h.Integral(1,4)

print 'preselected events'
print '%10s%90s%26s%26s%26s' % ('', 'per-jet', 'per-event from per-jet', 'per-event from per-jet*SF', 'per-event')
fmt = '%10s' + '%10s'*9 + '%13s'*6
print fmt % ('', 'effb', 'SFb', 'effb*SFb', 'effc', 'SFc', 'effc*SFc', 'effl', 'SFl', 'effl*SFl', 'btag eff', 'fake rate', 'btag eff', 'fake rate', 'btag eff', 'fake rate')
for bdisc in ['0', '1', '2']:
  effb, sfb = btag_eff_per_jet('bottom', bdisc), scale_factor('bottom', bdisc)
  effc, sfc = btag_eff_per_jet('charm', bdisc), scale_factor('charm', bdisc)
  effl, sfl = btag_eff_per_jet('light', bdisc), scale_factor('light', bdisc)
  print fmt % (bdisc, '%.3f' % effb, '%.3f' % sfb, '%.3f' % (effb*sfb),
                      '%.3f' % effc, '%.3f' % sfc, '%.3f' % (effc*sfc),
                      '%.3f' % effl, '%.3f' % sfl, '%.3f' % (effl*sfl),
                      '%.3f' % btag_eff_per_event_from_btag_eff_per_jet('bjets', effb, effc, effl),
                      '%.3f' % btag_eff_per_event_from_btag_eff_per_jet('nobjets', effb, effc, effl),
                      '%.3f' % btag_eff_per_event_from_btag_eff_per_jet('bjets', effb*sfb, effc*sfc, effl*sfl),
                      '%.3f' % btag_eff_per_event_from_btag_eff_per_jet('nobjets', effb*sfb, effc*sfc, effl*sfl),
                      '%.3f' % btag_eff_per_event('bquarks', bdisc),
                      '%.3f' % btag_eff_per_event('nobquarks', bdisc))
