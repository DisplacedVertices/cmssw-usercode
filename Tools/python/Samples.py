#!/usr/bin/env python

from JMTucker.Tools.CMSSWTools import cmssw_base
from JMTucker.Tools.Sample import *

########################################################################

def _model(sample):
    s = sample if type(sample) == str else sample.name
    return s.split('_tau')[0]

def _tau(sample):
    s = sample if type(sample) == str else sample.name
    is_um = '0um_' in s
    x = int(s[s.index('tau')+3:s.index('um_' if is_um else 'mm_')])
    if not is_um:
        x *= 1000
    return x

def _mass(sample):
    s = sample if type(sample) == str else sample.name
    x = s.index('_M')
    y = s.find('_',x+1)
    if y == -1:
        y = len(s)
    return int(s[x+2:y])

def _decay(sample):
    s = sample if type(sample) == str else sample.name
    decay = {
        'mfv_neu': r'\tilde{N} \rightarrow tbs',
        'xx4j': r'X \rightarrow q\bar{q}',
        'mfv_ddbar': r'\tilde{g} \rightarrow d\bar{d}',
        'mfv_neuuds': r'\tilde{N} \rightarrow uds',
        'mfv_neuudmu': r'\tilde{N} \rightarrow u\bar{d}\mu^{\minus}',
        'mfv_neuude': r'\tilde{N} \rightarrow u\bar{d}e^{\minus}',
        'mfv_neucdb': r'\tilde{N} \rightarrow cdb',
        'mfv_neucds': r'\tilde{N} \rightarrow cds',
        'mfv_neutbb': r'\tilde{N} \rightarrow tbb',
        'mfv_neutds': r'\tilde{N} \rightarrow tds',
        'mfv_neuubb': r'\tilde{N} \rightarrow ubb',
        'mfv_neuudb': r'\tilde{N} \rightarrow udb',
        'mfv_neuudtu': r'\tilde{N} \rightarrow u\bar{d}\tau^{\minus}',
        'mfv_xxddbar': r'X \rightarrow d\bar{d}',
        'mfv_stopdbardbar': r'\tilde{t} \rightarrow \bar{d}\bar{d}',
        'mfv_stopbbarbbar': r'\tilde{t} \rightarrow \bar{b}\bar{b}',
        }[_model(sample)]
    if s.endswith('_2015'):
        decay += ' (2015)'
    if 'hip1p0_mit' in s:
        decay += ' (HIP)'
    return decay

def _latex(sample):
    tau = _tau(sample)
    if tau < 1000:
        tau = '%3i\mum' % tau
    else:
        assert tau % 1000 == 0
        tau = '%4i\mm' % (tau/1000)
    return r'$%s$,   $c\tau = %s$, $M = %4s\GeV$' % (_decay(sample), tau, _mass(sample))

def _set_signal_stuff(sample):
    sample.is_signal = True
    sample.model = _model(sample)
    sample.decay = _decay(sample)
    sample.tau  = _tau(sample)
    sample.mass = _mass(sample)
    sample.latex = _latex(sample)

########################################################################

########
# 2017 MC
########

qcd_samples_2017 = [
    MCSample('qcdht0500_2017', '/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',   54624037, nice='QCD, 500 < H_{T} < 700 GeV',   color=804, syst_frac=0.20, xsec=3.163e4),
    MCSample('qcdht0700_2017', '/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',  48042655, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.802e3),
    MCSample('qcdht1000_2017', '/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM', 16619159, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.206e3),
    MCSample('qcdht1500_2017', '/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM', 11323084, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=120),
    MCSample('qcdht2000_2017', '/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM',   5468913, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=25.3),
    ]

ttbar_samples_2017 = [
    MCSample('ttbar_2017', '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM', 153674394, nice='t#bar{t}', color=4, syst_frac=0.15, xsec=832.),
    ]

leptonic_samples_2017 = [
#    MCSample('wjetstolnu_2017',    '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',                24120319, nice='W + jets #rightarrow l#nu', color=  9, syst_frac=0.10, xsec=6.153e4), 
#    MCSample('dyjetstollM10_2017', '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/AODSIM',  40509291, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.861e4),
#    MCSample('dyjetstollM50_2017', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16DR80Premix-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM', 29082237, nice='DY + jets #rightarrow ll, M > 50 GeV', color= 32, syst_frac=0.10, xsec=6.025e3),
#    MCSample('qcdmupt15_2017',     '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',          22094081, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', color=801, syst_frac=0.20, xsec=7.21e8 * 4.2e-4),
    ]

