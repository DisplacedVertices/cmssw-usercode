#!/usr/bin/env python

import sys, os

run_pat = 'pat' in sys.argv
run_ttbar = 'ttbar' in sys.argv
skip_tests = 'skip_tests' in sys.argv
testing = 'testing' in sys.argv
dir = 'crab/MakeSamples'

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
events_per_job = 50
total_number_of_events = 100000
first_lumi = 1
use_dbs3 = 1

[USER]
script_exe = twostep.sh
additional_input_files = %(additional_input_files)s
ui_working_dir = %(ui_working_dir)s
copy_data = 1
storage_element = T3_US_Cornell
publish_data = 1
publish_data_name = mfv_%(name)s
dbs_url_for_publication = phys03
%(jmt_externals_hack)s
ssh_control_persist = no

[GRID]
se_black_list = T2_RU_ITEP,T3_FR_IPNL,T3_US_FIU,T2_GR_Ioannina,T3_US_UCR,T2_PL_Warsaw,T3_US_Baylor,T2_FR_IPHC,T3_MX_Cinvestav,T2_TH_CUNSTDA,T3_US_TTU,T2_UA_KIPT,T2_BR_SPRACE,T3_US_OSU,T2_RU_PNPI,T2_FI_HIP,T2_BE_IIHE,T3_US_UCD,T2_AT_Vienna,T3_US_Omaha,T2_FR_CCIN2P3,T2_RU_RRC_KI,T2_TW_Taiwan,T3_US_Rutgers,T3_UK_London_QMUL
'''

################################################################################

if os.environ['USER'] != 'tucker' and not run_ttbar:
    raw_input('do you have the jmt_externals_hack for crab? if not, ^C now.')

if not skip_tests:
    print 'testing gensimhlt.py'
    if os.system('python gensimhlt.py') != 0: # cannot just import or else this screws up singleton services like MessageLogger when we expand pat.py below
        raise RuntimeError('gensimhlt.py does not work')

    print 'testing reco.py (may need to expand if you have modified the base reconstruction)'
    if os.system('python reco.py') != 0:
        raise RuntimeError('reco.py does not work')

if run_pat:
    print 'expanding pat.py'
    import JMTucker.Tools.PATTuple_cfg as _pat
    _pat.process.source.fileNames = ['file:reco.root']
    _pat.process.maxEvents.input = -1
    _pat.no_skimming_cuts(_pat.process)
    _pat.aod_plus_pat(_pat.process)
    _pat.input_is_pythia8(_pat.process)
    _pat.keep_random_state(_pat.process)
    _pat.keep_mixing_info(_pat.process)
    open('pat.py', 'wt').write(_pat.process.dumpPython())

os.system('mkdir -p ' + os.path.join(dir, 'psets'))

def submit(name, tau0=None, mass=None):
    print name

    if run_pat:
        output_file = 'aodpat.root'
    else:
        output_file = 'reco.root'

    additional_input_files = ['minSLHA.spc', 'modify.py']
    if run_pat:
        additional_input_files.append('pat.py')
    if run_ttbar:
        additional_input_files.remove('minSLHA.spc')

    pset_fn = os.path.join(dir, 'psets/mfv_%(name)s.py' % locals())
    new_py = open('gensimhlt.py').read()

    reco_pset_fn = 'my_reco.py'
    additional_input_files.append(reco_pset_fn)
    new_reco_py = open('reco.py').read()

    if 'ttbar' not in name:
        assert tau0 is not None and mass is not None

    jmt_externals_hack = 'jmt_externals_hack = pythia8_hack'

    if 'gluino' in name:
        new_py += '\nfrom modify import set_gluino_tau0\n'
        new_py += '\nset_gluino_tau0(process, %e)\n' % tau0       
        from modify import set_mass
        set_mass(mass)
    elif 'neutralino' in name:
        new_py += '\nfrom modify import set_neutralino_tau0\n'
        new_py += '\nset_neutralino_tau0(process, %e)\n' % tau0
        from modify import set_masses
        set_masses(mass+5, mass)
    elif 'ttbar' in name:
        jmt_externals_hack = ''
        new_py += '\nfrom modify import ttbar\n'
        new_py += '\nttbar(process)\n'
    else:
        raise RuntimeError("don't know what LSP to use")

    if 'design' in name:
        glb_snip = "\nprocess.GlobalTag = GlobalTag(process.GlobalTag, 'DESIGN53_V18::All', '')\n"
        new_py += glb_snip
        new_reco_py += glb_snip + '''
from modify import prefer_it
prefer_it(process, 'castorThing', 'frontier://FrontierProd/CMS_COND_HCAL_000', 'CastorSaturationCorrsRcd', 'CastorSaturationCorrs_v1.00_mc')
'''

    if 'nopu' in name:
        new_py += '\nfrom modify import nopu\n'
        new_py += 'nopu(process)\n'

    snip = '\nfrom modify import ideal_bs_tag, gauss_bs\n'
    if 'gaubs' in name:
        snip += 'gauss_bs(process)\n'
        new_py += snip
        new_reco_py += snip
    elif 'gaunxybs' in name:
        snip += 'gauss_bs(process, True)\n'
        new_py += snip
        new_reco_py += snip
    elif 'gaunxyzbs' in name:
        snip += 'gauss_bs(process, True, True)\n'
        new_py += snip
        new_reco_py += snip

    if 'ali_' in name:
        ali_tag = name.split('ali_')[-1].capitalize()
        new_reco_py += '''
from modify import prefer_it
prefer_it(process, 'tkAlign', 'frontier://FrontierPrep/CMS_COND_ALIGNMENT', 'TrackerAlignmentRcd', 'TrackerAlignment_2010RealisticPlus%s_mc')
''' % ali_tag

    if 'tune_' in name:
        new_py += '\nfrom modify import set_tune\n'
        new_py += '\nset_tune(process,%s)\n' % name.split('tune_')[1]

    if 'tkex' in name:
        new_reco_py += "\nprocess.output.outputCommands += ['keep recoTrackExtras_generalTracks__*', 'keep TrackingRecHitsOwned_generalTracks__*']\n"

    open(pset_fn, 'wt').write(new_py)
    open(reco_pset_fn, 'wt').write(new_reco_py)

    additional_input_files = ', '.join(additional_input_files)

    ui_working_dir = os.path.join(dir, 'crab_mfv_%s' % name)
    open('crab.cfg','wt').write(crab_cfg % locals())
    if not testing:
        os.system('crab -create')
        for i in xrange(4):
            os.system('crab -c %s -submit 500' % ui_working_dir)
        os.system('rm -f crab.cfg reco.pyc my_reco.py')

################################################################################

if run_ttbar:
    to_run = ['ali_' + x for x in ['bowing', 'elliptical', 'curl', 'radial', 'sagitta', 'skew', 'telescope', 'twist', 'zexpansion']]
    #to_run = 'designnopugaubs designnopugaunxybs designnopugaunxyzbs'.split()
    #to_run = ['designnoputkex']
    to_run = ['tune_' + x for x in ['3','4','5','6','7','8','9','10','11','12','13']]

    for run in to_run:
        submit('ttbar_' + run)
else:
    tau0s = [0., 0.1, 0.3, 1.0, 3.0, 9.9, 15., 30.]
    masses = range(200, 1501, 100)
    tunes = [5]

    to_do = [(t,m,tu) for m in masses for t in tau0s for tu in tunes]

    for tau0, mass, tune in to_do:
        name = 'neutralino_tau%05ium_M%04i' % (int(tau0*1000), mass)
        if tune != 5:
            name += '_tune_%i' % tune
        submit(name, tau0, mass)
