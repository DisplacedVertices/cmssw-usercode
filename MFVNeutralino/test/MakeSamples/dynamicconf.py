# things common to many pys that depend on the year/cmssw version

import os, inspect, FWCore.ParameterSet.Config as cms

if not os.path.isfile('year.txt'):
    from JMTucker.Tools.Year import year # this doesn't exist on remote jobs but this should get triggered when testing interactively first
    open('year.txt','wt').write('%s\n' % year)

year = int(open('year.txt').read().strip())
if year not in (2017, 2018):
    raise ValueError('bad year %s' % year)

cmssw_version = os.environ['CMSSW_VERSION'].replace('patch', '').replace('pre', '-')
cmssw_version = tuple(int(x) for x in cmssw_version.split('_')[1:])
if cmssw_version[:2] not in [(9,3),(9,4),(10,2)]:
    raise ValueError('unsupported cmssw version')

####

from Configuration.StandardSequences.Eras import eras

if year == 2017:
    era = eras.Run2_2017
elif year == 2018:
    era = eras.Run2_2018

mods = {x : (era,) for x in ('gensim','rawhlt','reco','miniaod')}

if year == 2017:
    mods['miniaod'] = (era, eras.run2_miniAOD_94XFall17)
if year == 2018:
    from Configuration.ProcessModifiers.premix_stage2_cff import premix_stage2
    mods['rawhlt'] = mods['reco'] = (era, premix_stage2)

def process(name):
    caller = inspect.stack()[1][1].replace('.py','')
    return cms.Process(name, *mods[caller])

####

if year == 2017:
    globaltag = {
        'gensim': '93X_mc2017_realistic_v3',
        'rawhlt': '94X_mc2017_realistic_v11',
        'reco': '94X_mc2017_realistic_v11',
        'miniaod': '94X_mc2017_realistic_v14',
        # ntuple globaltag value taken from CMSSWTools and dumped before submission
        }
elif year == 2018:
    globaltag = {
        'gensim': '102X_upgrade2018_realistic_v11',
        'rawhlt': '102X_upgrade2018_realistic_v15',
        'reco': '102X_upgrade2018_realistic_v15',
        'miniaod': '102X_upgrade2018_realistic_v15',
        }
