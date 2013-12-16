#!/usr/bin/env python

import os

# Could use DBSAPI, but easier to just use popoen.

class dbs_query:
    def __init__(self, ana01=False, ana02=False):
        self.ana01 = ana01
        self.ana02 = ana02
        self.url = '--url https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_01_writer/servlet/DBSServlet' if (ana01 or ana02) else ''
        if ana02:
            self.url = self.url.replace('01', '02')
        self.cmd = 'dbs search %s --query "%%s"' % self.url
        
    def __call__(self, query, line_filter, line_xform):
        cmdout = os.popen(self.cmd % query).readlines()
        ret = []
        for line in cmdout:
            line = line.strip()
            if line_filter(line):
                x = line_xform(line)
                if x is not None:
                    ret.append(x)
        if not ret:
            raise RuntimeError('query %r (ana01: %s ana02: %s) did not succeed. dbs command output:\n' % (query, self.ana01, self.ana02) + ''.join(cmdout))
        return ret

def files_in_dataset(dataset, ana01=False, ana02=False):
    return dbs_query(ana01, ana02)('find file where dataset=' + dataset,
                                   lambda s: s.endswith('.root'),
                                   lambda s: s)

def numevents_in_dataset(dataset, ana01=False, ana02=False):
    def xform(line):
        try:
            return int(line)
        except ValueError:
            return None
    return dbs_query(ana01, ana02)('find sum(file.numevents) where dataset=' + dataset,
                                   lambda s: True,
                                   xform)[0]

def files_numevents_in_dataset(dataset, ana01=False, ana02=False):
    def xform(line):
        line = line.split()
        if not len(line) == 2 or not line[0].endswith('.root'):
            return None
        try:
            return line[0], int(line[1])
        except ValueError:
            return None
    return dbs_query(ana01, ana02)('find file,file.numevents where dataset=' + dataset,
                                   lambda s: True,
                                   xform)

