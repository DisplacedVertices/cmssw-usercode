from itertools import product
import FWCore.ParameterSet.Config as cms

def set_minbias(process):
    process.generator.PythiaParameters.processParameters = cms.vstring(
        'SoftQCD:nonDiffractive = on', 
        'SoftQCD:singleDiffractive = on', 
        'SoftQCD:doubleDiffractive = on'
        )

def set_qcdht(process, which):
    process.externalLHEProducer.args = [{
            # yes octal
            0700: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/madgraph/V5_2.2.2/QCD_HT_LO_MLM/QCD_HT700to1000/v1/QCD_HT700to1000_tarball.tar.xz',
            1000: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/madgraph/V5_2.2.2/QCD_HT_LO_MLM/QCD_HT1000to1500/v1/QCD_HT1000to1500_tarball.tar.xz',
            1500: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/madgraph/V5_2.2.2/QCD_HT_LO_MLM/QCD_HT1500to2000/v1/QCD_HT1500to2000_tarball.tar.xz',
            2000: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/madgraph/V5_2.2.2/QCD_HT_LO_MLM/QCD_HT2000toInf/v1/QCD_HT2000toInf_tarball.tar.xz',
            }[which]]

def set_qcdht2000(process):
    process.externalLHEProducer.args = ['/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/madgraph/V5_2.2.2/QCD_HT_LO_MLM/QCD_HT2000toInf/v1/QCD_HT2000toInf_tarball.tar.xz']

def set_ttbar(process):
    process.generator.PythiaParameters.processParameters = cms.vstring(
        'Top:gg2ttbar = on',
        'Top:qqbar2ttbar = on',
        '24:onMode = off',
        '24:onIfAny = 1 2 3 4 5',
        'Tune:pp 5',
        )

def set_leptoquark(process, lifetime, mass, generation):
    params = [
        'LeptoQuark:gg2LQLQbar = on',
        'LeptoQuark:qqbar2LQLQbar = on',
        '42:m0 = %s' % mass,
        '42:tau0 = %s' % lifetime,
        ]

    if generation == 2:
        params.append('42:0:products = 4 -13')
    elif generation != 1:
        raise ValueError('generation can be 1 or 2')

    process.generator.PythiaParameters.processParameters = cms.vstring(*params)

def set_particle_tau0(process, id, tau0):
    params = [x for x in process.generator.PythiaParameters.processParameters.value() if ':tau0' not in x]
    process.generator.PythiaParameters.processParameters = params
    process.generator.PythiaParameters.processParameters.append('%i:tau0 = %f' % (id, tau0)) # tau0 is in mm by pythia convention

def set_energy(process, energy):
    process.generator.comEnergy = energy # JMTBAD does nothing if LHE gridpacks being used

def set_tune(process, tune):
    process.generator.PythiaParameters.tuneSettings = cms.vstring('Tune:pp %i' % tune)

def set_gluino_tau0(process, tau0):
    set_particle_tau0(process, 1000021, tau0)

def set_neutralino_tau0(process, tau0):
    set_particle_tau0(process, 1000022, tau0)

def set_rhadrons_on(process):
    process.generator.PythiaParameters.processParameters.append('RHadrons:allow = on')

