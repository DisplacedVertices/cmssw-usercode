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


# JMTBAD these two don't do the full story for removing BS
# pos/tilt/width

def gauss_bs(process):
    from IOMC.EventVertexGenerators.VtxSmearedParameters_cfi import VtxSmearedCommon, GaussVtxSmearingParameters
    process.VtxSmeared = cms.EDProducer("GaussEvtVtxGenerator",
                                        GaussVtxSmearingParameters,
                                        VtxSmearedCommon
                                        )

def center_bs(process):
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
