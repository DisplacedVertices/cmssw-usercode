#!/usr/bin/env python

import os
os.environ['JMT_ROOTTOOLS_NOBATCHMODE'] = 'y'
from JMTucker.Tools.ROOTTools import *
set_style()
cmssw_setup()
_b = ROOT.TBrowser()


from JMTucker.Tools.Samples import *
samples = (qcdht0100, qcdht0250, qcdht0500, qcdht1000, ttbarhadronic, ttbarsemilep, ttbardilep)
samples2num = dict(zip(samples, xrange(len(samples))))
samples = dict(zip(xrange(len(samples)), samples))


#f_bkg = ROOT.TFile('root://cmseos.fnal.gov//store/user/tucker/minintuplev18_background.root')
f_bkg = ROOT.TFile('minintuple.root')
events_bkg = f_bkg.Get('Events')

def set_aliases(t):
    t.SetAlias('si_sample', 'int_mfvSampleInfo_sample_Mini.obj')
    t.SetAlias('si_weight', 'double_mfvSampleInfo_weight_Mini.obj')
    t.SetAlias('si_partialw', 'double_mfvSampleInfo_partialWeight_Mini.obj')
    t.SetAlias('si_lumiw', 'double_mfvSampleInfo_lumiWeight_Mini.obj')
    t.SetAlias('si_extraw', 'double_mfvSampleInfo_extraWeight_Mini.obj')
    t.SetAlias('si_xsec', 'double_mfvSampleInfo_crossSection_Mini.obj')
    t.SetAlias('si_nevents', 'int_mfvSampleInfo_numEvents_Mini.obj')

    t.SetAlias('vtx', 'MFVVertexAuxs_mfvSelectedVerticesTight__Mini.obj')
    t.SetAlias('vtx_size', 'MFVVertexAuxs_mfvSelectedVerticesTight__Mini.@obj.size()')
    t.SetAlias('evt', 'MFVEvent_mfvEvent__PAT.obj')

set_aliases(events_bkg)

#events_bkg.Scan('id_run:id_lumi:id_event:si_sample:si_nevents:si_xsec:si_weight')

onev = 'vtx_size >= 1'
twov = 'vtx_size >= 2'

t = events_bkg