mfv_signal_samples_2017 = [
    MCSample('mfv_neu_tau00100um_M0400_2017', '/mfv_neu_tau00100um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-046f7dbb01fa0a1079ac02e4677757e6/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0600_2017', '/mfv_neu_tau00100um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-48ab61cd2cb4dc6130ac56d00fc592ab/USER', 10000),
    MCSample('mfv_neu_tau00100um_M0800_2017', '/mfv_neu_tau00100um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-1990982db6b1e35188446d210283726a/USER', 10000),
    MCSample('mfv_neu_tau00100um_M1200_2017', '/mfv_neu_tau00100um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-d515706a98191c643f01573ba60905e8/USER', 10000),
    MCSample('mfv_neu_tau00100um_M1600_2017', '/mfv_neu_tau00100um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-41a41b8ae1cb1ac208061229a436de58/USER', 10000),
    MCSample('mfv_neu_tau00100um_M3000_2017', '/mfv_neu_tau00100um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-6b96dcc0c9a38f7d060f7afe02580043/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0400_2017', '/mfv_neu_tau00300um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-451ea3d222a407021f103365e309d57a/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0600_2017', '/mfv_neu_tau00300um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-4ccf664906812b9e7114f3de870fff82/USER', 10000),
    MCSample('mfv_neu_tau00300um_M0800_2017', '/mfv_neu_tau00300um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-f2c84972b68fb0901f28a53865c0b400/USER', 10000),
    MCSample('mfv_neu_tau00300um_M1200_2017', '/mfv_neu_tau00300um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-8f8e8e7eccf3f4faafb85710e2f0a90d/USER', 10000),
    MCSample('mfv_neu_tau00300um_M1600_2017', '/mfv_neu_tau00300um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-1a3d24a2e16093a3fabc70a9630088ec/USER', 10000),
    MCSample('mfv_neu_tau00300um_M3000_2017', '/mfv_neu_tau00300um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-9ac213e76b5df02b43c7551479cc5221/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0400_2017', '/mfv_neu_tau01000um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-3f04b9902bdc5169bb34ce32998fb618/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0600_2017', '/mfv_neu_tau01000um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-15d444206d422a59b9cbad8e9361e396/USER', 10000),
    MCSample('mfv_neu_tau01000um_M0800_2017', '/mfv_neu_tau01000um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-8c72d00e7be0fff6ae525dc8a072859d/USER', 10000),
    MCSample('mfv_neu_tau01000um_M1200_2017', '/mfv_neu_tau01000um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-b7d2e8cd544bda846104ec3cc022fd60/USER', 10000),
    MCSample('mfv_neu_tau01000um_M1600_2017', '/mfv_neu_tau01000um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-dc4db5437423b07aff4ff7c8f5394b7f/USER',  9900),
    MCSample('mfv_neu_tau01000um_M3000_2017', '/mfv_neu_tau01000um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-93da8b3b366678c42874c260fee2cf06/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0400_2017', '/mfv_neu_tau10000um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-727e5f4e4cc2bc162209381938c75f2c/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0600_2017', '/mfv_neu_tau10000um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-58ca8f88fd73b725a4a117c89ef895db/USER', 10000),
    MCSample('mfv_neu_tau10000um_M0800_2017', '/mfv_neu_tau10000um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-0b7d06aa358a969fdde1c918596bcdcf/USER', 10000),
    MCSample('mfv_neu_tau10000um_M1200_2017', '/mfv_neu_tau10000um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-88eca91d2e38a1e858917e6229a25fb3/USER', 10000),
    MCSample('mfv_neu_tau10000um_M1600_2017', '/mfv_neu_tau10000um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-ea02c4e3abeff3089624c535e2a90b92/USER', 10000),
    MCSample('mfv_neu_tau10000um_M3000_2017', '/mfv_neu_tau10000um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-6d9460bf061763afc98bed28f798a434/USER', 10000),
    MCSample('mfv_neu_tau30000um_M0400_2017', '/mfv_neu_tau30000um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-f8b19854ff3c6c995809080e7341bdd1/USER', 10000),
    MCSample('mfv_neu_tau30000um_M0600_2017', '/mfv_neu_tau30000um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-c7ffec9d8e57f450025736d3e7ad983d/USER', 10000),
    MCSample('mfv_neu_tau30000um_M0800_2017', '/mfv_neu_tau30000um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-e23312ac463371fd848af40e6b094a68/USER', 10000),
    MCSample('mfv_neu_tau30000um_M1200_2017', '/mfv_neu_tau30000um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-d7acf62824a7a6b1d12aa6bab81f9aa4/USER', 10000),
    MCSample('mfv_neu_tau30000um_M1600_2017', '/mfv_neu_tau30000um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-5267718a61ebcb310b853f78982d36fd/USER', 10000),
    MCSample('mfv_neu_tau30000um_M3000_2017', '/mfv_neu_tau30000um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-5ab83f0d9fdd2683765d51bd9fa47839/USER', 10000),
    MCSample('mfv_neu_tau100000um_M0400_2017', '/mfv_neu_tau100000um_M0400/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-67166f1a82362e16f9ae0674958921b2/USER', 10000),
    MCSample('mfv_neu_tau100000um_M0600_2017', '/mfv_neu_tau100000um_M0600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-724e69e0b8e50ff5419b4afed1753aba/USER', 10000),
    MCSample('mfv_neu_tau100000um_M0800_2017', '/mfv_neu_tau100000um_M0800/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-8ba75b41f6de329e0507960cf62e6654/USER', 10000),
    MCSample('mfv_neu_tau100000um_M1200_2017', '/mfv_neu_tau100000um_M1200/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-e100cbd5e9c3d0af1528f826409959af/USER', 10000),
    MCSample('mfv_neu_tau100000um_M1600_2017', '/mfv_neu_tau100000um_M1600/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-fdb13f8873d2bb070ee21d05a27b710e/USER', 10000),
    MCSample('mfv_neu_tau100000um_M3000_2017', '/mfv_neu_tau100000um_M3000/tucker-RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1-518a667c1a87b8ebee83b6b0f9151326/USER', 10000),
    ]