def slha(tau0, m_gluino, m_neutralino, decay_idses, fn=None):
    width = 0.0197e-11 / tau0 # tau0 in mm

    n_decay_idses = len(decay_idses)
    sum_br = 0.
    decay_strs = []
    for decay_ids in decay_idses:
        if len(decay_ids) == 2 and type(decay_ids[0]) == float and (type(decay_ids[1]) == tuple or type(decay_ids[1]) == list):
            br, decay_ids = decay_ids
        else:
            br = 1./n_decay_idses
        sum_br += br

        n_decay_ids = len(decay_ids)
        if n_decay_ids not in (2,3,4):
            raise ValueError('decay_ids must have len 2 or 3: %r' % decay_ids)

        decay_strs.append('\t%.2E\t%i\t' % (br, n_decay_ids) +  '\t'.join(str(x) for x in decay_ids))

    if abs(sum_br - 1) > 1e-4:
        raise ValueError('brs did not sum to 1')

    if m_neutralino is None:
        slha = '''
BLOCK SPINFO  # Spectrum calculator information
     1   Minimal    # spectrum calculator
     2   1.0.0         # version number
#
BLOCK MODSEL  # Model selection
     1     1   #
#

BLOCK MASS  # Mass Spectrum
# PDG code           mass       particle
  1000021     %(m_gluino)E       # ~g

DECAY   1000021     %(width)E   # gluino decays
#          BR         NDA      ID1       ID2
'''
    else:
        slha = '''
BLOCK SPINFO  # Spectrum calculator information
     1   Minimal    # spectrum calculator
     2   1.0.0         # version number
#
BLOCK MODSEL  # Model selection
     1     1   #
#

BLOCK MASS  # Mass Spectrum
# PDG code           mass       particle
  1000021     %(m_gluino)E       # ~g
  1000022     %(m_neutralino)E   # ~chi_10

DECAY   1000021     0.01E+00   # gluino decays
#          BR         NDA      ID1       ID2
    1.0E00            2      1000022    21   # BR(~g -> ~chi_10  g)

DECAY   1000022     %(width)E   # neutralino decays
#           BR         NDA      ID1       ID2       ID3
'''

    slha += '\n'.join(decay_strs) + '\n'
    slha = slha % locals()
    if fn:
        open(fn, 'wt').write(slha)

    return slha

def slha_mfv(tau0, m_gluino, m_neutralino, fn=None):
    return slha(tau0, m_gluino, m_neutralino, [(0.5, (3,5,6)), (0.5, (-3,-5,-6))], fn)

def slha_mfv_neutralino(tau0, m_neutralino, fn=None):
    return slha_mfv(tau0, m_neutralino+5, m_neutralino, fn)

def slha_mfv_gluino(tau0, m_gluino, fn=None):
    return slha_mfv(tau0, m_gluino, None, fn)

def set_mfv_neutralino(process, tau0, m_neutralino):
    process.generator.PythiaParameters.processParameters = cms.vstring(
        'SUSY:gg2gluinogluino = on',
        'SUSY:qqbar2gluinogluino = on',
        'SUSY:idA = 1000021',
        'SUSY:idB = 1000021',
        )

    set_neutralino_tau0(process, tau0)

    slha = slha_mfv_neutralino(tau0, m_neutralino)
    process.generator.SLHATableForPythia8 = cms.string(slha)

def set_mfv_gluino(process, tau0, m_gluino):
    process.generator.PythiaParameters.processParameters = cms.vstring(
        'SUSY:gg2gluinogluino = on',
        'SUSY:qqbar2gluinogluino = on',
        'SUSY:idA = 1000021',
        'SUSY:idB = 1000021',
        )

    set_gluino_tau0(process, tau0)
    set_rhadrons_on(process)

    slha = slha_mfv_gluino(tau0, m_gluino)
    process.generator.SLHATableForPythia8 = cms.string(slha)
    
def set_gluino_ddbar(process, tau0, m_gluino):
    process.generator.PythiaParameters.processParameters = cms.vstring(
        'SUSY:gg2gluinogluino = on',
        'SUSY:qqbar2gluinogluino = on',
        'SUSY:idA = 1000021',
        'SUSY:idB = 1000021',
        )

    set_gluino_tau0(process, tau0)
    set_rhadrons_on(process)

    slhaf = slha(tau0, m_gluino, None, [(1., (1,-1))])
    process.generator.SLHATableForPythia8 = cms.string(slhaf)

########################################################################

