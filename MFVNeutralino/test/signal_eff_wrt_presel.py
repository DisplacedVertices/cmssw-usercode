#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
version = 'V27darksectorreviewm'

boosted = True
ps = plot_saver(plot_dir('sigeff_wrt_presel_%s_%s' % (version, "mLLP_eq_10pc" if boosted else "mLLP_eq_40pc")), size=(600,600), pdf=True, log=True, pdf_log=True)

#multijet = Samples.mfv_signal_samples_2018
#dijet = Samples.mfv_stopdbardbar_samples_2018

#HtoLLPto4j = Samples.mfv_HtoLLPto4j_samples_2017
#HtoLLPto4b = Samples.mfv_HtoLLPto4b_samples_2017
#ZprimetoLLPto4j = Samples.mfv_ZprimetoLLPto4j_samples_2017
#ZprimetoLLPto4b = Samples.mfv_ZprimetoLLPto4b_samples_2017

if boosted :

    HtoLLPto4j = [Samples.mfv_HtoLLPto4j_tau0p1mm_M1000_450_2017
     , Samples.mfv_HtoLLPto4j_tau0p1mm_M400_40_2017
     , Samples.mfv_HtoLLPto4j_tau0p1mm_M600_60_2017
     , Samples.mfv_HtoLLPto4j_tau0p1mm_M800_80_2017
     , Samples.mfv_HtoLLPto4j_tau10000mm_M1000_100_2017
     , Samples.mfv_HtoLLPto4j_tau10000mm_M400_40_2017
     , Samples.mfv_HtoLLPto4j_tau10000mm_M600_60_2017
     , Samples.mfv_HtoLLPto4j_tau10000mm_M800_80_2017
     , Samples.mfv_HtoLLPto4j_tau1000mm_M1000_100_2017
     , Samples.mfv_HtoLLPto4j_tau1000mm_M400_40_2017
     , Samples.mfv_HtoLLPto4j_tau1000mm_M600_60_2017
     , Samples.mfv_HtoLLPto4j_tau1000mm_M800_80_2017
     , Samples.mfv_HtoLLPto4j_tau100mm_M1000_100_2017
     , Samples.mfv_HtoLLPto4j_tau100mm_M400_40_2017
     , Samples.mfv_HtoLLPto4j_tau100mm_M600_60_2017
     , Samples.mfv_HtoLLPto4j_tau100mm_M800_80_2017
     , Samples.mfv_HtoLLPto4j_tau10mm_M1000_100_2017
     , Samples.mfv_HtoLLPto4j_tau10mm_M400_40_2017
     , Samples.mfv_HtoLLPto4j_tau10mm_M600_60_2017
     , Samples.mfv_HtoLLPto4j_tau10mm_M800_80_2017
     , Samples.mfv_HtoLLPto4j_tau1mm_M1000_100_2017
     , Samples.mfv_HtoLLPto4j_tau1mm_M400_40_2017
     , Samples.mfv_HtoLLPto4j_tau1mm_M600_60_2017
     , Samples.mfv_HtoLLPto4j_tau1mm_M800_80_2017
     ]

    HtoLLPto4b = [Samples.mfv_HtoLLPto4b_tau0p1mm_M1000_450_2017
     , Samples.mfv_HtoLLPto4b_tau0p1mm_M400_40_2017
     , Samples.mfv_HtoLLPto4b_tau0p1mm_M600_60_2017
     , Samples.mfv_HtoLLPto4b_tau0p1mm_M800_80_2017
     , Samples.mfv_HtoLLPto4b_tau10000mm_M1000_100_2017
     , Samples.mfv_HtoLLPto4b_tau10000mm_M400_40_2017
     , Samples.mfv_HtoLLPto4b_tau10000mm_M600_60_2017
     , Samples.mfv_HtoLLPto4b_tau10000mm_M800_80_2017
     , Samples.mfv_HtoLLPto4b_tau1000mm_M1000_100_2017
     , Samples.mfv_HtoLLPto4b_tau1000mm_M400_40_2017
     , Samples.mfv_HtoLLPto4b_tau1000mm_M600_60_2017
     , Samples.mfv_HtoLLPto4b_tau1000mm_M800_80_2017
     , Samples.mfv_HtoLLPto4b_tau100mm_M1000_100_2017
     , Samples.mfv_HtoLLPto4b_tau100mm_M400_40_2017
     , Samples.mfv_HtoLLPto4b_tau100mm_M600_60_2017
     , Samples.mfv_HtoLLPto4b_tau100mm_M800_80_2017
     , Samples.mfv_HtoLLPto4b_tau10mm_M1000_100_2017
     , Samples.mfv_HtoLLPto4b_tau10mm_M400_40_2017
     , Samples.mfv_HtoLLPto4b_tau10mm_M600_60_2017
     , Samples.mfv_HtoLLPto4b_tau10mm_M800_80_2017
     , Samples.mfv_HtoLLPto4b_tau1mm_M1000_100_2017
     , Samples.mfv_HtoLLPto4b_tau1mm_M400_40_2017
     , Samples.mfv_HtoLLPto4b_tau1mm_M600_60_2017
     , Samples.mfv_HtoLLPto4b_tau1mm_M800_80_2017
     ]

    ZprimetoLLPto4j = [Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M1000_100_2017
     , Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M1500_150_2017
     , Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M2000_200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M2500_250_2017
     , Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M3000_300_2017
     , Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M3500_350_2017
     , Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M4000_400_2017
     , Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M4500_450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M1000_100_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M1500_150_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M2000_200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M2500_250_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M3000_300_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M3500_350_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M4000_400_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M4500_450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M1000_100_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M1500_150_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M2000_200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M2500_250_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M3000_300_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M3500_350_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M4000_400_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M4500_450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M1000_100_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M1500_150_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M2000_200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M2500_250_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M3000_300_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M3500_350_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M4000_400_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M4500_450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M1000_100_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M1500_150_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M2000_200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M2500_250_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M3000_300_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M3500_350_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M4000_400_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M4500_450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M1000_100_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M1500_150_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M2000_200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M2500_250_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M3000_300_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M3500_350_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M4000_400_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M4500_450_2017
     ]

    ZprimetoLLPto4b = [Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M1000_100_2017
     , Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M1500_150_2017
     , Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M2000_200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M2500_250_2017
     , Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M3000_300_2017
     , Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M3500_350_2017
     , Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M4000_400_2017
     , Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M4500_450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M1000_100_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M1500_150_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M2000_200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M2500_250_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M3000_300_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M3500_350_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M4000_400_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M4500_450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M1000_100_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M1500_150_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M2000_200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M2500_250_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M3000_300_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M3500_350_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M4000_400_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M4500_450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M1000_100_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M1500_150_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M2000_200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M2500_250_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M3000_300_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M3500_350_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M4000_400_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M4500_450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M1000_100_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M1500_150_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M2000_200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M2500_250_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M3000_300_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M3500_350_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M4000_400_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M4500_450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M1000_100_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M1500_150_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M2000_200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M2500_250_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M3000_300_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M3500_350_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M4000_400_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M4500_450_2017
     ]

