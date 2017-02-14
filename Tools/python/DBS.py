#!/usr/bin/env python

import os, re, sys, json, cPickle as pickle
from collections import defaultdict
from itertools import izip
from pprint import pprint
from FWCore.PythonUtilities.LumiList import LumiList
from JMTucker.Tools.general import popen

# could use DBSAPI or DASAPI or whatever, but I'm lazy

class das_query:
    json_keys_expected = ['apilist', 'ctime', 'data', 'incache', 'mongo_query', 'nresults', 'status', 'timestamp']

    def __init__(self, instance='global', json=False):
        if type(instance) == int:
            instance = 'phys0%i' % instance
        else:
            allowed = ['phys01', 'phys02', 'phys03', 'global']
            if instance not in allowed:
                raise ValueError('instance must be one of: %r' % allowed)
        self.instance = instance
        self.instance_cmd = 'instance=prod/%s' % self.instance
        self.cmd = "dasgoclient_linux -query '%s'"
        self.json = json
        if json:
            self.cmd = self.cmd.replace('-query', '-json -query')
        
    def __call__(self, query, line_filter=lambda s: True, line_xform=lambda s: s):
        full_cmd = self.cmd % query
        if self.instance != 'global':
            if '|' in query:
                full_cmd = full_cmd.replace('|', self.instance_cmd + ' |')
            else:
                assert self.cmd[-1] == "'"
                full_cmd = full_cmd[:-1] + ' ' + self.instance_cmd + "'"
        cmdout = os.popen(full_cmd).readlines()
        if self.json:
            json_obj = json.loads(cmdout[0])
            assert type(json_obj) == dict and sorted(json_obj.keys()) == das_query.json_keys_expected
            return json_obj
        else:
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
    return das_query(instance)('file dataset=%s' % dataset,
                               lambda s: s.endswith('.root'))

def numevents_in_file(fn, instance='global'):
    def xform(line):
        try:
            return int(float(line))
        except ValueError:
            return None
    return das_query(instance)('file=%s | grep file.nevents' % fn,
                               line_xform=xform)[0]

