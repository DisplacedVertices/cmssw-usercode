#!/usr/bin/env python

import os
from itertools import combinations
from pprint import pprint
from FWCore.PythonUtilities.LumiList import LumiList
import JMTucker.Tools.Samples as Samples 
from JMTucker.Tools.CRAB3Tools import crab_command, crab_dirs_from_argv
from JMTucker.Tools.DBS import dasgo_ll_for_dataset as ll_for_dataset
import JMTucker.Tools.colors as colors

wds = crab_dirs_from_argv()

def ll2str(ll):
    return str(ll).replace('\n', ' ')

def check_and_print_diff(a,b):
    oa = eval(a)
    ob = eval(b)
    if oa.compactList != ob.compactList:
        print colors.red('%s != %s' % (a, b))
        print '  %s - %s:' % (a,b), ll2str(oa-ob)
        print '  %s - %s:' % (b,a), ll2str(ob-oa)
    else:
        print colors.green('%s == %s' % (a,b))

for wd in wds:
    print colors.bold(wd)
    sample = Samples.sample_from_end_string(Samples, wd)
    goodLumis = LumiList(sample.json)

    if any(not os.path.isfile(os.path.join(wd, 'results', x)) for x in 'inputDatasetLumis.json lumisToProcess.json outputDatasetsLumis.json processedLumis.json'.split()):
        print 'running crab report'
        report = crab_command('report', dir=wd) 
        #pprint(report)
    else:
        print 'using already-made crab report jsons'

    inputDatasetLumisDBS_fn = os.path.join(wd, 'results/inputDatasetLumisDBS.json')
    if not os.path.isfile(inputDatasetLumisDBS_fn):
        print 'getting LL from DBS for %s' % sample.dataset
        inputDatasetLumisDBS = ll_for_dataset(sample.dataset)
        inputDatasetLumisDBS.writeJSON(inputDatasetLumisDBS_fn)
    else:
        print 'using already-made LL from DBS'
        inputDatasetLumisDBS = LumiList(inputDatasetLumisDBS_fn)
  
    inputDatasetLumis = LumiList(os.path.join(wd, 'results/inputDatasetLumis.json'))

    goodInputDatasetLumis    = goodLumis & inputDatasetLumis
    goodInputDatasetLumisDBS = goodLumis & inputDatasetLumisDBS

    check_and_print_diff('goodInputDatasetLumis', 'goodInputDatasetLumisDBS')

    lumisToProcess = LumiList(os.path.join(wd, 'results/lumisToProcess.json'))
    processedLumis = LumiList(os.path.join(wd, 'results/processedLumis.json'))

    check_and_print_diff('goodInputDatasetLumis', 'lumisToProcess')
    check_and_print_diff('lumisToProcess', 'processedLumis')

    print

if len(wds) > 1:
    print colors.bold('check overlaps')
    overlaps = False
    for wda,wdb in combinations(wds, 2):
        lla = LumiList(os.path.join(wda, 'results/processedLumis.json'))
        llb = LumiList(os.path.join(wdb, 'results/processedLumis.json'))
        llaandb = lla & llb
        if llaandb:
            overlaps = True
            print colors.red('A = %s and B = %s have overlap:' % (wda, wdb)), ll2str(llaandb)
    if not overlaps:
        print colors.green('none!')