class scanpackbase(object):
    jobs_per_batch = 5000
    events_per_job = 200

    def __init__(self):
        self.name = self.__class__.__name__
        self.samples = list(product(self.kinds, self.taus, self.masses))
        self.njobs = 0
        self.job2isample = []
        for isample, (kind,tau,mass) in enumerate(self.samples):
            eps, epj = self.events_per_sample(kind,tau,mass), self.events_per_job
            assert eps > epj and eps % epj == 0
            njobs = eps / epj

            self.njobs += njobs
            self.job2isample += [isample]*njobs
        assert self.njobs > 0

        self.jobs_in_last_batch = self.njobs % self.jobs_per_batch
        if self.jobs_in_last_batch == 0:
            self.jobs_in_last_batch = self.jobs_per_batch

        int_ceil = lambda x,y: (x+y-1)/y
        self.nbatches = int_ceil(self.njobs, self.jobs_per_batch)
        self.ibatch = 0

    def sample(self, batch, job):
        assert 0 <= batch < self.nbatches
        assert 0 <= job < self.jobs_per_batch
        if batch == self.nbatches - 1:
            assert job < self.jobs_in_last_batch
        return self.samples[self.job2isample[batch * self.jobs_per_batch + job]]

    def __iter__(self):
        for self.ibatch in xrange(self.nbatches):
            yield self

    @property
    def nevents(self):
        if self.ibatch < self.nbatches - 1:
            njobs = self.jobs_per_batch
        else:
            njobs = self.jobs_in_last_batch
        return self.events_per_job * njobs

    @property
    def batch_name(self):
        return '%s_%s' % (self.name, self.ibatch)

class scanpacktest(scanpackbase):
    kinds = [set_mfv_neutralino, set_gluino_ddbar]
    taus = [tau/1000. for tau in [100,10000]]
    masses = [400, 800]

    jobs_per_batch = 50
    events_per_job = 10
    def events_per_sample(self, kind, tau, mass):
        return 100

class scanpacktest2(scanpackbase):
    kinds = [set_mfv_neutralino, set_gluino_ddbar]
    taus = [tau/1000. for tau in [300,10000]]
    masses = [600, 800]

    jobs_per_batch = 39
    def events_per_sample(self, kind, tau, mass):
        return 1000

class scanpack1(scanpackbase):
    kinds = [set_mfv_neutralino, set_gluino_ddbar]
    taus = [tau/1000. for tau in range(100, 1000, 300) + range(1000, 40000, 3000) + range(40000, 1000001, 160000)]
    masses = range(300, 600, 100) + range(600, 3001, 200)

    def events_per_sample(self, kind, tau, mass):
        return 10000

def get_scanpack(x):
    return {
        'scanpacktest': scanpacktest,
        'scanpacktest2': scanpacktest2,
        'scanpack1': scanpack1,
        }[x]()

def do_scanpack(process, x, batch, job):
    sp = get_scanpack(x)
    set_kind, tau, mass = sp.sample(batch, job)
    print 'do_scanpack: %s nbatches %s njobs %s lastjobs %s batch %s job %s kind %s tau %s mass %s' % (x, sp.nbatches, sp.njobs, sp.jobs_in_last_batch, batch, job, set_kind.__name__, tau, mass)
    set_kind(process, tau, mass)

########################################################################

def set_fns(process, list_fn, jobnum):
    fns = [fn.strip() for fn in open(list_fn).readlines() if fn.strip()]
    if jobnum >= 0:
        if jobnum >= len(fns):
            raise ValueError('jobnum %i too big for %i list' % (jobnum, len(fns)))
        fns = [fns[jobnum]]
    process.source.fileNames = fns

def set_nopu(process):
    process.load('SimGeneral.MixingModule.mixNoPU_cfi')