else :

    HtoLLPto4j = [Samples.mfv_HtoLLPto4j_tau0p1mm_M1000_450_2017
     , Samples.mfv_HtoLLPto4j_tau0p1mm_M400_150_2017
     , Samples.mfv_HtoLLPto4j_tau0p1mm_M600_250_2017
     , Samples.mfv_HtoLLPto4j_tau0p1mm_M800_350_2017
     , Samples.mfv_HtoLLPto4j_tau10000mm_M1000_450_2017
     , Samples.mfv_HtoLLPto4j_tau10000mm_M400_150_2017
     , Samples.mfv_HtoLLPto4j_tau10000mm_M600_250_2017
     , Samples.mfv_HtoLLPto4j_tau10000mm_M800_350_2017
     , Samples.mfv_HtoLLPto4j_tau1000mm_M1000_450_2017
     , Samples.mfv_HtoLLPto4j_tau1000mm_M400_150_2017
     , Samples.mfv_HtoLLPto4j_tau1000mm_M600_250_2017
     , Samples.mfv_HtoLLPto4j_tau1000mm_M800_350_2017
     , Samples.mfv_HtoLLPto4j_tau100mm_M1000_450_2017
     , Samples.mfv_HtoLLPto4j_tau100mm_M400_150_2017
     , Samples.mfv_HtoLLPto4j_tau100mm_M600_250_2017
     , Samples.mfv_HtoLLPto4j_tau100mm_M800_350_2017
     , Samples.mfv_HtoLLPto4j_tau10mm_M1000_450_2017
     , Samples.mfv_HtoLLPto4j_tau10mm_M400_150_2017
     , Samples.mfv_HtoLLPto4j_tau10mm_M600_250_2017
     , Samples.mfv_HtoLLPto4j_tau10mm_M800_350_2017
     , Samples.mfv_HtoLLPto4j_tau1mm_M1000_450_2017
     , Samples.mfv_HtoLLPto4j_tau1mm_M400_150_2017
     , Samples.mfv_HtoLLPto4j_tau1mm_M600_250_2017
     , Samples.mfv_HtoLLPto4j_tau1mm_M800_350_2017
     ]

    HtoLLPto4b = [Samples.mfv_HtoLLPto4b_tau0p1mm_M1000_450_2017
     , Samples.mfv_HtoLLPto4b_tau0p1mm_M400_150_2017
     , Samples.mfv_HtoLLPto4b_tau0p1mm_M600_250_2017
     , Samples.mfv_HtoLLPto4b_tau0p1mm_M800_350_2017
     , Samples.mfv_HtoLLPto4b_tau10000mm_M1000_450_2017
     , Samples.mfv_HtoLLPto4b_tau10000mm_M400_150_2017
     , Samples.mfv_HtoLLPto4b_tau10000mm_M600_250_2017
     , Samples.mfv_HtoLLPto4b_tau10000mm_M800_350_2017
     , Samples.mfv_HtoLLPto4b_tau1000mm_M1000_450_2017
     , Samples.mfv_HtoLLPto4b_tau1000mm_M400_150_2017
     , Samples.mfv_HtoLLPto4b_tau1000mm_M600_250_2017
     , Samples.mfv_HtoLLPto4b_tau1000mm_M800_350_2017
     , Samples.mfv_HtoLLPto4b_tau100mm_M1000_450_2017
     , Samples.mfv_HtoLLPto4b_tau100mm_M400_150_2017
     , Samples.mfv_HtoLLPto4b_tau100mm_M600_250_2017
     , Samples.mfv_HtoLLPto4b_tau100mm_M800_350_2017
     , Samples.mfv_HtoLLPto4b_tau10mm_M1000_450_2017
     , Samples.mfv_HtoLLPto4b_tau10mm_M400_150_2017
     , Samples.mfv_HtoLLPto4b_tau10mm_M600_250_2017
     , Samples.mfv_HtoLLPto4b_tau10mm_M800_350_2017
     , Samples.mfv_HtoLLPto4b_tau1mm_M1000_450_2017
     , Samples.mfv_HtoLLPto4b_tau1mm_M400_150_2017
     , Samples.mfv_HtoLLPto4b_tau1mm_M600_250_2017
     , Samples.mfv_HtoLLPto4b_tau1mm_M800_350_2017
     ]
    ZprimetoLLPto4j = [Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M1000_450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M1500_700_2017
     , Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M2000_950_2017
     , Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M2500_1200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M3000_1450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M3500_1700_2017
     , Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M4000_1950_2017
     , Samples.mfv_ZprimetoLLPto4j_tau0p1mm_M4500_2200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M1000_450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M1500_700_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M2000_950_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M2500_1200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M3000_1450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M3500_1700_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M4000_1950_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10000mm_M4500_2200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M1000_450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M1500_700_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M2000_950_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M2500_1200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M3000_1450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M3500_1700_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M4000_1950_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1000mm_M4500_2200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M1000_450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M1500_700_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M2000_950_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M2500_1200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M3000_1450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M3500_1700_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M4000_1950_2017
     , Samples.mfv_ZprimetoLLPto4j_tau100mm_M4500_2200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M1000_450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M1500_700_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M2500_1200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M3000_1450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M3500_1700_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M4000_1950_2017
     , Samples.mfv_ZprimetoLLPto4j_tau10mm_M4500_2200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M1000_450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M1500_700_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M2000_950_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M2500_1200_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M3000_1450_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M3500_1700_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M4000_1950_2017
     , Samples.mfv_ZprimetoLLPto4j_tau1mm_M4500_2200_2017
     ]

    ZprimetoLLPto4b = [Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M1000_450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M1500_700_2017
     , Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M2000_950_2017
     , Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M2500_1200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M3000_1450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M3500_1700_2017
     , Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M4000_1950_2017
     , Samples.mfv_ZprimetoLLPto4b_tau0p1mm_M4500_2200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M1000_450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M1500_700_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M2000_950_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M2500_1200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M3000_1450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M3500_1700_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M4000_1950_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10000mm_M4500_2200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M1000_450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M1500_700_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M2000_950_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M2500_1200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M3000_1450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M3500_1700_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M4000_1950_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1000mm_M4500_2200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M1000_450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M1500_700_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M2000_950_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M2500_1200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M3000_1450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M3500_1700_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M4000_1950_2017
     , Samples.mfv_ZprimetoLLPto4b_tau100mm_M4500_2200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M1000_450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M1500_700_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M2000_950_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M2500_1200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M3000_1450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M3500_1700_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M4000_1950_2017
     , Samples.mfv_ZprimetoLLPto4b_tau10mm_M4500_2200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M1000_450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M1500_700_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M2000_950_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M2500_1200_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M3000_1450_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M3500_1700_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M4000_1950_2017
     , Samples.mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2017
     ]


