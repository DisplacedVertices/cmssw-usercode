import sys, os
running_script = __name__ == '__main__' and hasattr(sys, 'argv')
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/user/tucker/mfvneutralino_genfsimreco_tau1mm/mfvneutralino_genfsimreco_tau1mm/f0b5b0c98c357fc0015e0194f7aef803/fastsim_47_1_0c1.root']
process.TFileService.fileName = 'simple_trigger_efficiency.root'

process.SimpleTriggerEfficiency = cms.EDAnalyzer('SimpleTriggerEfficiency', trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'))
process.p = cms.Path(process.SimpleTriggerEfficiency)

################################################################################

if running_script and 'analyze' in sys.argv:
    try:
        fn = [x for x in sys.argv[1:] if x.endswith('.root')][0]
    except IndexError:
        fn = process.TFileService.fileName.value()
    if not os.path.isfile(fn):
        print 'need a input file! (%s not found)' % fn
        sys.exit(1)

    from JMTucker.Tools.ROOTTools import ROOT, clopper_pearson
    f = ROOT.TFile(fn)
    hnum = f.Get('SimpleTriggerEfficiency/triggers_pass_num')
    hden = f.Get('SimpleTriggerEfficiency/triggers_pass_den')

    print 'number of events:', hden.GetBinContent(1)
    
    width = 0
    content = []
    for i in xrange(1, hden.GetNbinsX() + 1):
        path = hden.GetXaxis().GetBinLabel(i)
        width = max(width, len(path))

        num = hnum.GetBinContent(i)
        den = hden.GetBinContent(i)
        eff, lo, hi = clopper_pearson(num, den)

        content.append((i-1, path, eff, lo, hi))

    fmt = '(%3i) %' + str(width + 2) + 's %.4f  [%.4f, %.4f]'

    print 'sorted by trigger bit:'
    for c in content:
        print fmt % c
    print
    print 'sorted by decreasing eff:'
    content.sort(key=lambda x: x[2], reverse=True)
    for c in content:
        print fmt % c

################################################################################
            
if running_script and 'submit' in sys.argv:
    pass
