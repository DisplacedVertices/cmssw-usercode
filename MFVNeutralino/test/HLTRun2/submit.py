import os, sys

crab_cfg_template = '''[CMSSW]
events_per_job = %(events_per_job)s
total_number_of_events = -1
pset = hlt.py
%(dbs_url)s
datasetpath = %(datasetpath)s

[USER]
ui_working_dir = crab/HLTRun2/crab_%(name)s
return_data = 1

[CRAB]
jobtype = cmssw
scheduler = %(scheduler)s
'''

os.system('mkdir -p crab/HLTRun2')

datasets = [
    ('qcd0015', '/QCD_Pt-15to30_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_castor_PHYS14_25_V3-v2/GEN-SIM-RAW'),
    ('qcd0030', '/QCD_Pt-30to50_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_castor_PHYS14_25_V3-v2/GEN-SIM-RAW'),
    ('qcd0050', '/QCD_Pt-50to80_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_castor_PHYS14_25_V3-v1/GEN-SIM-RAW'),
    ('qcd0080', '/QCD_Pt-80to120_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_castor_PHYS14_25_V3-v1/GEN-SIM-RAW'),
    ('qcd0120', '/QCD_Pt-120to170_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_castor_PHYS14_25_V3-v1/GEN-SIM-RAW'),
    ('qcd0170', '/QCD_Pt-170to300_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_castor_PHYS14_25_V3-v1/GEN-SIM-RAW'),
    ('qcd0300', '/QCD_Pt-300to470_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_castor_PHYS14_25_V3-v1/GEN-SIM-RAW'),
    ('qcd0470', '/QCD_Pt-470to600_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_castor_PHYS14_25_V3-v1/GEN-SIM-RAW'),
    ('qcd0600', '/QCD_Pt-600to800_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_castor_PHYS14_25_V3-v1/GEN-SIM-RAW'),
    ('qcd0800', '/QCD_Pt-800to1000_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_castor_PHYS14_25_V3-v1/GEN-SIM-RAW'),
    ('qcd1000', '/QCD_Pt-1000to1400_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_castor_PHYS14_25_V3-v1/GEN-SIM-RAW'),
    ('qcd1400', '/QCD_Pt-1400to1800_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_castor_PHYS14_25_V3-v1/GEN-SIM-RAW'),
    ('qcd1800', '/QCD_Pt-1800_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_castor_PHYS14_25_V3-v1/GEN-SIM-RAW'),
    ('neugun', '/Neutrino_Pt-2to20_gun/Phys14DR-AVE20BX25_tsg_PHYS14_25_V3-v1/GEN-SIM-RAW'),
    ('mfv0400', '/Neutralino_M400_13TeV_DisplaceVtx_GENSIM_721/mzientek-Neutralino_731_m400_HLT-8bb1453964da032b385b47cbbd4968dd/USER'),
    ('mfv0500', '/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/mzientek-Neutralino_731_m500_HLT-8bb1453964da032b385b47cbbd4968dd/USER'),
    ('mfv0600', '/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/mzientek-Neutralino_731_m600_HLT-8bb1453964da032b385b47cbbd4968dd/USER'),
    ('mfv0700', '/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/mzientek-Neutralino_731_m700_HLT-8bb1453964da032b385b47cbbd4968dd/USER'),
    ('mfv0800', '/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/mzientek-Neutralino_731_m800_HLT-8bb1453964da032b385b47cbbd4968dd/USER'),
    ('mfv0900', '/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/mzientek-Neutralino_731_m900_HLT-8bb1453964da032b385b47cbbd4968dd/USER'),
    ('mfv1000', '/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/mzientek-Neutralino_731_m1000_HLT-8bb1453964da032b385b47cbbd4968dd/USER'),
]

for name, datasetpath in datasets:
    if name.startswith('mfv'):
        events_per_job = '100'
        dbs_url = 'dbs_url = phys03'
        scheduler = 'condor'
    else:
        events_per_job = '2000'
        dbs_url = ''
        scheduler = 'remoteGlidein'

    crab_cfg = crab_cfg_template % locals()
    open('crab.cfg', 'wt').write(crab_cfg)
    os.system('crab -create -submit all')