#for sample in multijet + dijet:
for sample in HtoLLPto4j + HtoLLPto4b + ZprimetoLLPto4j + ZprimetoLLPto4b:
    #fn = os.path.join('/uscms/home/joeyr/crabdirs/Histos_within_fiducial_fixed_beampipe_wrt_origin_correct_release%s' % version, sample.name + '.root')
    fn = os.path.join('/uscms/home/joeyr/crabdirs/Histos%s' % version, sample.name + '.root')
    if not os.path.exists(fn):
        print 'no', sample.name
        continue
    f = ROOT.TFile(fn)
    t = f.Get('SimpleTriggerResults/t')
    hr = draw_hist_register(t, True)
    cut_den = 'pEventPreSel'
    h_den = hr.draw('weight', cut_den, binning='1,0,1', goff=True)
    cut_num = 'pFullSel'
    h_num = hr.draw('weight', cut_num, binning='1,0,1', goff=True)

    den, _ = get_integral(h_den)
    num, _ = get_integral(h_num)
    eff, eff_l, eff_h = clopper_pearson(num, den) # ignore integral != entries, just get central value right
    if eff < 1e-6 : continue
    sample.y, sample.yl, sample.yh = eff, eff_l, eff_h
    print '%26s: efficiency = %.5f (%.5f, %.5f), %.5f raw events, den = %.5f (%.5f raw events)' % (sample.name, sample.y, sample.yl, sample.yh, h_num.GetEntries(), den, h_den.GetEntries())

per = PerSignal('efficiency', y_range=(1e-6,5.05))
per.add(HtoLLPto4j, title='H #rightarrow XX #rightarrow 4j, m(X) = %s*m(H)' % ("0.1" if boosted else "0.4"))
per.add(HtoLLPto4b, title='H #rightarrow XX #rightarrow 4b, m(X) = %s*m(H)' % ("0.1" if boosted else "0.4"), color=ROOT.kBlue)
#per.add(multijet, title='#tilde{N} #rightarrow tbs')
#per.add(dijet, title='#tilde{t} #rightarrow #bar{d}#bar{d}', color=ROOT.kBlue)
per.draw(canvas=ps.c)
ps.save('sigeff')

per2 = PerSignal('efficiency_Zprime', y_range=(1e-6,5.05))
per2.add(ZprimetoLLPto4j, title='Z\' #rightarrow XX #rightarrow 4j, m(X) = %s*m(Z\')' % ("0.1" if boosted else "0.4"))
per2.add(ZprimetoLLPto4b, title='Z\' #rightarrow XX #rightarrow 4b, m(X) = %s*m(Z\')' % ("0.1" if boosted else "0.4"), color=ROOT.kBlue)
per2.draw(canvas=ps.c)
ps.save('sigeff_Zprime')
