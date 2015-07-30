#!/usr/bin/env python

import imp
import os
import sys
from pprint import pprint

fn = sys.argv[1]
name = os.path.basename(fn).replace('.py', '')

module = imp.load_module(name, open(fn), fn, ('.py', 'r', imp.PY_SOURCE))
process = module.process

process_keys = set(x for x in dir(process) if not (x.startswith('__') and x.endswith('__')))  #process.__dict__.keys()

' name source'

easy = 'aliases analyzers endpaths es_prefers es_producers es_sources filters outputModules paths producers psets sequences services vpsets'.split()

for n in easy:
    print n.ljust(15),
    o = eval('sorted(process.%s.keys())' % n)
    exec '%s = o' % n
    print 'sub?', process_keys.issuperset(o)
    process_keys -= set(o)

assert \
    process.looper is None and \
    not process._Process__modifiers and \
    not process._Process__partialschedules and \
    process.schedule is None and \
    process.subProcess is None

left = sorted(process_keys)
should_be = ['PoolSource', '_Process__InExtendCall', '_Process__aliases', '_Process__analyzers', '_Process__endpaths', '_Process__esprefers', '_Process__esproducers', '_Process__essources', '_Process__filters', '_Process__findFirstSequenceUsingModule', '_Process__isStrict', '_Process__looper', '_Process__modifiers', '_Process__name', '_Process__outputmodules', '_Process__partialschedules', '_Process__paths', '_Process__producers', '_Process__psets', '_Process__schedule', '_Process__sequences', '_Process__services', '_Process__setObjectLabel', '_Process__source', '_Process__subProcess', '_Process__vpsets', '_cloneToObjectDict', '_dumpConfigESPrefers', '_dumpConfigNamedList', '_dumpConfigOptionallyNamedList', '_dumpConfigUnnamedList', '_dumpPython', '_dumpPythonList', '_findPreferred', '_insertInto', '_insertManyInto', '_insertOneInto', '_insertPaths', '_okToPlace', '_place', '_placeAlias', '_placeAnalyzer', '_placeESPrefer', '_placeESProducer', '_placeESSource', '_placeEndPath', '_placeFilter', '_placeLooper', '_placeOutputModule', '_placePSet', '_placePath', '_placeProducer', '_placeSequence', '_placeService', '_placeSource', '_placeSubProcess', '_placeVPSet', '_pruneModules', '_replaceInSequences', '_sequencesInDependencyOrder', '_validateSequence', 'add_', 'aliases', 'aliases_', 'analyzerNames', 'analyzers', 'analyzers_', 'dumpConfig', 'dumpPython', 'endpaths', 'endpaths_', 'es_prefers', 'es_prefers_', 'es_producers', 'es_producers_', 'es_sources', 'es_sources_', 'extend', 'fillProcessDesc', 'filterNames', 'filters', 'filters_', 'globalReplace', 'load', 'looper', 'looper_', 'name_', 'outputModules', 'outputModules_', 'pathNames', 'paths', 'paths_', 'prefer', 'process', 'producerNames', 'producers', 'producers_', 'prune', 'psets', 'psets_', 'schedule', 'schedule_', 'sequences', 'sequences_', 'services', 'services_', 'setLooper_', 'setName_', 'setPartialSchedule_', 'setSchedule_', 'setSource_', 'setStrict', 'setSubProcess_', 'source', 'source_', 'subProcess', 'subProcess_', 'validate', 'vpsets', 'vpsets_']
assert left == should_be

####

print 'name:', process.name_()
for n in easy:
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\nXXX %s:' % n
    for k in eval(n):
        print k
        o = getattr(process, k)
        if n in ('endpaths', 'paths', 'sequences'):
            pprint(repr(o).split('+'))
        else:
            print o.dumpPython()
        print '========================================================='
    print
