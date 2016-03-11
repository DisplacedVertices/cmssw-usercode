#!/usr/bin/env python

import os, sys, cPickle
from collections import defaultdict
from pprint import pprint
from FWCore.PythonUtilities.LumiList import LumiList

# Could use DBSAPI or DASAPI or whatever, but I'm too lazy to learn it.

class das_query:
    def __init__(self, instance='global', json=False):
        if type(instance) == int:
            instance = 'phys0%i' % instance
        else:
            allowed = ['phys01', 'phys02', 'phys03', 'global']
            if instance not in allowed:
                raise ValueError('instance must be one of: %r' % allowed)
        self.instance = instance
        self.extra = 'instance=prod/%s' % self.instance
        self.cmd = "das_client.py --limit=0 --query '%s %%s'" % self.extra
        self.json = json
        if json:
            self.cmd += ' --format=json'
        
    def __call__(self, query, line_filter=lambda s: True, line_xform=lambda s: s):
        full_cmd = self.cmd % query
        cmdout = os.popen(full_cmd).readlines()
        if self.json:
            return cmdout[0]
        ret = []
        for line in cmdout:
            line = line.strip()
            if line_filter(line):
                x = line_xform(line)
                if x is not None:
                    ret.append(x)
        if not ret:
            raise RuntimeError('query %r (instance: %s) did not succeed. full das command:\n%s\ndas command output:\n%s' % (query, self.instance, full_cmd, ''.join(cmdout) if cmdout else cmdout))
        return ret

def files_in_dataset(dataset, instance='global'):
    return das_query(instance)('dataset=%s file' % dataset,
                               lambda s: s.endswith('.root'))

def numevents_in_file(fn, instance='global'):
    def xform(line):
        try:
            return int(line)
        except ValueError:
            return None
    return das_query(instance)('file=%s | grep file.nevents' % fn,
                               line_xform=xform)[0]

def numevents_in_dataset(dataset, instance='global'):
    def xform(line):
        try:
            return int(line)
        except ValueError:
            return None
    return das_query(instance)('dataset=%s | grep dataset.nevents' % dataset,
                               line_xform=xform)[0]

def files_numevents_in_dataset(dataset, instance='global'):
    def xform(line):
        line = line.split()
        if not len(line) == 2 or not line[0].endswith('.root'):
            return None
        try:
            return line[0], int(line[1])
        except ValueError:
            return None
    return das_query(instance)('dataset=%s file | grep file.name,file.nevents' % dataset,
                               line_xform=xform)

def sites_for_dataset(dataset, instance='global'):
    return das_query(instance)('dataset=%s site' % dataset,
                               line_filter=lambda s: s.startswith('T'))

def _file_run_lumi_obj(dataset, instance='global'):
    json_str = das_query(instance, json=True)('file,run,lumi dataset=%s' % dataset)
    true = True # lol
    false = False
    #open('json_str','wt').write(json_str)
    #json_str = open('json_str2').read()
    obj = eval(json_str) # json.loads doesn't work...
    #pprint(obj)

    assert type(obj) == dict and sorted(obj.keys()) == ['apilist', 'ctime', 'data', 'incache', 'mongo_query', 'nresults', 'status', 'timestamp']
    obj = obj['data']
    return obj

def _file_from_json(x):
    file = x['file']
    assert len(file) == 1
    file = file[0]['name']
    assert file.startswith('/store')
    return file

def _run_lumis_from_json(x):
    lumis = x['lumi']
    assert len(lumis) == 1
    lumis = lumis[0]['number']
    assert type(lumis) == list
    for rng in lumis:
        assert type(rng) == list and len(rng) == 2
    run = x['run']
    assert len(run) == 1
    run = x['run'][0]['run_number']
    assert type(run) == int
    return run, lumis

def ll_for_dataset(dataset, instance='global'):
    obj = _file_run_lumi_obj(dataset, instance)
    compact_list = defaultdict(list)
    for x in obj:
        run, lumis = _run_lumis_from_json(x)
        compact_list[run].extend(lumis)

    return LumiList(compactList=compact_list)

def json_for_dataset(json_fn, dataset, instance='global'):
    ll_for_dataset(dataset, instance).writeJSON(json_fn)

def files_for_events(run_events, dataset, instance='global'):
    run_lumis = defaultdict(list)
    for x in run_events: # list of runs, or list of (run, event), or list of (run, lumi, event)
        if type(x) == int:
            run_lumis[x] = None
        elif len(x) == 2:
            run_lumis[x[0]] = None
        else:
            run_lumis[x[0]].append(x[1])

    files = []

    obj = _file_run_lumi_obj(dataset, instance)

    for x in obj:
        #assert len(x['run']) == len(x['lumi'])
        assert len(set(y['name'] for y in x['file'])) == 1

        keep = False
        class StopIt(Exception):
            pass

        try:
            for run_d in x['run']:
                run = run_d['run_number']
                allowed = run_lumis[run]
                if allowed is None:
                    keep = True
                    raise StopIt()

                for lumi_d in x['lumi']:
                    for lumi_lo, lumi_hi in lumi_d['number']:
                        for lumi in allowed:
                            if lumi >= lumi_lo and lumi <= lumi_hi:
                                keep = True
                                raise StopIt()
        except StopIt:
            pass

        if keep:
            files.append(str(x['file'][0]['name']))

    return files

if __name__ == '__main__':
    pass

    #execfile('events_to_debug.txt')
    #pprint(files_for_events(duh, 'fuh'))
    #pprint(files_for_events(duh, '/Cosmics/Commissioning2015-CosmicSP-CosmicsSP_07Feb2015-v2/RAW-RECO'))
    #from JMTucker.Tools.Samples import *
    #for s in data_samples[:5]:
    #    pprint(files_for_events(duh, s.dataset))

    ##obj = _file_run_lumi_obj('/JetHT/Run2015D-PromptReco-v4/AOD')
    ##cPickle.dump(obj, open('obj','wb'), -1)
    #obj = cPickle.load(open('obj','rb'))
    #d = []
    #for o in obj:
    #    file = _file_from_json(o)
    #    run, lumis = _run_lumis_from_json(o)
    #    d.append((LumiList(compactList={run: lumis}), file))
    #
    ##n = len(d)
    ##for ix in xrange(n):
    ##    print ix
    ##    for iy in xrange(ix+1, n):
    ##        assert not (d[ix][0] & d[iy][0])
    #
    #files = []
    #ll = LumiList('todo.leftaftercomplete2partial.json')
    #for r,l in ll.getLumis():
    #    found = False
    #    for tll, file in d:
    #        if tll.contains(r,l):
    #            #print r,l,file
    #            found = True
    #            files.append(file)
    #    if not found:
    #        print 'did not find for', r, l

                
