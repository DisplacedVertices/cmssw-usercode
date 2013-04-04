import sys, os
running_script = __name__ == '__main__' and hasattr(sys, 'argv')
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

from JMTucker.MFVNeutralino.SimFiles import load as load_files
load_files(process, 'tau9900um_M0400', 'all', sec_files = False)
process.TFileService.fileName = 'simple_trigger_efficiency.root'

process.genMus = cms.EDFilter('CandViewSelector', src = cms.InputTag('genParticles'), cut = cms.string('abs(pdgId) == 13 && abs(mother.pdgId) == 24'))
process.genMuCount = cms.EDFilter('CandViewCountFilter', src = cms.InputTag('genMus'), minNumber = cms.uint32(1))
                                
process.genEls = cms.EDFilter('CandViewSelector', src = cms.InputTag('genParticles'), cut = cms.string('abs(pdgId) == 11 && abs(mother.pdgId) == 24'))
process.genElCount = cms.EDFilter('CandViewCountFilter', src = cms.InputTag('genEls'), minNumber = cms.uint32(1))
                                
process.genMusInAcc = cms.EDFilter('CandViewSelector', src = cms.InputTag('genParticles'), cut = cms.string('abs(pdgId) == 13 && abs(mother.pdgId) == 24 && pt > 26 && abs(eta) < 2.1'))
process.genElsInAcc = cms.EDFilter('CandViewSelector', src = cms.InputTag('genParticles'), cut = cms.string('abs(pdgId) == 11 && abs(mother.pdgId) == 24 && pt > 30 && abs(eta) < 2.5'))
process.genMuInAccCount = cms.EDFilter('CandViewCountFilter', src = cms.InputTag('genMusInAcc'), minNumber = cms.uint32(1))
process.genElInAccCount = cms.EDFilter('CandViewCountFilter', src = cms.InputTag('genElsInAcc'), minNumber = cms.uint32(1))

process.RandomNumberGeneratorService = cms.Service('RandomNumberGeneratorService')
process.RandomNumberGeneratorService.SimpleTriggerEfficiency = cms.PSet(initialSeed = cms.untracked.uint32(1219))
process.RandomNumberGeneratorService.SimpleTriggerEfficiencyMu = cms.PSet(initialSeed = cms.untracked.uint32(1220))
process.RandomNumberGeneratorService.SimpleTriggerEfficiencyMuInAcc = cms.PSet(initialSeed = cms.untracked.uint32(1221))

#import prescales
process.SimpleTriggerEfficiency = cms.EDAnalyzer('SimpleTriggerEfficiency',
                                                 trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                                                 prescale_paths = cms.vstring(), #*prescales.prescales.keys()),
                                                 prescale_values = cms.vuint32(), #*[o for l,h,o in prescales.prescales.itervalues()]),
                                                 )

process.SimpleTriggerEfficiencyMu      = process.SimpleTriggerEfficiency.clone()
process.SimpleTriggerEfficiencyMuInAcc = process.SimpleTriggerEfficiency.clone()
process.SimpleTriggerEfficiencyEl      = process.SimpleTriggerEfficiency.clone()
process.SimpleTriggerEfficiencyElInAcc = process.SimpleTriggerEfficiency.clone()

process.p1 = cms.Path(process.SimpleTriggerEfficiency)
process.p2 = cms.Path(process.genMus      * process.genMuCount      * process.SimpleTriggerEfficiencyMu)
process.p3 = cms.Path(process.genMusInAcc * process.genMuInAccCount * process.SimpleTriggerEfficiencyMuInAcc)
process.p4 = cms.Path(process.genEls      * process.genElCount      * process.SimpleTriggerEfficiencyEl)
process.p5 = cms.Path(process.genElsInAcc * process.genElInAccCount * process.SimpleTriggerEfficiencyElInAcc)

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