def set_pu15(process):
    process.mix.input.nbPileupEvents.probFunctionVariable = cms.vint32(*range(50))
    process.mix.input.nbPileupEvents.probValue = cms.vdouble(0.000108643, 0.000388957, 0.000332882, 0.00038397, 0.000549167, 0.00105412, 0.00459007, 0.0210314, 0.0573688, 0.103986, 0.142369, 0.157729, 0.147685, 0.121027, 0.08855, 0.0582866, 0.0348526, 0.019457, 0.0107907, 0.00654313, 0.00463195, 0.00370927, 0.0031137, 0.00261141, 0.00215499, 0.00174491, 0.00138268, 0.00106731, 0.000798828, 0.00057785, 0.00040336, 0.00027161, 0.000176535, 0.00011092, 6.75502e-05, 4.00323e-05, 2.32123e-05, 1.32585e-05, 7.51611e-06, 4.25902e-06, 2.42513e-06, 1.39077e-06, 8.02452e-07, 4.64159e-07, 2.67845e-07, 1.5344e-07, 8.68966e-08, 4.84931e-08, 2.6606e-08, 1.433e-08)

def set_pu16(process):
    process.mix.input.nbPileupEvents.probFunctionVariable = cms.vint32(*range(75))
    process.mix.input.nbPileupEvents.probValue = cms.vdouble(1.78653e-05, 2.56602e-05, 5.27857e-05, 8.88954e-05, 0.000109362, 0.000140973, 0.000240998, 0.00071209, 0.00130121, 0.00245255, 0.00502589, 0.00919534, 0.0146697, 0.0204126, 0.0267586, 0.0337697, 0.0401478, 0.0450159, 0.0490577, 0.0524855, 0.0548159, 0.0559937, 0.0554468, 0.0537687, 0.0512055, 0.0476713, 0.0435312, 0.0393107, 0.0349812, 0.0307413, 0.0272425, 0.0237115, 0.0208329, 0.0182459, 0.0160712, 0.0142498, 0.012804, 0.011571, 0.010547, 0.00959489, 0.00891718, 0.00829292, 0.0076195, 0.0069806, 0.0062025, 0.00546581, 0.00484127, 0.00407168, 0.00337681, 0.00269893, 0.00212473, 0.00160208, 0.00117884, 0.000859662, 0.000569085, 0.000365431, 0.000243565, 0.00015688, 9.88128e-05, 6.53783e-05, 3.73924e-05, 2.61382e-05, 2.0307e-05, 1.73032e-05, 1.435e-05, 1.36486e-05, 1.35555e-05, 1.37491e-05, 1.34255e-05, 1.33987e-05, 1.34061e-05, 1.34211e-05, 1.34177e-05, 1.32959e-05, 1.33287e-05)

def prefer_it(process, name, connect, record, tag):
    from CondCore.DBCommon.CondDBSetup_cfi import CondDBSetup
    es_source = cms.ESSource('PoolDBESSource', CondDBSetup, connect = cms.string(connect), toGet = cms.VPSet(cms.PSet(record = cms.string(record), tag = cms.string(tag))))
    es_prefer = cms.ESPrefer('PoolDBESSource', name)
    setattr(process, name, es_source)
    setattr(process, 'es_prefer_' + name, es_prefer)

def ideal_bs_tag(process):
    prefer_it(process, 'idealCenteredBS', 'frontier://FrontierProd/CMS_COND_31X_BEAMSPOT', 'BeamSpotObjectsRcd', 'Ideal_Centered_MC_44_V1')

def gauss_bs(process, noxy=False, noz=False):
    ideal_bs_tag(process)
    from IOMC.EventVertexGenerators.VtxSmearedParameters_cfi import VtxSmearedCommon, GaussVtxSmearingParameters
    process.VtxSmeared = cms.EDProducer("GaussEvtVtxGenerator", GaussVtxSmearingParameters, VtxSmearedCommon)
    if noxy:
        process.VtxSmeared.SigmaX = 1e-12
        process.VtxSmeared.SigmaY = 1e-12
    if noz:
        process.VtxSmeared.SigmaZ = 1e-12

def center_bs(process):
    ideal_bs_tag(process)
    process.VtxSmeared.X0 = 0
    process.VtxSmeared.Y0 = 0
    process.VtxSmeared.Y0 = 0

