#!/usr/bin/env python

import os

# Could use DBSAPI, but easier to just use popoen.
    
def files_in_dataset(dataset, ana01=False, ana02=False):
    url = '--url https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_01_writer/servlet/DBSServlet' if (ana01 or ana02) else ''
    if ana02:
        url = url.replace('01', '02')
    cmd = 'dbs search %(url)s --query "find file where dataset=%(dataset)s"' % locals()
    cmdout = os.popen(cmd).readlines()
    ret = [y.strip('\n') for y in cmdout if '.root' in y]
    if not ret:
        raise RuntimeError('no files for %s (ana01: %s ana02: %s) found. dbs command output:\n' % (dataset, ana01, ana02) + ''.join(cmdout))
    return ret

def numevents_in_dataset(dataset, ana01=False, ana02=False):
    url = '--url https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_01_writer/servlet/DBSServlet' if (ana01 or ana02) else ''
    if ana02:
        url = url.replace('01', '02')
    cmd = 'dbs search %(url)s --query "find sum(file.numevents) where dataset=%(dataset)s"' % locals()
    cmdout = os.popen(cmd).readlines()
    ret = None
    for line in cmdout:
        try:
            ret = int(line)
        except ValueError:
            pass
    if ret is None:
        raise RuntimeError('not able to get numevents for %s. dbs command output:\n' % (dataset) + ''.join(cmdout))
    return ret
