#!/usr/bin/env python

import sys, os, math
from JMTucker.Tools.general import save_git_status
from modify import *

# JMTBAD argparse

reco_triggered_only = 'triggeredonly' in sys.argv or 'ntuple' in sys.argv

run_reco = 'gensimonly' not in sys.argv
run_pat = run_reco and 'pat' in sys.argv
run_ntuple = run_reco and ('ntuple' in sys.argv or 'minitree' in sys.argv)
run_minitree = run_ntuple and 'minitree' in sys.argv

run_tkdqm = 'tkdqm' in sys.argv

run_ttbar = 'ttbar' in sys.argv

skip_tests = 'skip_tests' in sys.argv
testing = 'testing' in sys.argv

dir = [x for x in sys.argv if x.startswith('crab/')]
dir = 'crab/MakeSamples' if not dir else dir[0]

nevents = [int(x.replace('nevents=', '')) for x in sys.argv if x.startswith('nevents=')]
nevents = 1000000 if not nevents else nevents[0]

events_per = [int(x.replace('events_per=', '')) for x in sys.argv if x.startswith('events_per=')]
events_per = 200 if not events_per else events_per[0]

return_data = 'return' in sys.argv

################################################################################

crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = remoteGlidein

[CMSSW]
datasetpath = None
pset = %(pset_fn)s
get_edm_output = 0
ignore_edm_output = 1
output_file = %(output_file)s
events_per_job = %(events_per)i
total_number_of_events = %(nevents)i
first_lumi = 1
use_dbs3 = 1

[USER]
script_exe = twostep.sh
additional_input_files = %(additional_input_files)s
ui_working_dir = %(ui_working_dir)s
ssh_control_persist = no
RETURN_OR_COPY

[GRID]
se_black_list = T3_MX_Cinvestav,T2_RU_RRC_KI,T3_UK_London_QMUL,T3_UK_ScotGrid_GLA,T3_US_UCD,T3_US_UMiss,T2_RU_PNPI,T3_RU_FIAN,T2_US_Purdue
'''

if return_data:
    crab_cfg = crab_cfg.replace('RETURN_OR_COPY', 'return_data = 1')
else:
    crab_cfg = crab_cfg.replace('RETURN_OR_COPY', '''
