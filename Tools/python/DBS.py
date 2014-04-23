#!/usr/bin/env python

import os

# Could use DBSAPI, but easier to just use popen.

class dbs_query:
    def __init__(self, ana01=False, ana02=False, ana03=False):
        self.ana01 = ana01
        self.ana02 = ana02
        self.ana03 = ana03
        self.extra = 'instance=prod/phys01' if (ana01 or ana02 or ana03) else ''
        if ana02:
            self.extra = self.extra.replace('01', '02')
        if ana03:
            self.extra = self.extra.replace('01', '03')
        self.cmd = "das_client.py --limit=0 --query '%s %%s'" % self.extra
        
    def __call__(self, query, line_filter=lambda s: True, line_xform=lambda s: s):
        full_cmd = self.cmd % query
        cmdout = os.popen(full_cmd).readlines()
        ret = []
        for line in cmdout:
            line = line.strip()
            if line_filter(line):
                x = line_xform(line)
                if x is not None:
                    ret.append(x)
        if not ret:
            raise RuntimeError('query %r (ana01: %s ana02: %s ana03: %s) did not succeed. full dbs command:\n%s\ndbs command output:\n%s' % (query, self.ana01, self.ana02, self.ana03, full_cmd, ''.join(cmdout) if cmdout else cmdout))
        return ret

def files_in_dataset(dataset, ana01=False, ana02=False, ana03=False):
    return dbs_query(ana01, ana02, ana03)('dataset=%s file' % dataset,
                                          lambda s: s.endswith('.root'))

def numevents_in_dataset(dataset, ana01=False, ana02=False, ana03=False):
    def xform(line):
        try:
            return int(line)
        except ValueError:
            return None
    return dbs_query(ana01, ana02, ana03)('dataset=%s | grep dataset.nevents' % dataset,
                                          line_xform=xform)[0]

def files_numevents_in_dataset(dataset, ana01=False, ana02=False, ana03=False):
    def xform(line):
        line = line.split()
        if not len(line) == 2 or not line[0].endswith('.root'):
            return None
        try:
            return line[0], int(line[1])
        except ValueError:
            return None
    return dbs_query(ana01, ana02, ana03)('dataset=%s file | grep file.name,file.nevents' % dataset,
                                          line_xform=xform)

def sites_for_dataset(dataset, ana01=False, ana02=False, ana03=False):
    return dbs_query(ana01, ana02, ana03)('dataset=%s site' % dataset,
                                          line_filter=lambda s: s.startswith('T'))

