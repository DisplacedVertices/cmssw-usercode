from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset

input_files(process, '/uscms/home/pkotamni/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/ntuple.root')
tfileservice(process, 'histos.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.VertexHistos_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

# Enable per-flavor trigger SF variation weights
process.mfvWeight.produce_variation_weights = cms.bool(True)

# common: vertex selection + nominal weight computation
common = cms.Sequence(process.mfvSelectedVerticesSeq * process.mfvWeight)

# ntk>=5, >=2 tight vertices (standard FullSel)
process.mfvAnalysisCutsFullSel = process.mfvAnalysisCuts.clone()

# Five weight variations: nominal + mu trig up/down + el trig up/down
variations = [
    ('Nominal',    cms.InputTag('mfvWeight')),
    ('MuTrigUp',   cms.InputTag('mfvWeight', 'weightMuTrigUp')),
    ('MuTrigDown', cms.InputTag('mfvWeight', 'weightMuTrigDown')),
    ('ElTrigUp',   cms.InputTag('mfvWeight', 'weightElTrigUp')),
    ('ElTrigDown', cms.InputTag('mfvWeight', 'weightElTrigDown')),
]

for var_name, weight_tag in variations:
    histo = process.mfvVertexHistos.clone(weight_src = weight_tag)
    histo_name = 'mfvVertexHistosFullSel' + var_name
    setattr(process, histo_name, histo)
    path = cms.Path(common * process.mfvAnalysisCutsFullSel * getattr(process, histo_name))
    setattr(process, 'pFullSel' + var_name, path)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.Samples import *
    from JMTucker.Tools.Year import year

    all_lep_for_year = {
        20161: all_lep_signal_samples_20161,
        20162: all_lep_signal_samples_20162,
        2017:  all_lep_signal_samples_2017,
        2018:  all_lep_signal_samples_2018,
    }[year]

    # Benchmark signal points: VH (ZH+WH+ggZH) M55 1mm/10mm/300um, M40 1mm + ttH dddd M55 10mm
    benchmark_pats = [
        'ZHToSSTodddd_tau1mm_M55',
        'ZHToSSTodddd_tau10mm_M55',
        'ZHToSSTodddd_tau300um_M55',
        'ZHToSSTodddd_tau1mm_M40',
        'WplusHToSSTodddd_tau1mm_M55',
        'WplusHToSSTodddd_tau10mm_M55',
        'WplusHToSSTodddd_tau300um_M55',
        'WplusHToSSTodddd_tau1mm_M40',
        'WminusHToSSTodddd_tau1mm_M55',
        'WminusHToSSTodddd_tau10mm_M55',
        'WminusHToSSTodddd_tau300um_M55',
        'WminusHToSSTodddd_tau1mm_M40',
        'ggZHToSSTodddd_tau1mm_M55',
        'ggZHToSSTodddd_tau10mm_M55',
        'ggZHToSSTodddd_tau300um_M55',
        'ggZHToSSTodddd_tau1mm_M40',
        'ttHToLLPs_dddd_tau10mm_M55',
    ]

    samples = [s for s in all_lep_for_year if any(pat in s.name for pat in benchmark_pats)]

    pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), ttH_duplicate_check_modifier)

    set_splitting(samples, dataset, 'histos', data_json=json_path('ana_run2.json'))

    cs = CondorSubmitter('LepTrigSF_' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)
