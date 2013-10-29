import sys, os

crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = remoteGlidein

[CMSSW]
datasetpath = None
pset = %(pset_fn)s
get_edm_output = 0
ignore_edm_output = 1
output_file = aodpat.root
events_per_job = 50
total_number_of_events = 100000
first_lumi = 1

[USER]
script_exe = twostep.sh
additional_input_files = minSLHA.spc, reco.py, pat.py
ui_working_dir = crab/gensimhltrecopat/crab_mfv_%(name)s
copy_data = 1
storage_element = T3_US_FNALLPC
check_user_remote_dir = 0
publish_data = 1
publish_data_name = mfv_%(name)s
dbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
jmt_externals_hack = pythia8_hack
ssh_control_persist = no

[GRID]
se_black_list = T2_RU_ITEP,T3_FR_IPNL,T3_US_FIU,T2_GR_Ioannina,T3_US_UCR,T2_PL_Warsaw,T3_US_Baylor,T2_FR_IPHC,T3_MX_Cinvestav,T2_TH_CUNSTDA,T3_US_TTU,T2_UA_KIPT,T2_BR_SPRACE,T3_US_OSU,T2_RU_PNPI,T2_FI_HIP,T2_BE_IIHE,T3_US_UCD,T2_AT_Vienna,T3_US_Omaha,T2_FR_CCIN2P3,T2_RU_RRC_KI,T2_TW_Taiwan,T3_US_Rutgers
'''

if os.environ['USER'] != 'tucker':
    raw_input('do you have the jmt_externals_hack for crab? if not, ^C now.')

skip_tests = False
if not skip_tests:
    print 'testing gensimhlt.py'
    if os.system('python gensimhlt.py') != 0: # cannot just import or else this screws up singleton services like MessageLogger when we expand pat.py below
        raise RuntimeError('gensimhlt.py does not work')

    print 'testing reco.py (may need to expand if you have modified the base reconstruction)'
    if os.system('python reco.py') != 0:
        raise RuntimeError('reco.py does not work')

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

os.system('mkdir -p crab/gensimhltrecopat')
os.system('mkdir -p crab/psets/gensimhltrecopat')
testing = 'testing' in sys.argv

def submit(name, tau0, mass):
    pset_fn = 'crab/psets/gensimhltrecopat/%(name)s.py' % locals()
    new_py = open('gensimhlt.py').read()
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
    else:
        raise RuntimeError("don't know what LSP to use")
    open(pset_fn, 'wt').write(new_py)
    open('crab.cfg','wt').write(crab_cfg % locals())
    if not testing:
        os.system('crab -create')
        for i in xrange(4):
            os.system('crab -submit 500')
        os.system('rm -f crab.cfg reco.pyc')

tau0s = [0., 0.01, 0.1, 0.3, 1.0, 9.9]
masses = [200, 300, 400, 600, 800, 1000]

to_do = [(0.3, m) for m in masses] + [(t, 300) for t in tau0s]

for tau0, mass in to_do:
    name = 'neutralino_tau%04ium_M%04i' % (int(tau0*1000), mass)
    submit(name, tau0, mass)
