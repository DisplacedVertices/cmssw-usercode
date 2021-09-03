#!/usr/bin/env python

import sys
print '''
First check that hltLSById in RecoLuminosity/LumiDB/python/dataDML.py
doesn't hang for run,ls =
199569,371, and if it does, patch as below (but line numbers will be
different, as this is for a different tag of RecoLuminosity/LumiDB.

Index: RecoLuminosity/LumiDB/python/dataDML.py
===================================================================
RCS file: /local/reps/CMSSW/CMSSW/RecoLuminosity/LumiDB/python/dataDML.py,v
retrieving revision 1.59
diff -u -r1.59 dataDML.py
--- RecoLuminosity/LumiDB/python/dataDML.py	12 Oct 2012 09:43:40 -0000	1.59
+++ RecoLuminosity/LumiDB/python/dataDML.py	11 Dec 2012 20:59:28 -0000
@@ -1375,6 +1375,8 @@
         while cursor.next():
             runnum=cursor.currentRow()['runnum'].data()
             cmslsnum=cursor.currentRow()['cmslsnum'].data()
+            if runnum == 199569 and cmslsnum > 371:
+                break
             prescaleblob=None
             hltcountblob=None
             hltacceptblob=None
'''
sys.exit(1)

import re, os, subprocess
from pprint import pprint
from collections import defaultdict
from FWCore.PythonUtilities.LumiList import LumiList
from RecoLuminosity.LumiDB import sessionManager, lumiCalcAPI, revisionDML
from DVCode.Tools.general import from_pickle, to_pickle

os.system('mkdir -p prescales_temp')

def popen(cmd):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]

ll = LumiList('prescales_temp/Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt')
ll_compact = ll.getCompactList()
runs = [int(i) for i in ll.getRuns()]
runs.sort()

def dump_lumibyls(runs):
    l = float(len(runs))
    for i,run in enumerate(runs):
        out_fn = 'prescales_temp/lumibyls/%i.csv' % run
        already = os.path.isfile(out_fn)
        print 'run %i (%i/%i)%s' % (run, i+1, l, ' (skipping since already dumped)' if already else '')
        if already:
            continue
        popen('lumiCalc2.py lumibyls -r %i -o %s' % (run, out_fn))

def parse_lumibyls(run):
    d = defaultdict(dict)
    for line in open('prescales_temp/lumibyls/%i.csv' % run):
        if 'Run' in line:
            continue
        x = line.strip().split(',')
        run = int(x[0].split(':')[0])
        ls = int(x[1].split(':')[0])
        delivered = float(x[5])
        recorded = float(x[6])
        d[run][ls] = recorded
    return d

def get_lumibylses(runs):
    fn = 'prescales_temp/lumibylses.gzpickle'
    if os.path.isfile(fn):
        return from_pickle(fn)

    d = {}
    for run in runs:
        d.update(parse_lumibyls(run))

    to_pickle(d, fn)
    return d

def lumi_context(action, runs_lumis):
    svc = sessionManager.sessionManager('frontier://LumiCalc/CMS_LUMI_PROD')
    session = svc.openSession(isReadOnly=True, cpp2sqltype=[('unsigned int','NUMBER(10)'),('unsigned long long','NUMBER(20)')])
    session.transaction().start(True)

    datatagid, datatagname = revisionDML.currentDataTag(session.nominalSchema())
    dataidmap = revisionDML.dataIdsByTagId(session.nominalSchema(), datatagid, runlist=runs_lumis.keys(), withcomment=False)
    assert dataidmap

    session.transaction().commit()

    if action == 'trgbyls':
        session.transaction().start(True)
        result = lumiCalcAPI.trgForIds(session.nominalSchema(), runs_lumis, dataidmap, trgbitname=None, trgbitnamepattern='*', withL1Count=False, withPrescale=True)
        session.transaction().commit()
    elif action == 'hltbyls':
        session.transaction().start(True)
        result = lumiCalcAPI.hltForIds(session.nominalSchema(), runs_lumis, dataidmap, hltpathname=None, hltpathpattern='*', withL1Pass=False, withHLTAccept=False)
        session.transaction().commit()
    elif action == 'hltmenu':
        session.transaction().start(True)
        result = lumiCalcAPI.hltpathsForRange(session.nominalSchema(), runs_lumis, hltpathname=None, hltpathpattern='*')
        session.transaction().commit()
    del session
    del svc

    return result

