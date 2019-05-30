#!/usr/bin/env python

from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.Year import year

settings = CMSSWSettings()
settings.is_mc = True

global_tag(process, which_global_tag(settings))
tfileservice(process, 'btageff.root')
sample_files(process, 'qcdht2000_%s' % year, 'miniaod', 1)
cmssw_from_argv(process)

process.load('PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi')
process.load('JMTucker.Tools.MCStatProducer_cff')
process.load('JMTucker.Tools.PATTupleSelection_cfi')
process.load('JMTucker.Tools.UpdatedJets_cff')
process.load('JMTucker.Tools.WeightProducer_cfi')

process.selectedPatJets.src = 'updatedJetsMiniAOD'
process.selectedPatJets.cut = process.jtupleParams.jetCut

process.JMTBTagEfficiency = cms.EDAnalyzer('JMTBTagEfficiency',
                                           weight_src = cms.InputTag('jmtWeightMiniAOD'),
                                           jets_src = cms.InputTag('selectedPatJets'),
                                           jet_pt_min = cms.double(20),
                                           b_discriminator = cms.string(str(year)),
                                           )

process.p = cms.Path(process.JMTBTagEfficiency)

if year == 2017:
    process.JMTBTagEfficiencyOld = process.JMTBTagEfficiency.clone(b_discriminator = '2017old')
    process.p *= process.JMTBTagEfficiencyOld

from JMTucker.MFVNeutralino.EventFilter import setup_event_filter
setup_event_filter(process, input_is_miniaod=True, mode='jets only novtx', event_filter_jes_mult=0)

ReferencedTagsTaskAdder(process)('p')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples 

    if year == 2017:
        samples = Samples.qcd_samples_2017 + Samples.ttbar_samples_2017
    elif year == 2018:
        samples = Samples.qcd_samples_2018 + Samples.ttbar_samples_2018

    set_splitting(samples, 'miniaod', 'default', default_files_per=16)

    ms = MetaSubmitter('BTagEffV25mv1', dataset='miniaod')
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    ms.submit(samples)

elif __name__ == '__main__' and hasattr(sys, 'argv') and 'ana' in sys.argv:
    from JMTucker.Tools.ROOTTools import *
    fn = root_fns_from_argv()[0]
    f = ROOT.TFile(fn, 'update')
    d = f.GetDirectory('JMTBTagEfficiency')
    d.cd()
    nwp = len(process.JMTBTagEfficiency.b_discriminator_min)
    for kind in 'light', 'charm', 'bottom':
        den = d.Get('den_%s' % kind)
        nx, ny = den.GetNbinsX(), den.GetNbinsY()

        for wp in xrange(nwp):
            num = d.Get('num_%s_%i' % (kind, wp))

            # check there are no eta overflows
            for ibin in [0, nx+1]:
                for jbin in xrange(1, ny+1):
                    assert num.GetBinContent(ibin,jbin) == 0 and den.GetBinContent(ibin,jbin) == 0

            eff = num.Clone('eff_%s_%i' % (kind, wp))
            for ibin in xrange(1, nx+1):
                for jbin in xrange(1, ny+2):
                    a = num.GetBinContent(ibin,jbin)
                    b = den.GetBinContent(ibin,jbin)
                    ea = num.GetBinError(ibin,jbin)
                    eb = den.GetBinError(ibin,jbin)
                    if b == 0 or ea == 0 or eb == 0:
                        # set pt overflow eff to the same-eta previous pt bin if empty
                        assert jbin == ny+1
                        eff.SetBinContent(ibin,jbin, eff.GetBinContent(ibin,ny))
                        eff.SetBinError  (ibin,jbin, eff.GetBinError  (ibin,ny))
                    else:
                        a = (a/ea)**2
                        b = (b/eb)**2
                        e,l,u = clopper_pearson(a,b)
                        ee = (u-l)/2
                        eff.SetBinContent(ibin,jbin, e)
                        eff.SetBinError  (ibin,jbin, ee)
            eff.Write()
