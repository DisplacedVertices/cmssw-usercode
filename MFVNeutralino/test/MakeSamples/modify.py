import FWCore.ParameterSet.Config as cms

def set_particle_tau0(process, id, tau0):
    params = [x for x in process.generator.PythiaParameters.processParameters.value() if ':tau0' not in x]
    process.generator.PythiaParameters.processParameters = params
    process.generator.PythiaParameters.processParameters.append('%i:tau0 = %f' % (id, tau0)) # tau0 is in mm by pythia convention

def set_gluino_tau0(process, tau0):
    set_particle_tau0(process, 1000021, tau0)

def set_neutralino_tau0(process, tau0):
    set_particle_tau0(process, 1000022, tau0)

def set_mass(m_gluino, fn='minSLHA.spc'):
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

DECAY   1000021     0.01E+00   # gluino decays
#           BR         NDA      ID1       ID2       ID3
     0.5E+00          3            3          5           6   # BR(~g -> s b t)
     0.5E+00          3           -3         -5          -6   # BR(~g -> sbar bbar tbar)
'''
    open(fn, 'wt').write(slha % locals())

def set_masses(m_gluino, m_neutralino, fn='minSLHA.spc'):
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

DECAY   1000022     0.01E+00   # neutralino decays
#           BR         NDA      ID1       ID2       ID3
     0.5E+00          3            3          5           6   # BR(~chi_10 -> s b t)
     0.5E+00          3           -3         -5          -6   # BR(~chi_10 -> sbar bbar tbar)
'''
    open(fn, 'wt').write(slha % locals())


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

def nopu(process):
    process.load('SimGeneral.MixingModule.mixNoPU_cfi')

def ttbar(process):
    process.generator.PythiaParameters.processParameters = cms.vstring(
        'Main:timesAllowErrors = 10000',
        'Top:gg2ttbar = on',
        'Top:qqbar2ttbar = on',
        '24:onMode = off',
        '24:onIfAny = 1 2 3 4 5',
        'Tune:pp 5',
        )
