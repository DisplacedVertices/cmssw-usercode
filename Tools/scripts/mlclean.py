#!/usr/bin/env python

import re

_replaceables = [
    (re.compile(r'\d\d-...-\d\d\d\d \d\d:\d\d:\d\d.* C[DE]?S?T'), 'DATETIME'),
    (re.compile(r'0x[0-9a-fA-F]+'), 'POINTER')
    ]

_event = re.compile(r'^Begin processing the (?P<record>\d+)th record\. Run (?P<run>\d+), Event (?P<event>\d+), LumiSection (?P<lumi>\d+)')
_event = re.compile(r'\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* Event (?P<event>\d+) \((?P<events_done>\d+)\)')

def clean_file(src, dest, out_limit=-1, events_only=[]):
    print 'cleaning MessageLogger crap out of %s, writing to %s' % (src, dest)
    
    destfile = open(dest, 'wt')

    out_cnt = 0
    skip_cnt = 0
    skip_chr = None

    curr = {
        'record': -1,
        'run': -1,
        'event': -1,
        'lumi': -1,
        'event_done': -1,
        }
    
    for line in open(src):
        matchobj = _event.search(line)
        if matchobj:
            #curr_record, curr_run, curr_event, curr_lumi = [int(matchobj.group(x)) for x in 'record', 'run', 'event', 'lumi']

            matchobj = matchobj.groupdict()
            for x in 'record', 'run', 'event', 'lumi', 'events_done':
                if matchobj.has_key(x):
                    curr[x] = int(matchobj[x])
                
            #print line,
            ##print 'record %i run %i event %i lumi %i' % (curr_record, curr_run, curr_event, curr_lumi)
            #print curr

        #if events_only and (curr_run, curr_event, curr_lumi) not in events_only:
        if events_only and curr['event'] not in events_only:
            continue
        
        if skip_cnt:
            skip_cnt -= 1
            continue
        if skip_chr is not None:
            if line.startswith(skip_chr):
                continue
            else:
                skip_chr = None

#        if 'FwkReport' in line:
#            skip_cnt = 2
#        elif 'RFIOFileDebug' in line:
#            skip_cnt = 2
#        elif line.startswith('    bytes read'):
#            skip_cnt = 2
#        elif 'PixelMatchGsfElectron' in line and 'CandViewShallowCloneCombiner' in line:
#            skip_cnt = 2
#        elif 'TrigReport' in line or 'TimeReport' in line or 'Storage statistics:' in line:
#            pass
#        elif line.startswith(' Dilepton # 1; dimu mass:  ---  ,  ---  ,  ---  ,  ---  ,  ---  ,  ---  ,  ---  ,  ---  ,  ---'):
#            skip_cnt = 1
#        elif 'At rec level' in line and 'CandCombiner made' in line:
#            pass
#        elif line.startswith('addBremCandidates, rec level'):
#            skip_chr = ' '
#        elif line.startswith('addTrueResonance:'):
#            skip_cnt = 2
#        elif 'Root_Information:' in line and 'TClass' in line:
#            skip_cnt = 2
#        elif line.startswith('TriggerTranslator, '):
#            skip_chr = '  '
#        elif line.startswith('compareTrigDecision:'):
#            skip_cnt = 7
# take out the if 0 if if you reenable these
        if 0:  
            pass
        else:
            for r, to in _replaceables:
                matchobj = r.search(line)
                if matchobj:
                    line = line.replace(matchobj.group(0), 'MLC_' + to)

            if out_limit < 0 or out_cnt < out_limit:
                destfile.write(line)
                out_cnt += 1
                if out_cnt == out_limit:
                    break

    print 'done.'

def main():
    import os, sys, tempfile
    from itertools import izip

    diff_mode = None
    if '-tk' in sys.argv:
        diff_mode = 'tkdiff'
    elif '-diff' in sys.argv:
        diff_mode = 'diff'

    no_clean = '-noclean' in sys.argv

    out_limit = -1
    events_only = []
    
    for arg in sys.argv:
        if arg.startswith('-l'):
            out_limit = int(arg.replace('-l',''))
        elif arg.startswith('-e'):
            obj = eval(arg.replace('-e',''))
            tobj = type(obj)
            if tobj == type(()) or tobj == type([]):
                events_only.extend(obj)
            else:
                events_only.append(obj)
    
    srcs = [x for x in sys.argv[1:] if not x.startswith('-')]

    if len(srcs) == 0:
        print 'usage: mldiff.py file1 [file2 file3 ... fileN] [-tk] [-diff] [-noclean] [-lNNN]'
        sys.exit(1)

    for src in srcs:
        ok = True
        if os.path.isfile(src):
            try:
                open(src)
            except IOError:
                ok = False
        if not ok:
            print '%s is not readable' % src
            sys.exit(1)

    suffix = '.mlclean'
    
    if diff_mode:
        if len(srcs) != 2:
            print 'error: %i filenames supplied but diff mode %s requested' % (len(srcs), diff_mode)
            sys.exit(1)

        tmp_dir = tempfile.gettempdir()
        dests = [os.path.join(tmp_dir, x.replace('/','_') + suffix) for x in srcs]
    else:
        dests = [x + suffix for x in srcs]

    print 'file movement is:'
    for pair in izip(srcs, dests):
        print '  %s -> %s' % pair
    if out_limit >= 0:
        print 'limiting output to %i lines' % out_limit
    if events_only:
        print 'only outputting events', events_only
    if diff_mode:
        print 'will do a %s on the two files' % diff_mode
        if no_clean:
            print 'will not clean up the output'

    for src, dest in izip(srcs, dests):
        clean_file(src, dest, out_limit, events_only)

    if diff_mode:
        cmd = '%s %s %s' % (diff_mode, dests[0], dests[1])
        print 'execute "%s"' % cmd
        os.system(cmd)

        if not no_clean:
            for dest in dests:
                print 'removing %s' % dest
                os.remove(dest)

if __name__ == '__main__':
    main()