def get_hists(f, dn, twod=False):
    hnum = f.Get(dn).Get('triggers%s_pass_num' % ('2d' if twod else ''))
    hden = f.Get(dn).Get('triggers%s_pass_den' % ('2d' if twod else ''))
    return hnum, hden

################################################################################

if running_script and 'table' in sys.argv:
    from JMTucker.Tools.ROOTTools import ROOT, clopper_pearson
    apply_prescales = False
    apply_prescales_in_sort = True

    f = get_f()
    hnum, hden = get_hists(f, 'SimpleTriggerEfficiencyMuInAcc')
    print 'number of events:', hden.GetBinContent(1)
    
    width = 0
    content = []
    for i in xrange(1, hden.GetNbinsX() + 1):
        path = hden.GetXaxis().GetBinLabel(i)
        width = max(width, len(path))

        num = hnum.GetBinContent(i)
        den = hden.GetBinContent(i)
        eff, lo, hi = clopper_pearson(num, den)

        prescaled_eff = 1
        
        if apply_prescales:
            import prescales
            l1, hlt, overall = prescales.get(path)
            if overall > 0:
                eff /= overall
                lo /= overall
                hi /= overall
            elif overall == 0:
                eff = lo = hi = 0.
        else:
            l1, hlt, overall = -1, -1, -1

        content.append((i-1, path, eff, lo, hi, l1, hlt, overall, prescaled_eff))

    fmt = '(%3i) %' + str(width + 2) + 's %.4f  68%% CL: [%.4f, %.4f]   after prescales: (%10i * %10i = %10i):  %.4f'

    print 'sorted by trigger bit:'
    for c in content:
        print fmt % c
    print
    print 'sorted by decreasing eff',
    if apply_prescales_in_sort:
        print '(after applying prescales):'
        key = lambda x: x[-1]
    else:
        print ':'
        key = lambda x: x[2]
    print '(applying prescales):' if apply_prescales_in_sort else ':'
    content.sort(key=key, reverse=True)
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
            
if running_script and '2d' in sys.argv:
    from JMTucker.Tools.ROOTTools import ROOT, set_style, plot_saver, histogram_divide
    set_style()
    ps = plot_saver('plots/mfv_simple_eff')

    apply_prescales = False
    import prescales

    f = get_f()
    hnum, hden = get_hists(f, 'SimpleTriggerEfficiencyMuInAcc', twod=True)
    hnum.Divide(hden)
    xax, yax = hnum.GetXaxis(), hnum.GetYaxis()
    for x in xrange(1, xax.GetNbins()+1):
        for y in xrange(1, yax.GetNbins()+1):
            xpath = xax.GetBinLabel(x)
            ypath = yax.GetBinLabel(y)
            

################################################################################
            
if running_script and 'submit' in sys.argv:
    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = condor

[CMSSW]
%(dbs_url)s
datasetpath = %(dataset)s
pset = simple_trigger_efficiency.py
%(job_control)s

[USER]
ui_working_dir = crab/simple_trigger_efficiency/crab_ste_%(name)s
return_data = 1
'''

    os.system('mkdir -p crab/simple_trigger_efficiency')
    just_testing = 'testing' in sys.argv

    def submit(sample):
        #new_py = open('simple_trigger_efficiency.py').read()
        #open('simple_trigger_efficiency_crab.py', 'wt').write(new_py)
        open('crab.cfg', 'wt').write(crab_cfg % sample)
        if not just_testing:
            os.system('crab -create -submit')
            os.system('rm -f crab.cfg simple_trigger_efficiency_crab.py simple_trigger_efficiency_crab.pyc')
        else:
            print '.py diff:\n---------'
            os.system('diff -uN simple_trigger_efficiency.py simple_trigger_efficiency_crab.py')
            raw_input('ok?')
            print '\ncrab.cfg:\n---------'
            os.system('cat crab.cfg')
            raw_input('ok?')
            print

    from JMTucker.Tools.Samples import mfv_signal_samples
    for sample in mfv_signal_samples:
        submit(sample)