def tracker_alignment(process, tag):
    prefer_it(process, 'tkAlign', 'frontier://FrontierProd/CMS_COND_ALIGNMENT', 'TrackerAlignmentRcd', 'TrackerAlignment_2010RealisticPlus%s_mc' % tag.capitalize())

def keep_random_info(process):
    process.output.outputCommands += [
        'drop *_randomEngineStateProducer_*_*',
        'drop CrossingFramePlaybackInfoExtended_*_*_*'
        ]

def castor_thing(process):
    prefer_it(process, 'castorThing', 'frontier://FrontierProd/CMS_COND_HCAL_000', 'CastorSaturationCorrsRcd', 'CastorSaturationCorrs_v1.00_mc')

def keep_tracker_extras(process):
    process.output.outputCommands += [
        'keep recoTrackExtras_generalTracks__*',
        'keep TrackingRecHitsOwned_generalTracks__*'
        ]

class DummyBeamSpots():
    bowing = cms.PSet(
            X0 = cms.double(0.246344),
            Y0 = cms.double(0.389749),
            Z0 = cms.double(0.402745),
            SigmaZ = cms.double(5.98845),
            dxdz = cms.double(1.70494e-05),
            dydz = cms.double(-2.13481e-06),
            BeamWidthX = cms.double(0.00151667),
            BeamWidthY = cms.double(0.00151464),
            covariance = cms.vdouble(1.24561e-10, 5.32196e-13, 0, 0, 0, 0, 0, 1.24935e-10, 0, 0, 0, 0, 0, 0.00445375, 0, 0, 0, 0, 0.00222686, 0, 0, 0, 3.36155e-12, 2.7567e-14, 0, 3.37374e-12, 0, 2.97592e-10),
            EmittanceX = cms.double(0),
            EmittanceY = cms.double(0),
            BetaStar = cms.double(0),
        )

    curl = cms.PSet(
            X0 = cms.double(0.246597),
            Y0 = cms.double(0.38699),
            Z0 = cms.double(0.314451),
            SigmaZ = cms.double(5.99379),
            dxdz = cms.double(-1.9081e-06),
            dydz = cms.double(-1.02914e-05),
            BeamWidthX = cms.double(0.00147516),
            BeamWidthY = cms.double(0.00150106),
            covariance = cms.vdouble(1.23255e-10, 5.60119e-13, 0, 0, 0, 0, 0, 1.22964e-10, 0, 0, 0, 0, 0, 0.0045269, 0, 0, 0, 0, 0.00226344, 0, 0, 0, 3.30386e-12, 2.14557e-14, 0, 3.3566e-12, 0, 2.93467e-10),
            EmittanceX = cms.double(0),
            EmittanceY = cms.double(0),
            BetaStar = cms.double(0),
        )

    elliptical = cms.PSet(
            X0 = cms.double(0.246156),
            Y0 = cms.double(0.389613),
            Z0 = cms.double(0.288198),
            SigmaZ = cms.double(5.97317),
            dxdz = cms.double(5.21863e-06),
            dydz = cms.double(7.79036e-06),
            BeamWidthX = cms.double(0.00149346),
            BeamWidthY = cms.double(0.00148959),
            covariance = cms.vdouble(1.23521e-10, 8.78629e-13, 0, 0, 0, 0, 0, 1.22967e-10, 0, 0, 0, 0, 0, 0.00439882, 0, 0, 0, 0, 0.0021994, 0, 0, 0, 3.33981e-12, 3.81918e-14, 0, 3.32571e-12, 0, 2.91985e-10),
            EmittanceX = cms.double(0),
            EmittanceY = cms.double(0),
            BetaStar = cms.double(0),
        )

    radial = cms.PSet(
            X0 = cms.double(0.246322),
            Y0 = cms.double(0.389811),
            Z0 = cms.double(0.327943),
            SigmaZ = cms.double(6.08119),
            dxdz = cms.double(6.83738e-06),
            dydz = cms.double(1.8884e-07),
            BeamWidthX = cms.double(0.00149758),
            BeamWidthY = cms.double(0.00153033),
            covariance = cms.vdouble(1.22914e-10, 5.21468e-13, 0, 0, 0, 0, 0, 1.24135e-10, 0, 0, 0, 0, 0, 0.00459276, 0, 0, 0, 0, 0.00229637, 0, 0, 0, 3.28346e-12, 1.84415e-14, 0, 3.32401e-12, 0, 2.91313e-10),
            EmittanceX = cms.double(0),
            EmittanceY = cms.double(0),
            BetaStar = cms.double(0),
        )

    sagitta = cms.PSet(
            X0 = cms.double(0.235756),
            Y0 = cms.double(0.389839),
            Z0 = cms.double(0.451828),
            SigmaZ = cms.double(5.9656),
            dxdz = cms.double(-6.12007e-06),
            dydz = cms.double(-3.34286e-06),
            BeamWidthX = cms.double(0.00142781),
            BeamWidthY = cms.double(0.00146079),
            covariance = cms.vdouble(1.21587e-10, 1.2445e-12, 0, 0, 0, 0, 0, 1.22063e-10, 0, 0, 0, 0, 0, 0.00443525, 0, 0, 0, 0, 0.00221762, 0, 0, 0, 3.24618e-12, 2.20384e-14, 0, 3.29028e-12, 0, 2.87833e-10),
            EmittanceX = cms.double(0),
            EmittanceY = cms.double(0),
            BetaStar = cms.double(0),
        )

    skew = cms.PSet(
            X0 = cms.double(0.246258),
            Y0 = cms.double(0.389962),
            Z0 = cms.double(0.386416),
            SigmaZ = cms.double(6.02712),
            dxdz = cms.double(-0.00011416),
            dydz = cms.double(-7.07232e-06),
            BeamWidthX = cms.double(0.00164608),
            BeamWidthY = cms.double(0.00151397),
            covariance = cms.vdouble(1.26645e-10, 7.7728e-14, 0, 0, 0, 0, 0, 1.25663e-10, 0, 0, 0, 0, 0, 0.00445011, 0, 0, 0, 0, 0.00222484, 0, 0, 0, 3.39247e-12, 1.9986e-14, 0, 3.34669e-12, 0, 3.14378e-10),
            EmittanceX = cms.double(0),
            EmittanceY = cms.double(0),
            BetaStar = cms.double(0),
        )

    telescope = cms.PSet(
            X0 = cms.double(0.245667),
            Y0 = cms.double(0.386495),
            Z0 = cms.double(0.425672),
            SigmaZ = cms.double(6.16219),
            dxdz = cms.double(3.75215e-06),
            dydz = cms.double(-1.91476e-06),
            BeamWidthX = cms.double(0),
            BeamWidthY = cms.double(0),
            covariance = cms.vdouble(3.44758e-10, 3.61193e-13, 0, 0, 0, 0, 0, 3.46413e-10, 0, 0, 0, 0, 0, 0.000100795, 0, 0, 0, 0, 9.63705e-05, 0, 0, 0, 9.41413e-12, 7.89166e-14, 0, 9.46686e-12, 0, 0),
            EmittanceX = cms.double(0),
            EmittanceY = cms.double(0),
            BetaStar = cms.double(0),
        )

    twist = cms.PSet(
            X0 = cms.double(0.246196),
            Y0 = cms.double(0.389666),
            Z0 = cms.double(0.293139),
            SigmaZ = cms.double(6.0066),
            dxdz = cms.double(4.09512e-06),
            dydz = cms.double(1.19775e-05),
            BeamWidthX = cms.double(0.00148173),
            BeamWidthY = cms.double(0.00149055),
            covariance = cms.vdouble(1.22449e-10, 0, 0, 0, 0, 0, 0, 1.22109e-10, 0, 0, 0, 0, 0, 0.0045879, 0, 0, 0, 0, 0.00229394, 0, 0, 0, 3.27196e-12, 7.22971e-15, 0, 3.27492e-12, 0, 2.89948e-10),
            EmittanceX = cms.double(0),
            EmittanceY = cms.double(0),
            BetaStar = cms.double(0),
        )

    zexpansion = cms.PSet(
            X0 = cms.double(0.246214),
            Y0 = cms.double(0.389698),
            Z0 = cms.double(0.394112),
            SigmaZ = cms.double(6.00186),
            dxdz = cms.double(3.61695e-06),
            dydz = cms.double(1.45456e-06),
            BeamWidthX = cms.double(0.0014962),
            BeamWidthY = cms.double(0.00149599),
            covariance = cms.vdouble(1.24303e-10, 7.70197e-13, 0, 0, 0, 0, 0, 1.22716e-10, 0, 0, 0, 0, 0, 0.00449324, 0, 0, 0, 0, 0.00224661, 0, 0, 0, 3.3007e-12, 2.37285e-14, 0, 3.20966e-12, 0, 2.94185e-10),
            EmittanceX = cms.double(0),
            EmittanceY = cms.double(0),
            BetaStar = cms.double(0),
        )
    
