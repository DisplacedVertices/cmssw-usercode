#!/usr/bin/env python

import sys, os, math
from JMTucker.Tools.general import save_git_status

skip_tests = 'skip_tests' in sys.argv
testing = 'testing' in sys.argv

dir = [x for x in sys.argv if x.startswith('crab/')]
dir = 'crab/TrackMover' if not dir else dir[0]

################################################################################

crab_cfg_template = '''
[CRAB]
jobtype = cmssw
scheduler = remoteGlidein

[CMSSW]
datasetpath = %(dataset)s
pset = %(pset_fn)s
get_edm_output = 0
ignore_edm_output = 1
output_file = movedtree.root
use_dbs3 = 1
JOB_CONTROL

[USER]
script_exe = twostep.sh
additional_input_files = my_treer.py
ui_working_dir = %(ui_working_dir)s
ssh_control_persist = no
copy_data = 1
storage_element = T3_US_Cornell
publish_data = 1
publish_data_name = mfv_movedtree_v20
dbs_url_for_publication = phys03

[GRID]
#se_black_list = 
'''

################################################################################

if not skip_tests:
    for py in 'ntuple treer'.split():
        print 'testing %s.py' % py
        if os.system('python %s.py' % py) != 0:
            raise RuntimeError('%s.py does not work' % py)

os.system('mkdir -p ' + os.path.join(dir, 'psets'))
save_git_status(os.path.join(dir, 'gitstatus'))

def submit(sample):
    print sample.name

    pset_fn = os.path.join(dir, 'psets/%(name)s.py' % sample)
    new_py = open('ntuple.py').read()

    if not sample.is_mc:
        new_py = new_py.replace('runOnMC = True', 'runOnMC = False')
        new_py += '\nprocess.dummyToMakeDiffHash = cms.PSet(submitName = cms.string("%s"))\n' % sample.name
        if sample.name.startswith('MultiJetPk2012'):
            for name_part, tag in [
                ('2012B', 'FT_53_V6C_AN4'),
                ('2012C1', 'FT53_V10A_AN4'),
                ('2012C2', 'FT_P_V42C_AN4'),
                ('2012D1', 'FT_P_V42_AN4'),
                ('2012D2', 'FT_P_V42D_AN4'),
                ]:
                if name_part in sample.name:
                    new_py += '\nprocess.GlobalTag.globaltag = "%s::All"\n' % tag
        
    open(pset_fn, 'wt').write(new_py)

    os.system('python -c \'import treer; open("my_treer.py","wt").write(treer.process.dumpPython())\'')

    ui_working_dir = os.path.join(dir, 'crab_%s' % sample.name)

    if sample.is_mc:
        timing = { 'dyjetstollM10': 0.011203, 'dyjetstollM50': 0.019867, 'qcdbce020': 0.008660, 'qcdbce030': 0.007796, 'qcdbce080': 0.061260, 'qcdbce170': 0.328891, 'qcdbce250': 0.481813, 'qcdbce350': 0.519482, 'qcdem020': 0.010137, 'qcdem030': 0.01, 'qcdem080': 0.037925, 'qcdem170': 0.286123, 'qcdem250': 0.471398, 'qcdem350': 0.686303, 'qcdht0100': 0.008273, 'qcdht0250': 0.116181, 'qcdht0500': 0.738374, 'qcdht1000': 1.002745, 'qcdmu0020': 0.012301, 'qcdmu0030': 0.015762, 'qcdmu0050': 0.018178, 'qcdmu0080': 0.119300, 'qcdmu0120': 0.245562, 'qcdmu0170': 0.32, 'qcdmu0300': 0.419818, 'qcdmu0470': 0.584266, 'qcdmu0600': 0.455305, 'qcdmu0800': 0.879171, 'qcdmu1000': 1.075712, 'singletop_s': 0.093429, 'singletop_s_tbar': 0.146642, 'singletop_tW': 0.327386, 'singletop_tW_tbar': 0.184349, 'singletop_t': 0.092783, 'singletop_t_tbar': 0.060983, 'ttbarhadronic': 0.752852, 'ttbarsemilep': 0.419073, 'ttbardilep': 0.295437, 'ttgjets': 0.861987, 'ttwjets': 0.714156, 'ttzjets': 0.827464, 'wjetstolnu': 0.010842, 'ww': 0.046754, 'wz': 0.049839, 'zz': 0.059791, }
        sample.events_per = int(3.5*3600/timing[sample.name]) / 2
        nj = int(sample.nevents_orig / float(sample.events_per)) + 1
        assert nj < 5000

        crab_cfg = crab_cfg_template.replace('JOB_CONTROL', '''
events_per_job = %(events_per)i
total_number_of_events = -1
''')
    else:
        crab_cfg = crab_cfg_template.replace('JOB_CONTROL', '''
lumi_mask = /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt
lumis_per_job = 20
total_number_of_lumis = -1
''')

    vd = locals()
    vd['name'] = sample.name
    vd['dataset'] = sample.dataset
    if sample.is_mc:
        vd['events_per'] = sample.events_per
    open('crab.cfg','wt').write(crab_cfg % vd)
    if not testing:
        os.system('crab -create')
        os.system('crsuball %s' % ui_working_dir)
        os.system('rm -f crab.cfg my_treer.py')

################################################################################

import JMTucker.Tools.Samples as Samples

for sample in Samples.from_argv(Samples.ttbar_samples + Samples.qcd_samples + Samples.data_samples):
    submit(sample)
