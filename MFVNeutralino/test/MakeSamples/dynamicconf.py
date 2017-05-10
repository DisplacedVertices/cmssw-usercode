# this file for stuff that depends on the cmssw version, like globaltag

import os

cmssw_version = tuple(int(x) for x in os.environ['CMSSW_VERSION'].split('_')[1:])
if cmssw_version[0] not in (7,8):
    raise ValueError('unsupported cmssw version')

if cmssw_version[0] == 8: 
    globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v6' 
else:
    globaltag = 'MCRUN2_71_V1::All'
