import sys, os
running_script = __name__ == '__main__' and hasattr(sys, 'argv')
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/user/tucker/mfvneutralino_genfsimreco_tau1mm/mfvneutralino_genfsimreco_tau1mm/f0b5b0c98c357fc0015e0194f7aef803/fastsim_47_1_0c1.root']
process.TFileService.fileName = 'simple_trigger_efficiency.root'

process.genMuons = cms.EDFilter('CandViewSelector', src = cms.InputTag('genParticles'), cut = cms.string('abs(pdgId) == 13 && abs(mother.pdgId) == 24'))
process.genMuonCount = cms.EDFilter('CandViewCountFilter', src = cms.InputTag('genMuons'), minNumber = cms.uint32(1))
                                
process.genMuonsInAcc = cms.EDFilter('CandViewSelector', src = cms.InputTag('genParticles'), cut = cms.string('abs(pdgId) == 13 && abs(mother.pdgId) == 24 && pt > 17 && abs(eta) < 2.1'))
process.genMuonInAccCount = cms.EDFilter('CandViewCountFilter', src = cms.InputTag('genMuonsInAcc'), minNumber = cms.uint32(1))

process.SimpleTriggerEfficiency = cms.EDAnalyzer('SimpleTriggerEfficiency', trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'))
process.SimpleTriggerEfficiencyMu = process.SimpleTriggerEfficiency.clone()
process.SimpleTriggerEfficiencyMuInAcc = process.SimpleTriggerEfficiency.clone()

process.p1 = cms.Path(process.SimpleTriggerEfficiency)
process.p2 = cms.Path(process.genMuons      * process.genMuonCount      * process.SimpleTriggerEfficiencyMu)
process.p3 = cms.Path(process.genMuonsInAcc * process.genMuonInAccCount * process.SimpleTriggerEfficiencyMuInAcc)

################################################################################

def get_f():
    try:
        fn = [x for x in sys.argv[1:] if x.endswith('.root')][0]
    except IndexError:
        fn = process.TFileService.fileName.value()
    if not os.path.isfile(fn):
        print 'need a input file! (%s not found)' % fn
        sys.exit(1)

    f = ROOT.TFile(fn)
    return f

def get_hists(f, dn):
    hnum = f.Get(dn).Get('triggers_pass_num')
    hden = f.Get(dn).Get('triggers_pass_den')
    return hnum, hden

if running_script and 'table' in sys.argv:
    from JMTucker.Tools.ROOTTools import ROOT
    f = get_f()
    hnum, hden = get_hists(f, 'SimpleTriggerEfficiencyMuInAcc')
    print 'number of events:', hden.GetBinContent(1)

    apply_prescales = True
    
    from JMTucker.Tools.ROOTTools import clopper_pearson
    import prescales
    width = 0
    content = []
    for i in xrange(1, hden.GetNbinsX() + 1):
        path = hden.GetXaxis().GetBinLabel(i)
        width = max(width, len(path))

        num = hnum.GetBinContent(i)
        den = hden.GetBinContent(i)
        eff, lo, hi = clopper_pearson(num, den)

        l1, hlt, overall = prescales.get(path)
            
        if apply_prescales:
            if overall > 0:
                eff /= overall
                lo /= overall
                hi /= overall
            else:
                eff = lo = hi = 0.

        content.append((i-1, path, eff, lo, hi, l1, hlt, overall))

    fmt = '(%3i) %' + str(width + 2) + 's %.4f  68%% CL: [%.4f, %.4f]  (prescales: %10i * %10i = %10i )'

    print 'sorted by trigger bit:'
    for c in content:
        print fmt % c
    print
    print 'sorted by decreasing eff:'
    content.sort(key=lambda x: x[2], reverse=True)
    for c in content:
        print fmt % c

################################################################################
            
if running_script and 'compare' in sys.argv:
    from JMTucker.Tools.ROOTTools import ROOT, set_style, plot_saver, histogram_divide
    set_style()
    ps = plot_saver('plots/mfv_simple_eff')
    
    f = get_f()
    hnum,    hden    = get_hists(f, 'SimpleTriggerEfficiency')
    hnum_mu, hden_mu = get_hists(f, 'SimpleTriggerEfficiencyMu')

    eff_all = histogram_divide(hnum,    hden)
    eff_mu  = histogram_divide(hnum_mu, hden_mu)

    eff_all.SetLineColor(ROOT.kRed)
    eff_all.Draw('APL')
    eff_mu.SetLineColor(ROOT.kBlue)
    eff_mu.Draw('P same')
    ps.save('compare')

################################################################################
            
if running_script and 'submit' in sys.argv:
    pass
