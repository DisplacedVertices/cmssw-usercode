# this file for stuff that depends on the cmssw version, like globaltag

import os

year = open('year.txt').read().strip()
doing_2015 = year == '2015'

cmssw_version = os.environ['CMSSW_VERSION'].replace('patch', '').replace('pre', '-')
cmssw_version = tuple(int(x) for x in cmssw_version.split('_')[1:])
if cmssw_version[0] not in (7,8):
    raise ValueError('unsupported cmssw version')

if cmssw_version[0] == 8: 
    assert not doing_2015
    globaltag_gensim = '80X_mcRun2_asymptotic_2016_TrancheIV_v6' 
else:
    globaltag_gensim = 'MCRUN2_71_V1::All'

if doing_2015:
    globaltag = '76X_mcRun2_asymptotic_v12'
else:
    globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v6' 

