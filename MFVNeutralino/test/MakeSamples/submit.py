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
output_file = reco.root
events_per_job = 5
total_number_of_events = 10
first_lumi = 1

[USER]
script_exe = twostep.csh
additional_input_files = minSLHA.spc, reco.py, pat.py
ui_working_dir = crab/gensimhltrecopat/crab_mfv_%(name)s
copy_data = 1
storage_element = T3_US_FNALLPC
check_user_remote_dir = 0
publish_data = 1
publish_data_name = testtwostep_mfv_%(name)s
dbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
jmt_externals_hack = pythia8_hack
jmt_externals_hack_dirs = GeneratorInterface/Pythia8Interface

[GRID]
se_black_list = metu.edu.tr,uoi.gr,troitsk.ru,brunel.ac.uk,bris.ac.uk,kfki.hu,pi.infn.it,ihep.su,ciemat.es,jinr-t1.ru,nectec.or.th,ts.infn.it,hep.by,cinvestav.mx
'''

if os.environ['USER'] != 'tucker':
    raw_input('do you have the jmt_externals_hack for crab? if not, ^C now.')

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
open('pat.py', 'wt').write(_pat.process.dumpPython())

os.system('mkdir -p crab/gensimhltrecopat')
os.system('mkdir -p psets/gensimhltrecopat')
testing = 'testing' in sys.argv

def submit(name, tau0, mass):
    pset_fn = 'psets/gensimhltrecopat/%(name)s.py' % locals()
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
        os.system('crab -create -submit')
        os.system('rm -f crab.cfg reco.pyc')

tau0s = [0., 0.01, 0.1, 1.0, 9.9]
masses = [200, 400, 600, 800, 1000]

tau0s = [1.0]
masses = [400]

for tau0 in tau0s:
    for mass in masses:
        name = 'neutralino_tau%04ium_M%04i' % (int(tau0*1000), mass)
        submit(name, tau0, mass)
