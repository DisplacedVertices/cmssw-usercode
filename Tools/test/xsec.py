from JMTucker.Tools.BasicAnalyzer_cfg import *

remove_tfileservice(process)
cmssw_from_argv(process)

add_analyzer(process, 'GenXSecAnalyzer')
add_analyzer(process, 'JMTLHEGenInfo', use_lhe=cms.bool(False))


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.qcd_samples_2017 + Samples.ttbar_samples_2017 + Samples.leptonic_samples_2017
    
    for s in samples:
        s.datasets['miniaod'].split_by = 'events'
        s.datasets['miniaod'].events_per = 1000000

    cs = CondorSubmitter('XsecV1', dataset='miniaod', _njobs=1)
    cs.submit_all(samples)