def dummy_beamspot(process, tag):
    params = getattr(DummyBeamSpots, tag)

    process.myBeamSpot = cms.EDProducer('DummyBeamSpotProducer', params)

    for name, path in process.paths.items():
        if path._seq is not None:
            path.insert(0, process.myBeamSpot)

    for name, out in process.outputModules.items():
        new_cmds = []
        for cmd in out.outputCommands:
            if 'offlineBeamSpot' in cmd:
                new_cmds.append(cmd.replace('offlineBeamSpot', 'myBeamSpot'))
        out.outputCommands += new_cmds

    import itertools
    from PhysicsTools.PatAlgos.tools.helpers import massSearchReplaceAnyInputTag
    for path_name, path in itertools.chain(process.paths.iteritems(), process.endpaths.iteritems()):
        massSearchReplaceAnyInputTag(path, cms.InputTag('offlineBeamSpot'), cms.InputTag('myBeamSpot'), verbose=True)

def set_weakmode(process, weakmode):
    tracker_alignment(process, weakmode)
    if process.name_() != 'HLT':
        dummy_beamspot(process, weakmode)

def hlt_filter(process, hlt_path):
    from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
    process.triggerFilter = hltHighLevel.clone()
    process.triggerFilter.HLTPaths = [hlt_path]
    process.triggerFilter.andOr = True # = OR
    process_out = None
    try:
        process_out = process.output
    except AttributeError:
        process_out = process.out
    if hasattr(process_out, 'SelectEvents'):
        raise ValueError('process_out already has SelectEvents: %r' % process_out.SelectEvents)
    process_out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('ptriggerFilter'))
    for name, path in process.paths.items():
        path.insert(0, process.triggerFilter)
    process.ptriggerFilter = cms.Path(process.triggerFilter)
    if hasattr(process, 'schedule'):
        process.schedule.insert(0, process.ptriggerFilter)