all_signal_samples_2017 = mfv_signal_samples_2017

for s in all_signal_samples_2017:
    _set_signal_stuff(s)
    s.xsec = 1e-3
    s.is_private = s.dataset.startswith('/mfv_')
    if s.is_private:
        s.dbs_inst = 'phys03'
        s.condor = True
        s.xrootd_url = xrootd_sites['T3_US_FNALLPC']

########################################################################

########
# 2017 data
########

data_samples_2017 = [
    DataSample('JetHT2017B', '/JetHT/Run2017B-17Nov2017-v1/AOD'),  # 297047 299329
    DataSample('JetHT2017C', '/JetHT/Run2017C-17Nov2017-v1/AOD'),  # 299368 302029
    DataSample('JetHT2017D', '/JetHT/Run2017D-17Nov2017-v1/AOD'),  # 302031 302663
    DataSample('JetHT2017E', '/JetHT/Run2017E-17Nov2017-v1/AOD'),  # 303824 304797
    DataSample('JetHT2017F', '/JetHT/Run2017F-17Nov2017-v1/AOD'),  # 305040 306460
    ]

auxiliary_data_samples_2017 = [
    DataSample('SingleMuon2017B', '/SingleMuon/Run2017B-17Nov2017-v1/AOD'),
    DataSample('SingleMuon2017C', '/SingleMuon/Run2017C-17Nov2017-v1/AOD'),
    DataSample('SingleMuon2017D', '/SingleMuon/Run2017D-17Nov2017-v1/AOD'),
    DataSample('SingleMuon2017E', '/SingleMuon/Run2017E-17Nov2017-v1/AOD'),
    DataSample('SingleMuon2017F', '/SingleMuon/Run2017F-17Nov2017-v1/AOD'),
    ]

for s in data_samples_2017 + auxiliary_data_samples_2017:
    s.json = cmssw_base('src/JMTucker/MFVNeutralino/test/jsons/2017.json')

########################################################################

registry = SamplesRegistry()

# shortcuts, be careful:
# - can't add data, qcd datasets by primary (have the same primary for different datasets)
from functools import partial
_adbp = registry.add_dataset_by_primary
_adbp3 = partial(_adbp, dbs_inst='phys03')

__all__ = [
    'qcd_samples_2017',
    'ttbar_samples_2017',
    'leptonic_samples_2017',
    'mfv_signal_samples_2017',
    'data_samples_2017',
    'auxiliary_data_samples_2017',

    'registry',
    ]

for x in __all__:
    o = eval(x)
    if type(o) == list:
        registry.add_list(x,o)
        for sample in o:
            registry.add(sample)
            exec '%s = sample' % sample.name
            __all__.append(sample.name)

__all__ += [
    'all_signal_samples_2017',
    ]

########################################################################

########
# Extra datasets and other overrides go here.
########

########
# miniaod
########

for sample in data_samples_2017 + auxiliary_data_samples_2017:
    sample.add_dataset('miniaod', sample.dataset.replace('AOD', 'MINIAOD'))

qcdht0500_2017.add_dataset('miniaod', '/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM' ,  54624037)
qcdht0700_2017.add_dataset('miniaod', '/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',  47620074)
qcdht1000_2017.add_dataset('miniaod', '/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM', 16606018)
qcdht1500_2017.add_dataset('miniaod', '/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM', 11323084)
qcdht2000_2017.add_dataset('miniaod', '/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',   5468913)
ttbar_2017.add_dataset('miniaod', '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM', 153531390)

for sample in mfv_signal_samples_2017:
    sample.add_dataset('miniaod', '/%s/None/USER' % sample.primary_dataset, sample.nevents_orig)
    sample.datasets['miniaod'].condor = True
    sample.datasets['miniaod'].xrootd_url = xrootd_sites['T3_US_FNALLPC']

