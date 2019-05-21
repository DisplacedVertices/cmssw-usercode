#!/usr/bin/env python

import os, re, sys, json, cPickle as pickle
from collections import defaultdict
from itertools import izip
from pprint import pprint
from FWCore.PythonUtilities.LumiList import LumiList
from JMTucker.Tools.general import popen

# could use DBSAPI or DASAPI or whatever, but I'm lazy

class das_query:
    def __init__(self, instance='global', json=False):
        if type(instance) == int:
            instance = 'phys0%i' % instance
        else:
            allowed = ['phys01', 'phys02', 'phys03', 'global']
            if instance not in allowed:
                raise ValueError('instance must be one of: %r' % allowed)
        self.instance = instance
        self.instance_cmd = 'instance=prod/%s' % self.instance
        self.cmd = "dasgoclient -query '%s'"
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
            return json.loads(''.join(cmdout))
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

def datasets(pattern, instance='global'):
    return das_query(instance)('dataset dataset=%s' % pattern)

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

def sites_for_dataset(dataset, instance='global', json=False):
    l = das_query(instance, json)('site dataset=%s' % dataset,
                                  line_filter=lambda s: s.startswith('T'))
    if json:
        r = []
        for x in l:
            assert sorted(x.keys()) == ['das', 'qhash', 'site']
            y = x['site']
            assert type(y) == list and len(y) == 1
            d = y[0]
            if all(d.has_key(k) for k in ['block_completion', 'dataset_fraction', 'kind', 'name', 'se', 'replica_fraction', 'block_fraction']):
                r.append(d)
        return r
    else:
        return sorted(set(l)) # dasgo gives same lines to you many times

def site_is_tape(site_json):
    return site_json['name'].endswith('_Buffer') or site_json['name'].endswith('_MSS')

def site_completions(site_json, as_float=False):
    z = [str(site_json[x]) for x in ('block_completion', 'block_fraction', 'dataset_fraction', 'replica_fraction')]
    if as_float:
        return [float(c.replace('%',''))/100. for c in z]
    else:
        return z

def site_completions_string(site_json):
    x = (site_json['name'],) + tuple(site_completions(site_json, True))
    return '%s (%.4f %.4f %.4f %.4f)' % x

def complete_at_site(site_json):
    return all(c == '100.00%' for c in site_completions(site_json))

def file_details_run_lumis(dataset, instance='global'):
    objs = das_query(instance, json=True)('file,run,lumi dataset=%s' % dataset)
    raw = defaultdict(lambda: defaultdict(list))
    for o in objs:
        assert type(o) == dict and set(o) == set([u'qhash', u'das', u'run', u'file', u'lumi'])
        files, runs, lumis = o['file'], o['run'], o['lumi']
        assert len(files) == len(runs) and len(runs) == len(lumis)
        for f,r,l in izip(files, runs, lumis):
            if f['name'] is None:
                assert r['run_number'] is None
                assert l['number'] is None
            else:
                assert type(f) == dict and f.keys() == ['name'] and type(f['name']) == unicode
                assert type(r) == dict and r.keys() == ['run_number'] and type(r['run_number']) == int
                assert type(l) == dict and l.keys() == ['number'] and type(l['number']) == list
                f,r,l = str(f['name']), r['run_number'], l['number']
                raw[f][r] += l

    ret = {}
    for k,d in raw.iteritems():
        d2 = {}
        for k2,l in d.iteritems():
            d2[k2] = sorted(l)
        ret[k] = d2
    return ret

def file_details_nevents(dataset, instance='global', check=False):
    raise NotImplementedError('update for dasgo needed')
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
    rl = defaultdict(list)
    for run_lumis in details.itervalues():
        for run, lumis in run_lumis.iteritems():
            rl[run].extend(lumis)
    return LumiList(runsAndLumis=rl)

def ll_for_dataset(dataset, instance='global'):
    return ll_from_file_details(file_details_run_lumis(dataset, instance))

def json_for_dataset(json_fn, dataset, instance='global'):
    ll_for_dataset(dataset, instance).writeJSON(json_fn)

def files_for_json(json_fn, dataset, instance='global'):
    json = LumiList(json_fn)
    files = set()
    for file, run_lumis in file_details_run_lumis(dataset, instance).iteritems():
        ll = LumiList(runsAndLumis=run_lumis)
        if json & ll:
            files.add(file)
    return sorted(files)

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
        ll = LumiList(runsAndLumis=run_lumis)
        for x in wanted_run_lumis:
            if ll.contains(*x):
                files.add(file)
    return sorted(files)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'll':
            dataset, outfn = sys.argv[2:4]
            ll_for_dataset(dataset).writeJSON(outfn)
        else:
            sys.exit('unrecognized cmd %s' % cmd)

    #ds = '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/AODSIM'
    #all_files = files_in_dataset(ds)
    #print len(all_files)
    #files = files_for_json('json.qcdht2000ext', ds)
    #print len(files)

    #print ll_for_dataset('duh')
    #from Samples import *
    #print files_for_events([(1,15324,51305214)], qcdht1000ext.dataset)
    #print files_for_events([(1,85331,33407210)], ttbar.dataset)

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