def get_menus(runs):
    fn = 'prescales_temp/menus.gzpickle'
    if os.path.isfile(fn):
        return from_pickle(fn)
            
    menus = defaultdict(set)
    for run in runs:
        menu = lumi_context('hltmenu', {run:None})[run]
        for hlt_path, l1_seed, l1_bit in menu:
            assert l1_bit == 'n/a' or l1_seed == l1_bit
        menu = tuple([(hlt_path, l1_seed) for hlt_path, l1_seed, l1_bit in menu])
        menus[menu].add(run)

    to_pickle(menus, fn)
    return menus

def collapse(l):
    l = list(l)
    l.sort()
    a = b = None
    s = []
    def sforab(a,b):
        return (a,b)
    for x in sorted(l):
        if a is None:
            a = x
            b = x
        elif x == b+1:
            b = x
        else:
            s.append(sforab(a,b))
            a = b = x
        #print a, b, s
    s.append(sforab(a,b))
    return s

def get_l1_prescales(runs):
    fn = 'prescales_temp/l1prescales.gzpickle'
    if os.path.isfile(fn):
        return from_pickle(fn)

    prescales = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
    l = len(runs)
    for i,run in enumerate(runs):
        print 'get_l1_prescales run %i (%i/%i)' % (run, i+1, l)
        res = lumi_context('trgbyls', {run:None})[run]
        for line in res:
            ls = line[0]
            for l1_name, duh, prescale in line[-1]:
                prescales[l1_name][prescale][run].add(ls)

    for l1_name, duh in prescales.iteritems():
        for prescale, duh2 in duh.iteritems():
            for run in duh2:
                duh2[run] = collapse(duh2[run])
            duh[prescale] = dict(duh2)
        prescales[l1_name] = dict(duh)
    prescales = dict(prescales)

    to_pickle(prescales, fn)
    return prescales

def get_hlt_prescales(runs):
    fn = 'prescales_temp/hltprescales.gzpickle'
    if os.path.isfile(fn):
        return from_pickle(fn)

    prescales = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
    l = len(runs)
    for i,run in enumerate(runs):
        print 'get_hlt_prescales run %i (%i/%i)' % (run, i+1, l)
        res = lumi_context('hltbyls', {run:None})[run]
        for line in res:
            ls = line[0]
            for hlt_name, prescale, duh, duh2 in line[-1]:
                prescales[hlt_name][prescale][run].add(ls)

    for hlt_name, duh in prescales.iteritems():
        for prescale, duh2 in duh.iteritems():
            for run in duh2:
                duh2[run] = collapse(duh2[run])
            duh[prescale] = dict(duh2)
        prescales[hlt_name] = dict(duh)
    prescales = dict(prescales)

    to_pickle(prescales, fn)
    return prescales
    
def step_em():
    for i in xrange(0, len(runs), 50):
        print i,i+50
        hlt_prescales = get_hlt_prescales(runs[i:i+50])
        os.system('mv prescales_temp/hltprescales.gzpickle prescales_temp/hltprescales.gzpickle.%i' % i)
        os.system('ls -l prescales_temp/hltprescales*')

#step_em()

def merge_prescale_dicts(dicts):
    prescales = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for i,d in enumerate(dicts):
        print i
        for name, duh in d.iteritems():
            for prescale, duh2 in duh.iteritems():
                for run in duh2:
                    prescales[name][prescale][run].extend(duh2[run])
    for name, duh in prescales.iteritems():
        for prescale, duh2 in duh.iteritems():
            duh[prescale] = dict(duh2)
        prescales[name] = dict(duh)
    prescales = dict(prescales)
    return prescales

#hlt_prescales = merge_prescale_dicts([from_pickle('prescales_temp/hltprescales.gzpickle.%i' % i) for i in [1,2,3,150,200,250,300,350,400,450]])
#to_pickle(hlt_prescales, 'prescales_temp/hltprescales.gzpickle')

def version_free_name(path, version_re = re.compile(r'_v(\d+)')):
    if '_' in path:
        path = version_re.sub('_v', path)
    return path