########
# ntuples
########

#for x in ttbar_samples_2017 + qcd_samples_2017:
#    x.add_dataset('ntuplev18m')

########
# automatic condor declarations for ntuples
########

ds4condor = ['ntuple', 'v0ntuple', 'pick1vtx']
for s in registry.all():
    for ds in s.datasets.keys():
        for ds4 in ds4condor:
            if ds.startswith(ds4):
                s.datasets[ds].condor = True
                s.datasets[ds].xrootd_url = xrootd_sites['T3_US_FNALLPC']

########
# other condor declarations, generate condorable dict with Shed/condor_list.py
########

# 2018-04-27
condorable = {
    "T3_US_FNALLPC": {
        "main": [],
        "miniaod": [],
        },
    "T1_US_FNAL_Disk": {
        "main": [],
        "miniaod": [],
        },
    "T2_DE_DESY": {
        "main": [],
        "miniaod": [],
        },
    }

for site, d in condorable.iteritems():
    if not xrootd_sites.has_key(site):
        raise ValueError('need entry in xrootd_sites for %s' % site)
    for ds, samples in d.iteritems():
        for s in samples:
            s.datasets[ds].condor = True
            s.datasets[ds].xrootd_url = xrootd_sites[site]

########################################################################

if __name__ == '__main__':
    main(registry)

    import sys
    from pprint import pprint
    from JMTucker.Tools import DBS
    from JMTucker.Tools.general import popen

    if 0:
        from DBS import *
        for s in data_samples + mfv_signal_samples:
            n1, n2 = s.datasets['main'].nevents_orig, s.datasets['miniaod'].nevents_orig
            if n1 != n2:
                print s.name, n1, n2

    if 0:
        aod_strings = ['RunIIFall15DR76-PU25nsData2015v1', 'RunIISummer16DR80Premix-PUMoriond17']
        miniaod_strings = ['RunIIFall15MiniAODv2-PU25nsData2015v1', 'RunIISummer16MiniAODv2-PUMoriond17']
        no = 'Trains Material ALCA Flat RunIISpring16MiniAODv1'.split()
        from JMTucker.Tools.general import popen
        for s in xx4j_samples_2015: #qcd_samples + ttbar_samples + leptonic_background_samples:
            print s.name
            #print s.primary_dataset
            output = popen('dasgoclient_linux -query "dataset=/%s/*/*AODSIM"' % s.primary_dataset).split('\n')
            for y in 'AODSIM MINIAODSIM'.split():
                for x in output:
                    ok = True
                    for n in no:
                        if n in x:
                            ok = False
                    if not ok:
                        continue
                    #print x
                    if x.endswith('/' + y):
                        nevents = None
                        for line in popen('dasgoclient_linux -query "dataset=%s | grep dataset.nevents"' % x).split('\n'):
                            try:
                                nevents = int(float(line))
                            except ValueError:
                                pass
                        assert nevents is not None and nevents > 0
                        print '"%s", %i' % (x, nevents)

    if 0:
        for x,y in zip(qcd_samples, qcd_samples_ext):
            print x.name, x.int_lumi_orig/1000, '->', (x.int_lumi_orig + y.int_lumi_orig)/1000

    if 0:
        from JMTucker.Tools.general import coderep_files
        f = open('a.txt', 'wt')
        for x in qcd_samples + qcd_samples_ext + ttbar_samples + data_samples:
            for y in ('ntuplev11',):
                print x.name, y
                if not x.try_curr_dataset(y):
                    continue
                code = coderep_files(x.filenames)
                f.write('(%r, %r): (%i, %s),\n' % (x.name, y, len(x.filenames), code))

    if 0:
        import os
        from JMTucker.Tools.general import coderep_files
        f = open('a.txt', 'wt')
        for s in qcd_samples + qcd_samples_ext + ttbar_samples + data_samples:
            print s.name
            fns = s.filenames
            base = os.path.commonprefix(fns)
            bns = [x.replace(base, '') for x in fns]
            code = "[%r + x for x in '''\n" % base
            for bn in bns:
                code += bn + '\n'
            code += "'''.split('\n')]"
            f.write('(%r, %r): (%i, %s),\n' % (s.name, y, len(fns), code))

    if 0:
        dses = set(s.dataset for s in registry.all())
        for line in open('todel.txt'):
            line = line.strip()
            if line in dses:
                print line

    if 0:
        for ds in 'main', 'miniaod':
            for s in registry.all():
                if s.has_dataset(ds):
                    s.set_curr_dataset(ds)
                    print '%s %s %s %s' % (s.name, ds, s.condor, s.xrootd_url)

    if 0:
        have = ()
        print len(have)
        for s in all_signal_samples:
            if s not in have:
                print s.name + ',',