def numevents_in_dataset(dataset, instance='global'):
    def xform(line):
        try:
            return int(float(line))
        except ValueError:
            return None
    return das_query(instance)('dataset dataset=%s | grep dataset.nevents' % dataset,
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

def file_details_run_lumis(dataset, instance='global'):
    obj = das_query(instance, json=True)('file,run,lumi dataset=%s' % dataset)
    #obj = json.load(open('json_str'))
    raw = defaultdict(lambda: defaultdict(list))

    for o in obj['data']:
        assert type(o) == dict and sorted(o.keys()) == ['_id', 'cache_id', 'das', 'das_id', 'file', 'lumi', 'qhash', 'run']
        files, runs, lumis = o['file'], o['run'], o['lumi']
        assert len(files) == len(runs) and len(runs) == len(lumis)
        for f,r,l in izip(files, runs, lumis):
            assert type(f) == dict and f.keys() == ['name'] and type(f['name']) == unicode
            assert type(r) == dict and r.keys() == ['run_number'] and type(r['run_number']) == int
            assert type(l) == dict and l.keys() == ['number'] and type(l['number']) == list
            f,r,l = str(f['name']), r['run_number'], l['number']
            for x in l:
                assert len(x) == 2 and type(x[0]) == int and type(x[1]) == int
            raw[f][r] += l

    ret = {}
    for k,d in raw.iteritems():
        d2 = {}
        for k2,l in d.iteritems():
            d2[k2] = sorted(l)
        ret[k] = d2
    return ret

def file_details_nevents(dataset, instance='global', check=False):
    obj = das_query(instance, json=True)('file dataset=%s | grep file.name,file.nevents' % dataset)
    #obj = json.load(open('json_str2'))

    ret = {}
    for o in obj['data']:
        assert type(o) == dict and sorted(o.keys()) == ['_id', 'cache_id', 'das', 'das_id', 'file', 'qhash']
        o = sorted(o['file'])
        assert len(o) == 2 and sorted(o[1].keys()) == ['name', 'nevents'] and o[0].keys() == ['name']
        f, nevents = str(o[1]['name']), o[1]['nevents']
        assert f == o[0]['name'] and type(nevents) == int
        assert not ret.has_key(f)
        ret[f] = nevents

    if check:
        assert sum(ret.itervalues()) == int(das_query(instance)('dataset=%s | grep dataset.nevents' % dataset)[0])

    return ret

def ll_from_file_details(details):
    compact_list = defaultdict(list)
    for run_lumis in details.itervalues():
        for run, lumi_ranges in run_lumis.iteritems():
            compact_list[run].extend(lumi_ranges)
    return LumiList(compactList=compact_list)

def ll_for_dataset(dataset, instance='global'):
    return ll_from_file_details(file_details_run_lumis(dataset, instance))

def json_for_dataset(json_fn, dataset, instance='global'):
    ll_for_dataset(dataset, instance).writeJSON(json_fn)

def files_for_events(run_events, dataset, instance='global'):
    wanted_run_lumis = []
    for x in run_events: # list of runs, or list of (run, event), or list of (run, lumi, event)
        if type(x) == int:
            wanted_run_lumis.append((x, None))
        elif len(x) == 2:
            wanted_run_lumis.append((x[0], None))
        else:
            wanted_run_lumis.append(x[:2])

    files = set()
    for file, run_lumis in file_details_run_lumis(dataset, instance).iteritems():
        ll = LumiList(compactList=run_lumis)
        for x in wanted_run_lumis:
            if ll.contains(*x):
                files.add(file)
    return sorted(files)

#####

# these use dasgoclient

def dasgo_ll_for_dataset(dataset, instance='global', line_re = re.compile(r'^(/store.*root) (\d+) (\[.*\])$')):
    assert instance == 'global'
    d = defaultdict(set) 
    for line in popen('dasgoclient_linux -query "file,run,lumi dataset=%s"' % dataset).split('\n'):
        mo = line_re.match(line.strip())
        if mo:
            _, run, lumis = mo.groups()
            d[int(run)] |= set(eval(lumis))
    return LumiList(runsAndLumis=d)

def dasgo_json_for_dataset(json_fn, dataset, instance='global'):
    dasgo_ll_for_dataset(dataset, instance).writeJSON(json_fn)

if __name__ == '__main__':
    pass

    #print ll_for_dataset('duh')
    #print files_for_events([(272818, 519, 103103)], 'duh')

    #for name, dataset in [
    #    ('JetHT2016B1', '/JetHT/Run2016B-23Sep2016-v1/AOD'),
    #    ('JetHT2016B3', '/JetHT/Run2016B-23Sep2016-v3/AOD'),
    #    ('JetHT2016C', '/JetHT/Run2016C-23Sep2016-v1/AOD'),
    #    ('JetHT2016D', '/JetHT/Run2016D-23Sep2016-v1/AOD'),
    #    ('JetHT2016E', '/JetHT/Run2016E-23Sep2016-v1/AOD'),
    #    ('JetHT2016F', '/JetHT/Run2016F-23Sep2016-v1/AOD'),
    #    ('JetHT2016G', '/JetHT/Run2016G-23Sep2016-v1/AOD'),
    #    ('JetHT2016H1', '/JetHT/Run2016H-PromptReco-v1/AOD'),
    #    ('JetHT2016H2', '/JetHT/Run2016H-PromptReco-v2/AOD'),
    #    ('JetHT2016H3', '/JetHT/Run2016H-PromptReco-v3/AOD'),
    #    ]:
    #    print name
    #    x = file_details_run_lumis(dataset)
    #    open(name + '.neventsdict', 'wt').write(repr(file_details_nevents(dataset)))
    #    open(name + '.runlumisdict', 'wt').write(repr(x))
    #    ll_from_file_details(x).writeJSON(name + '.json')

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