def deterministic_seeds(process, base, salt, job, save_fn=''):
    salt = sum(ord(x) for x in str(salt))
    def check_assert(x):
        assert x
        return x
    seed_psets = [(k,v) for k,v in process.RandomNumberGeneratorService.parameters_().iteritems()
                  if isinstance(v, cms.PSet) and check_assert(not hasattr(v, 'initialSeedSet')) and hasattr(v, 'initialSeed')]
    seed_psets.sort(key = lambda x: x[0])
    n = len(seed_psets)
    for i, (k,_) in enumerate(seed_psets):
        getattr(process.RandomNumberGeneratorService, k).initialSeed = base + salt + job*n + i
    if save_fn:
        process.RandomNumberGeneratorService.saveFileName =  cms.untracked.string(save_fn)

def randomize_seeds(process, save_fn='RandomEngineState.xml'):
    from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
    randHelper =  RandomNumberServiceHelper(process.RandomNumberGeneratorService)
    randHelper.populate()
    if save_fn:
        process.RandomNumberGeneratorService.saveFileName =  cms.untracked.string(save_fn)

def set_trackersim16(process):
    prefer_it(process, 'tk16pixdyneff', 'frontier://FrontierProd/CMS_CONDITIONS', 'SiPixelDynamicInefficiencyRcd', 'SiPixelDynamicInefficiency_13TeV_v3_mc')
    prefer_it(process, 'tk16pixqual',   'frontier://FrontierProd/CMS_CONDITIONS', 'SiPixelQualityFromDbRcd',       'SiPixelQuality_v36_mc')
    prefer_it(process, 'tk16strqual',   'frontier://FrontierProd/CMS_CONDITIONS', 'SiStripBadChannelRcd',          'SiStripBadComponents_realisticMC_for2016_v1_mc')