def collapse_versions(prescales):
    new_prescales = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for name, duh in prescales.iteritems():
        new_name = version_free_name(name)
        for prescale, duh2 in duh.iteritems():
            for run in duh2:
                new_prescales[new_name][prescale][run].extend(duh2[run])
    prescales = new_prescales

    for name, duh in prescales.iteritems():
        for prescale, duh2 in duh.iteritems():
            duh[prescale] = dict(duh2)
        prescales[name] = dict(duh)
    prescales = dict(prescales)
    return prescales

def get_hlt_prescales_collapsed(runs, hlt_prescales=None):
    fn = 'prescales_temp/hltprescales_collapsed.gzpickle'
    if os.path.isfile(fn):
        return from_pickle(fn)

    if hlt_prescales is None:
        hlt_prescales = get_hlt_prescales(runs)
    hlt_prescales_collapsed = collapse_versions(hlt_prescales)

    to_pickle(hlt_prescales_collapsed, fn)
    return hlt_prescales_collapsed
    
dump_lumibyls(runs)
lumibylses = get_lumibylses(runs)
menus = get_menus(runs)
l1_prescales = get_l1_prescales(runs)
hlt_prescales = get_hlt_prescales(runs)
hlt_prescales_collapsed = get_hlt_prescales_collapsed(runs, hlt_prescales)
print len(l1_prescales)
print len(hlt_prescales)
print len(hlt_prescales_collapsed)


def menu_for_run(run):
    for menu, runs in menus.iteritems():
        if run in runs:
            return menu

def collapse_menu():
    collapsed_menu = {}
    for menu in menus.iterkeys():
        for hlt_path, l1_seed in menu:
            hlt_path_no_version = version_free_name(hlt_path)
            if collapsed_menu.has_key(hlt_path_no_version):
                if l1_seed != collapsed_menu[hlt_path_no_version]:
                    print 'hlt path:', hlt_path
                    print 'l1 seed:'
                    print l1_seed
                    print 'other l1 seed:'
                    print collapsed_menu[hlt_path_no_version]
            else:
                collapsed_menu[hlt_path_no_version] = l1_seed
    return collapsed_menu

#collapsed_menu = collapse_menu()

def prescales_by_intlumi(input):
    result = defaultdict(lambda: defaultdict(int))
    couldnt_get = defaultdict(set)
    for path, prescales_by_runls in input.iteritems():
        for prescale, runls in prescales_by_runls.iteritems():
            for run, ls_ranges in runls.iteritems():
                for ls_a, ls_b in ls_ranges:
                    for ls in xrange(ls_a, ls_b+1):
                        try:
                            lumi = lumibylses[run][ls]
                        except KeyError:
                            if prescale != 0:
                                couldnt_get[(run,ls)].add((path,prescale))
                            lumi = 0
                        result[path][prescale] += lumi/1e9
    for path in result.iterkeys():
        result[path] = dict(result[path])
    result = dict(result)
    if couldnt_get:
        print 'prescales_by_intlumi: could not get lumi for these run/ls:'
        pprint(sorted(couldnt_get.keys()))
        #for runls in sorted(couldnt_get.keys()):
        #    print runls, sorted(couldnt_get[runls])
    return result

#l1_prescales_by_intlumi = prescales_by_intlumi(l1_prescales)
#hlt_prescales_by_intlumi = prescales_by_intlumi(hlt_prescales)

def l1_seed_for_hlt_path_in_run(hlt_path, run):
    for hlt, l1 in menu_for_run(run):
        if hlt_path == hlt:
            return l1
    raise ValueError('could not find l1 seed for hlt path %s in run %i' % (hlt_path, run))

def normalize(i, a, b):
    assert a <= b
    if i < a:
        i = a
    if i > b:
        i = b
    return i

def ranges_contained(run, r1, r2):
    runrange = [z for y in ll_compact[str(run)] for z in y]
    rra,rrb = min(runrange), max(runrange)
    
    r1a,r1b = r1
    r2a,r2b = r2

    assert r1a <= r1b
    assert r2a <= r2b

    r1a = normalize(r1a, rra, rrb)
    r2a = normalize(r2a, rra, rrb)
    r1b = normalize(r1b, rra, rrb)
    r2b = normalize(r2b, rra, rrb)
    
    return (r1a <= r2a and r1b >= r2b) or (r2a <= r1a and r2b >= r1b)
        