copy_data = 1
storage_element = T3_US_FNALLPC
publish_data = 1
publish_data_name = mfv_%(name)s_v20
dbs_url_for_publication = phys03
''')

################################################################################

if run_pat and run_ntuple:
    raise ValueError('cannot do both pat and ntuple')

if not skip_tests:
    print 'testing gensimhlt.py'
    if os.system('python gensimhlt.py') != 0: # cannot just import or else this screws up singleton services like MessageLogger when we expand pat.py below
        raise RuntimeError('gensimhlt.py does not work')

    if run_reco:
        print 'testing reco.py (may need to expand if you have modified the base reconstruction)'
        if os.system('python reco.py') != 0:
            raise RuntimeError('reco.py does not work')

_final = None
_post = None

if run_pat:
    print 'expanding pat.py'
    import JMTucker.Tools.PATTuple_cfg as _final
    _final.aod_plus_pat(_final.process)
    _final.keep_random_state(_final.process)
    _final.keep_mixing_info(_final.process)
    _final.no_skimming_cuts(_final.process)
elif run_ntuple:
    print 'expanding ntuple.py'
    sys.path.insert(0, '..')
    import ntuple as _final
    if run_minitree:
        print 'expanding minitree.py'
        import minitree as _post
        _post.process.source.fileNames = ['file:ntuple.root']

if _final:
    _final.process.source.fileNames = ['file:reco.root']
    _final.process.maxEvents.input = -1
    _final.input_is_pythia8(_final.process)

os.system('mkdir -p ' + os.path.join(dir, 'psets'))
save_git_status(os.path.join(dir, 'gitstatus'))

def submit(name, tau0=None, mass=None):
    print name
    is_signal = tau0 is not None and mass is not None
    if not is_signal:
        if tau0 is not None or mass is not None:
            raise ValueError('must specify both tau0 and mass if either specified')
        if 'ttbar' not in name:
            raise ValueError('if not signal, must only be ttbar')

    if run_minitree:
        output_file = 'minitree.root'
    elif run_ntuple:
        output_file = 'ntuple.root'
    elif run_pat:
        output_file = 'aodpat.root'
    elif run_reco:
        output_file = 'reco.root'
    else:
        output_file = 'gensimhlt.root'

    additional_input_files = ['minSLHA.spc', 'modify.py']
    if run_minitree:
        additional_input_files.append('minitree.py')
    if run_ntuple:
        additional_input_files.append('ntuple.py')
    elif run_pat:
        additional_input_files.append('pat.py')
    if run_ttbar:
        additional_input_files.remove('minSLHA.spc')

    pset_fn = os.path.join(dir, 'psets/mfv_%(name)s.py' % locals())
    new_py = open('gensimhlt.py').read()

    if run_tkdqm:
        tkdqm_pset_fn = 'my_tkdqm.py'
        additional_input_files.append(tkdqm_pset_fn)
        output_file += ', tkdqm.root'
        new_tkdqm_py = open('tkdqm.py').read()
    else:
        new_tkdqm_py = ''

    if run_reco:
        reco_pset_fn = 'my_reco.py'
        additional_input_files.append(reco_pset_fn)
        new_reco_py = open('reco.py').read()
        if is_signal:
            new_reco_py += '\nkeep_random_info(process)\n'
        if reco_triggered_only:
            new_reco_py += '\nhlt_filter(process, "HLT_QuadJet50_v*")\n'
    else:
        new_reco_py = ''

    if 'gluino' in name:
        new_py += '\nset_gluino_tau0(process, %e)\n' % tau0       
        set_mass(mass)
    elif 'neutralino' in name:
        new_py += '\nset_neutralino_tau0(process, %e)\n' % tau0
        set_masses(mass+5, mass)
    elif 'ttbar' in name:
        new_py += '\nttbar(process)\n'
    else:
        raise RuntimeError("don't know what generation type to use")

    if 'design' in name:
        glb_snip = "\nprocess.GlobalTag = GlobalTag(process.GlobalTag, 'DESIGN53_V18::All', '')\n"
        new_py += glb_snip
        new_tkdqm_py += glb_snip + 'castor_thing(process)\n'
        new_reco_py += glb_snip + 'castor_thing(process)\n'
        if _final:
            _final.process.GlobalTag = GlobalTag(process.GlobalTag, 'DESIGN53_V18::All', '')
            castor_thing(_final.process)

    if 'nopu' in name:
        new_py += '\nnopu(process)\n'

    if 'gaubs' in name:
        snip = '\ngauss_bs(process)\n'
        new_py += snip
        new_tkdqm_py += snip
        new_reco_py += snip
    elif 'gaunxybs' in name:
        snip = '\ngauss_bs(process, True)\n'
        new_py += snip
        new_tkdqm_py += snip
        new_reco_py += snip
    elif 'gaunxyzbs' in name:
        snip = '\ngauss_bs(process, True, True)\n'
        new_py += snip
        new_tkdqm_py += snip
        new_reco_py += snip

    if 'ali_' in name:
        if not run_reco:
            raise ValueError('alignment means nothing if not running reco')
        ali_tag = name.split('ali_')[-1].split("_")[0].capitalize()
        new_reco_py += '\ntracker_alignment(process, "%s")\n' % ali_tag
        new_reco_py += 'dummy_beamspot(process, "myttbar%s")\n' % ali_tag
        new_tkdqm_py += '\ntracker_alignment(process, "%s")\n' % ali_tag
        new_tkdqm_py += 'dummy_beamspot(process, "myttbar%s")\n' % ali_tag
        if _final:
            tracker_alignment(_final.process, ali_tag)
            dummy_beamspot(_final.process, 'myttbar' + ali_tag)

    if 'tune_' in name:
        new_py += '\nset_tune(process,%s)\n' % name.split('tune_')[1]

    if 'tkex' in name:
        if not run_reco:
            raise ValueError('tkex means nothing if not running reco')
        new_reco_py += '\nkeep_tracker_extras(process)\n'

    new_py += 'process.dummyToMakeDiffHash = cms.PSet(submitName = cms.string("%s"))' % name

    open(pset_fn, 'wt').write(new_py)
    if run_tkdqm:
        open(tkdqm_pset_fn, 'wt').write(new_tkdqm_py)
    if run_reco:
        open(reco_pset_fn, 'wt').write(new_reco_py)

    if _final:
        open('ntuple.py' if run_ntuple else 'pat.py', 'wt').write(_final.process.dumpPython())

    if _post:
        open('minitree.py', 'wt').write(_post.process.dumpPython())

    additional_input_files = ', '.join(additional_input_files)

    ui_working_dir = os.path.join(dir, 'crab_mfv_%s' % name)
    vd = locals()
    vd['nevents'] = nevents
    vd['events_per'] = events_per
    open('crab.cfg','wt').write(crab_cfg % vd)
    if not testing:
        os.system('crab -create')
        for i in xrange(int(math.ceil(float(nevents)/events_per/500))):
            os.system('crab -c %s -submit 500' % ui_working_dir)
        os.system('rm -f crab.cfg reco.pyc my_reco.py my_tkdqm.py pat.py ntuple.py minitree.py')

################################################################################

if run_ttbar:
    #to_run = ['ali_' + x for x in ['bowing', 'elliptical', 'curl', 'radial', 'sagitta', 'skew', 'telescope', 'twist', 'zexpansion']]
    #to_run = 'designnopugaubs designnopugaunxybs designnopugaunxyzbs'.split()
    #to_run = ['designnoputkex']
    #to_run = ['tune_' + x for x in ['3','4','5','6','7','8','9','10','11','12','13']]
    #to_run = ['tune_' + x for x in ['3','4','5','6','7','8','9','10','11','12','13']]

    #for run in to_run:
    #    submit('ttbar_' + run)

    for i in xrange(5):
        submit('ttbar_%02itune_11' % i)
else:
    tau0s = [0.1, 0.3, 0.6, 1.0, 3.0, 6.0, 10, 20., 30.]
    masses = range(200, 1501, 100)
    tunes = [5]

    to_do = [(t,m,tu) for m in masses for t in tau0s for tu in tunes]

    for tau0, mass, tune in to_do:
        name = 'neutralino_tau%05ium_M%04i' % (int(tau0*1000), mass)
        if tune != 5:
            name += '_tune_%i' % tune

        submit(name, tau0, mass)
