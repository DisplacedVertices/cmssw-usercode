# this file for stuff that depends on the cmssw version, like globaltag

import os

year = open('year.txt').read().strip()

cmssw_version = os.environ['CMSSW_VERSION'].replace('patch', '').replace('pre', '-')
cmssw_version = tuple(int(x) for x in cmssw_version.split('_')[1:])
if cmssw_version[:2] not in [(9,3),(9,4)]:
    raise ValueError('unsupported cmssw version')

if cmssw_version[:2] == (9,3):
    globaltag = '93X_mc2017_realistic_v3'
    globaltag_miniaod = None
elif cmssw_version[:2] == (9,4):
    globaltag = '94X_mc2017_realistic_v11'
    globaltag_miniaod = '94X_mc2017_realistic_v14'