def l1_prescale_for_run_ls(l1_expr, the_run, the_ls_range):
    while '"' in l1_expr:
        l1_expr = l1_expr.replace('"', '')
    l1_expr = l1_expr.strip()

    # simple case
    if l1_prescales.has_key(l1_expr):
        for prescale, run_ls_ranges in l1_prescales[l1_expr].iteritems():
            for run, ls_ranges in run_ls_ranges.iteritems():
                if run != the_run:
                    continue
                for ls_range in ls_ranges:
                    if ranges_contained(run, ls_range, the_ls_range):
                        return prescale
    # or case:
    elif ' OR ' in l1_expr and ' AND ' not in l1_expr:
        l1_paths = l1_expr.split(' OR ')
        return 'OR',  tuple([l1_prescale_for_run_ls(l1_path, the_run, the_ls_range) for l1_path in l1_paths])
    # and case:
    elif ' AND ' in l1_expr and ' OR ' not in l1_expr:
        l1_paths = l1_expr.split(' AND ')
        return 'AND', tuple([l1_prescale_for_run_ls(l1_path, the_run, the_ls_range) for l1_path in l1_paths])
    # more complicated: vomit
    raise ValueError('could not find l1 prescale for expr %s in run %i and lsrange %s' % (l1_expr, the_run, the_ls_range))

def get_total_prescales(hlt_prescales):
    total = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    skip = ['HLT_TrackerCalibration_v3', 'DQM_FEDIntegrity_v11'] + ['ACoreOutput', 'ALCALUMIPIXELSOutput', 'ALCAP0Output', 'ALCAPHISYMOutput', 'AOutput', 'AlCa_LumiPixels_Random_v1', 'BOutput', 'CalibrationOutput', 'DQMOutput', 'DQM_FEDIntegrity_v10', 'DQM_FEDIntegrity_v8', 'DQM_FEDIntegrity_v9', 'DQM_HcalEmptyEvents_v1', 'DST_Physics_v4', 'DST_Physics_v5', 'EcalCalibrationOutput', 'ExpressOutput', 'HLTDQMOutput', 'HLTDQMResultsOutput', 'HLTMONOutput', 'HLT_DTCalibration_v2', 'HLT_DTErrors_v3', 'HLT_EcalCalibration_v3', 'HLT_HcalCalibration_v3', 'HLT_HcalUTCA_v1', 'HLT_LogMonitor_v2', 'HLT_LogMonitor_v3', 'HLT_LogMonitor_v4', 'HLT_Physics_Parked_v1', 'HLT_Physics_part1_v4', 'HLT_Physics_v4', 'HLT_Physics_v5', 'HLT_Random_v2', 'HLTriggerFinalPath', 'HLTriggerFirstPath', 'NanoDSTOutput', 'PhysicsDSTOutput', 'RPCMONOutput', 'TrackerCalibrationOutput']
    skipped = defaultdict(list)
    for hlt_path, prescales_by_runls in hlt_prescales.iteritems():
        if hlt_path in skip:
            continue
        
        for hlt_prescale, runls in prescales_by_runls.iteritems():
            for run, ls_ranges in runls.iteritems():
                try:
                    l1_seed = l1_seed_for_hlt_path_in_run(hlt_path, run)
                except ValueError:
                    skipped[hlt_path].append(run)
                    continue
                for ls_range in ls_ranges:
                    l1_prescale = l1_prescale_for_run_ls(l1_seed, run, ls_range)
                    total[hlt_path][(hlt_prescale, l1_prescale)][run].append(ls_range)

    for name, duh in total.iteritems():
        for prescale, duh2 in duh.iteritems():
            duh[prescale] = dict(duh2)
        total[name] = dict(duh)
    total = dict(total)

    if skipped:
        print 'warning: skipped these:'
        pprint(skipped)
    return total

total_prescales = get_total_prescales(hlt_prescales)
total_prescales_by_intlumi = prescales_by_intlumi(total_prescales)

total_prescales_collapsed = collapse_versions(total_prescales)
total_prescales_collapsed_by_intlumi = prescales_by_intlumi(total_prescales_collapsed)

for x in 'total_prescales total_prescales_by_intlumi total_prescales_collapsed total_prescales_collapsed_by_intlumi'.split():
    to_pickle(eval(x), 'prescales_temp/' + x + '.gzpickle')