def set_trackerali16(process):
    prefer_it(process, 'tkAlign', 'frontier://FrontierProd/CMS_CONDITIONS', 'TrackerAlignmentRcd', 'TrackerAlignment_Asymptotic_Run2016_v2_mc')

def set_cond15(process):
    prefer_it(process, 'tk15pixdyneff', 'frontier://FrontierProd/CMS_CONDITIONS', 'SiPixelDynamicInefficiencyRcd', 'SiPixelDynamicInefficiency_13TeV_v1_mc')
    prefer_it(process, 'tk15pixqual',   'frontier://FrontierProd/CMS_CONDITIONS', 'SiPixelQualityFromDbRcd',       'SiPixelQuality_v28_mc')
    prefer_it(process, 'tk15strqual',   'frontier://FrontierProd/CMS_CONDITIONS', 'SiStripBadChannelRcd',          'SiStripBadComponents_realisticMC_for2015_v1_mc')
    prefer_it(process, 'tkAlign',       'frontier://FrontierProd/CMS_CONDITIONS', 'TrackerAlignmentRcd',           'TrackerAlignment_run2Asymptotic_v1_mc')

def set_oldduplicatemerge(process, outliers_rejection=False):
    if process.name_() == 'RECO':
        process.duplicateTrackClassifier.mva.maxChi2n = [9999., 9999., 9999.]
        for x in process.duplicateTrackClassifier, process.jetCoreRegionalStep, process.muonSeededTracksInOutClassifier, process.muonSeededTracksOutInClassifier:
            x.mva.maxDzWrtBS = [3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38] # I think the PV cuts get used, which are same
            x.mva.minHits = [0, 0, 0]
            x.mva.minNVtxTrk = 0
        if outliers_rejection:
            process.mergedDuplicateTracks.Fitter = 'KFFittingSmootherWithOutliersRejectionAndRK'

def set_hip_simulation(process, scale=1.0): # scale relative to 6e33
    for x in 'process.SiStripSimBlock process.stripDigitizer process.theDigitizers.strip process.theDigitizersValid.strip process.theDigitizersMixPreMix.strip process.theDigitizersMixPreMixValid.strip process.mix.digitizers.strip process.mixData'.split():
        try:
            y = eval(x)
        except AttributeError:
            continue
        y.APVSaturationFromHIP = True
        y.APVSaturationProbScaling = scale

def set_hip_mitigation(process):
    from RecoTracker.Configuration.customizeMinPtForHitRecoveryInGluedDet import customizeHitRecoveryInGluedDetOn
    customizeHitRecoveryInGluedDetOn(process)

if __name__ == '__main__':
    if 0:
        from gensim import process
        for batch in 0,1,2,3: #,4
            for job in xrange(39):
                print batch, job,
                do_scanpack(process, 'scanpack1', batch, job)
