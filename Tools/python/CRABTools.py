#!/usr/bin/env python

# author: J. Tucker

import glob, os, re, subprocess, sys, time, getpass
import xml.etree.cElementTree
from collections import defaultdict
from ConfigParser import ConfigParser, NoOptionError
from JMTucker.Tools.hadd import hadd

username = getpass.getuser()
mycrab_tmp_dir = '/tmp/%s/mycrab' % username
os.system('mkdir -p %s' % mycrab_tmp_dir)

if os.path.exists('/uscms_data'):
    crab_working_dir_default_root = '/uscms_data/d2/%s/crab_dirs' % username
else:
    print 'warning: not using crab_working_dir_default_root!'
    crab_working_dir_default_root = None

def bool_from_argv(s, remove=True, return_pos=False):
    val = s in sys.argv
    ret = val
    if val and return_pos:
        ret = val, sys.argv.index(s) 
    if val and remove:
        sys.argv.remove(s)
    return ret

def confirm_cmd(cmd, always=False):
    ret = []
    cmds = cmd.split('\n') if '\n' in cmd else [cmd]
    for cmd in cmds:
        if cmd != '' and not cmd.startswith('#'):
            print cmd
            if always or 'doit' in sys.argv:
                ret.append(os.system(cmd))
    if len(ret) == 1:
        ret = ret[0]
    return ret

def print_run_cmd(cmd, _print=True):
    if _print:
        print cmd
    os.system(cmd)

def crab_popen(cmd, return_exit_code=False, print_output=False, no_ssh_control_persist=True):
    if no_ssh_control_persist and 'crab ' in cmd:
        cmd = cmd.replace('crab ', 'crab -USER.ssh_control_persist=no ')
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    output = []
    for line in child.stdout:
        if print_output:
            print line,
        output.append(line)
    output = ''.join(output)
    if return_exit_code:
        return output, child.returncode
    else:
        return output

def crabify_list(l, simple=True):
    if simple:
        return ','.join(str(x) for x in sorted(l))

    a = b = None
    s = []
    def sforab(a,b):
        if a == b:
            return str(a)
        else:
            return '%i-%i' % (a,b)
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
    return ','.join(s)

def decrabify_list(s):
    if s.lower() == 'all':
        raise CrabError('warning: decrabify_list does not support "all"')
    s = s.split(',')
    l = []
    for x in s:
        if '-' in x:
            y,z = x.split('-')
            l += range(int(y), int(z)+1)
        else:
            l.append(int(x))
    return l

def crab_jobs_from_argv():
    jobs = []
    for x in sys.argv:
        was_list = False
        try:
            l = decrabify_list(x)
            if l:
                jobs += l
                was_list = True
        except ValueError:
            pass
        if not was_list:
            try:
                j = int(x)
                jobs.append(j)
            except ValueError:
                pass
    jobs.sort()
    return jobs

def is_crab_working_dir(path):
    return os.path.isdir(path) and os.path.isdir(os.path.join(path, 'job'))

def crab_working_dirs(path=''):
    return [d for d in glob.glob(os.path.join(path, 'crab_*')) if is_crab_working_dir(d)]
    
def last_crab_working_dir(path=''):
    dirs = [(d, os.stat(d).st_mtime) for d in crab_working_dirs(path)]
    if dirs:
        dirs.sort(key=lambda x: x[1])
        return dirs[-1][0]

def crab_move_working_dirs(dirs=None, dest_dir=None):
    if dirs is None:
        dirs = crab_working_dirs()

    if dest_dir is None:
        dest_dir = crab_working_dir_default_root

    if dest_dir is None:
        print 'warning: dest_dir is None in crab_move_working_dirs(), giving up'
        return

    if not os.path.isdir(dest_dir):
        print 'making crab working dir root at', dest_dir
        os.mkdir(dest_dir) # let it throw if it didn't work

    for d in crab_working_dirs():
        # if the dir is a link, then don't try to move it.
        try:
            os.readlink(d)
        except OSError:
            print_run_cmd('mv %s %s && ln -s %s' % (d, dest_dir, os.path.join(dest_dir, d)))

def crab_dirs_from_argv():
    dirs = []

    if 'all' in sys.argv:
        dirs = crab_working_dirs()
    elif 'except' in sys.argv:
        dirs = [d for d in crab_working_dirs() if d not in sys.argv]
    elif len(sys.argv) > 1:
        dirs = [d for d in sys.argv[1:] if is_crab_working_dir(d)]

    if not dirs:
        dirs = [last_crab_working_dir()]

    # make sure each entry is in only once, but can't use
    # list(set(dirs)) because we want to keep the sorted order
    r = []
    for d in dirs:
        if d not in r and d is not None:
            r.append(d)
        
    return r

def crab_dir_from_argv():
    dir = crab_dirs_from_argv()
    if len(dir) != 1:
        raise CrabError('exactly one directory in argv expected')
    return dir[0]

class CrabError(Exception):
    pass

def crab_cleanup(extra=[]):
    to_remove = [] #['crab.history', 'SiteDBusername.conf', 'server_legnaro.conf'] + extra #+['glite_wms_CERN.conf', 'glite.conf.CMS_CERN']
    for f in to_remove:
        if os.path.isfile(f):
            os.remove(f)

def crab_report(working_dir):
    print_run_cmd('crab -c %s -report' % working_dir)

def crab_is_using_server(working_dir=None, cfg=None):
    if working_dir is None and cfg is None:
        raise ValueError('need one of working_dir or cfg to be provided')
    if working_dir is not None:
        cfg = crab_cfg_parser(working_dir)
    try:
        return cfg.get('CRAB', 'use_server') == '1'
    except NoOptionError:
        return False

def crab_status(working_dir, verbose=True, debug=False):
    d = defaultdict(list)
    
    cmd = 'crab -c %s -status' % working_dir
    if verbose: print cmd

    cfg = crab_cfg_parser(working_dir)
    use_server = crab_is_using_server(cfg=cfg)
    if cfg.get('CRAB', 'scheduler') in ['glite']:
        if verbose:
            if use_server:
                print '(via grid with server so this may take a little time)'
            else:
                print '(via grid so this may take some time)'

    s = crab_popen(cmd, print_output=debug) if True else open('crab_status_test').read()
    #open('crab_status_test','wt').write(s); sys.exit(1)
    
    if 'Total Jobs' not in s:
        raise CrabError, 'unable to get status for working_dir=' + working_dir

    for x in s.split('\n'):
        # hurr should redo this with regexps, then not have to use these hacks
        x = x.replace('Cancelled by user', 'CancelledByUser')
        x = [y.strip() for y in x.split() if y.strip()]
        #print len(x), x
        if len(x) < 4: continue

        try:
            x[0] = int(x[0])
        except ValueError:
            pass
        else:
            id, end, status, action = x[:4]
            #print 'id', id, 'end', end, 'status', status, 'action', action
            if end == 'N' and use_server:
                status += 'NotEnd'

            if len(x) == 7:
                #print 'len(x) == 7'
                exe_exit_code = int(x[4])
                job_exit_code = int(x[5])
                e_host = x[6]
                #print 'host', e_host, 'exe_exit_code', exe_exit_code, 'job_exit_code', job_exit_code
            elif len(x) == 6:
                exe_exit_code = -1
                job_exit_code = int(x[4])
                e_host = x[5]
            elif len(x) == 5:
                exe_exit_code = job_exit_code = -1
                e_host = x[4]
            elif len(x) == 4:
                exe_exit_code = job_exit_code = -1
            else:
                raise ValueError('trouble parsing job line: repr(x) = %s' % repr(x))

            # I guess "Cleared" means Retrieved and no longer available to get the output? jesus who cares
            if status == 'Cleared':
                status = 'Retrieved'

            # crab server sometimes gets jobs done fine but get weird and have code 50117
            # https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCrabFaq?redirectedfrom=CMS.SWGuideCrabFaq#Exit_code_50117_when_using_crabs
            # user should resubmit; call it Retrieved so that upstream (e.g. crmon) will see that it should be resubmitted since it's not Retrieved_0_0
            # I also see a similar problem with code 1 and 50700...
            if use_server and status == 'Done' and job_exit_code == exe_exit_code and exe_exit_code in (1, 50117, 50700):
                status = 'Retrieved'

            if status == 'Retrieved':
                key = '%s_%i_%i' % (status, exe_exit_code, job_exit_code)
            else:
                key = status
            d[key].append(id)

    if verbose:
        for k in sorted(d.keys()):
            print '%s: %s' % (k.ljust(25), crabify_list(d[k], simple=False))
            
    return d

def crab_get_output(working_dir, l=None, n=500, verbose=True, debug=False):
    missing = set()
    job_re = re.compile(r'Results of Jobs # (\d+) are in')
    if l is None:
        l = crab_status(working_dir)['Done']
    if l:
        for i in xrange(0, len(l), n):
            ll = l[i:i+n]
            cmd = 'crab -c %s -getoutput %s' % (working_dir, crabify_list(ll))
            if verbose:
                print cmd
            s = crab_popen(cmd, print_output=debug)
            ll_success = set()
            for line in s.split('\n'):
                mo = job_re.search(line)
                if mo:
                    j = int(mo.group(1))
                    assert j not in ll_success
                    ll_success.add(j)
            ll = set(ll)
            assert ll_success.issubset(ll)
            this_missing = ll - ll_success
            assert not missing & this_missing
            missing.update(this_missing)
        if missing:
            print '\033[36;7m warning: \033[m crab_get_output for %s could not get output for %i/%i jobs: %s' % (working_dir, len(missing), len(l), crabify_list(sorted(missing)))
    return sorted(missing)

def crab_create_submit(cfg, jobs):
    print_run_cmd('crab -cfg %s -create -submit %s' % (cfg, jobs))

def crab_kill(working_dir, jobs):
    cmd = 'crab -c %s -kill %s' % (working_dir, crabify_list(jobs))
    print cmd
    output = crab_popen(cmd)
    open(os.path.join(mycrab_tmp_dir, 'debug_crab_kill_%s' % os.path.basename(working_dir)), 'wt').write(output)
    
def crab_resubmit(working_dir, jobs, site_control=''):
    jobs_re = re.compile(r'crab:  Jobs (\[.*\]) will be resubmitted')
    total_re = re.compile(r'crab:  Total of (\d+) jobs submitted.')

    if site_control and not site_control.startswith('-GRID.'):
        site_control = '-GRID.' + site_control

    cmd = 'crab -c %s %s -resubmit %s' % (working_dir, site_control, crabify_list(jobs))
    print cmd
    output = crab_popen(cmd)
    open(os.path.join(mycrab_tmp_dir, 'debug_crab_resubmit_%s' % os.path.basename(working_dir)), 'wt').write(output)

    success = []
    for line in output.split('\n'):
        mo = jobs_re.search(line)
        if mo is not None:
            l = eval(mo.group(1))
            overlap = sorted(set(success) & set(l))
            if overlap:
                print '\033[36;7m warning: \033[m crab_resubmit for %s encountered success jobs twice: %s' % (working_dir, crabify_list(overlap))
            success.extend(l)

    for line in output.split('\n'):
        mo = total_re.search(line)
        if mo is not None:
            n = int(mo.group(1))
            if n != len(jobs):
                print '\033[36;7m warning: \033[m crab_resubmit for %s wanted to resubmit %i jobs, but crab reports only %i jobs resubmitted' % (working_dir, len(jobs), n)
            if n != len(success):
                print '\033[36;7m warning: \033[m crab_resubmit for %s claimed to resubmit %i jobs but we only found %i in the lists it printed' % (n, len(success))
            break

def crab_cfg_parser(working_dir):
    c = ConfigParser()
    c.read(os.path.join(working_dir, 'share/crab.cfg'))
    return c

def crab_get_outfiles(working_dir):
    for line in open(os.path.join(working_dir, 'job/CMSSW.sh')):
        if line.startswith('file_list'):
            line = line.split('"')[-2]
            line = line.replace('$SOFTWARE_DIR/', '')
            line = line.replace('$NJob', '%i')
            return line.split(',')
    
def crab_get_njobs(working_dir):
    log = open(os.path.join(working_dir, 'log/crab.log')).read()
    sub = 'Total of '
    try:
        ndx = log.index(sub)
    except IndexError:
        raise RuntimeError, 'could not get total # of jobs from crab.log!'
    return int(log[ndx+len(sub):].split(' ', 1)[0])

def crab_get_output_dir(working_dir):
    c = crab_cfg_parser(working_dir)
    try:
        cast_dir = c.get('USER', 'storage_path').split('=')[-1] + c.get('USER', 'user_remote_dir').split('=')[-1]
        cast_dir = cast_dir.replace('//','/')
    except NoOptionError:
        cast_dir = None
    return cast_dir

def crab_get_condor_clusters(working_dir, cluster_re=re.compile(r'\((\d+)\.')):
    clusters = set()
    for fn in glob.glob(os.path.join(working_dir, 'share/.condor_temp/CMSSW_*.log')):
        for line in open(fn):
            mo = cluster_re.search(line)
            if mo:
                clusters.add(int(mo.group(1)))
    return sorted(clusters)

def crab_get_output_files(working_dir, _re=re.compile(r'\$SOFTWARE_DIR/(.*?)[,"]')):
    c = crab_cfg_parser(working_dir)

    # Get file list from cfg file, if it's there (we may have let crab
    # determine the output files for us from TFileService and
    # PoolOutputModule, in which case the line won't be in the cfg
    # file.
    files = set()
    try:
        for x in c.get('CMSSW', 'output_file').split(','):
            x = x.strip()
            if x:
                files.add(x.replace('.','_%i.'))
    except NoOptionError:
        pass

    # Find any files that weren't in the cfg file by parsing the
    # script (this is fragile!).
    for line in open(os.path.join(working_dir, 'job/CMSSW.sh')):
        if 'file_list' in line:
            break
    for x in _re.findall(line):
        files.add(x.replace('$NJob', '%i'))
        
    return list(sorted(files))
    
def crab_check_output(working_dir, verbose=True, debug=False, resub_any=False, resub_stuck_done=False, resub_none=False, site_control=''):
    d = crab_status(working_dir, verbose, debug)
    use_server = crab_is_using_server(working_dir)

    to_kill = []
    to_resub = []
    
    if d.has_key('Aborted'): # If use_server mode, and the jobs are in end status, this is OK -- else the key will be AbortedNotEnd and we shouldn't touch them.
        to_resub.extend(d['Aborted'])

    if d.has_key('Cancelled'):
        to_kill.extend(d['Cancelled'])
        to_resub.extend(d['Cancelled'])
        
    if resub_any:
        for k in d.keys():
            if 'Retrieved' in k and not k.endswith('0_0'):
                to_resub.extend(d[k])
            
    for code in []: # to be recommissioned
        if type(code) != type(()):
            code = str(code)
            code = code, code
        key = 'Retrieved_%s' % '_'.join(code)
        if d.has_key(key):
            to_resub.extend(d[key])

    if d.has_key('Done'):
        missing = crab_get_output(working_dir, d['Done'], debug=debug)
        if missing:
            for m in missing:
                d['Done'].remove(m)
            d['DoneStuck'] = missing
            if resub_stuck_done:
                to_resub.extend(missing)

    if to_kill:
        crab_kill(working_dir, to_kill)

    if not resub_none and to_resub:
        uniq = 'crabcheckoutputat%i' % time.time()
        for job in to_resub:
            crab_cleanup_aborted_job(working_dir, job, uniq)
        crab_resubmit(working_dir, to_resub, site_control)

    return d

def crab_status_dict(dirs=None):
    if dirs is None:
        dirs = crab_dirs_from_argv()
    results = {}
    for d in dirs:
        results[d] = crab_status(d)
    return results

def crab_arguments_xml(path, jobs_into_dicts=True):
    if os.path.isdir(path):
        filename = os.path.join(path, 'share/arguments.xml')
    else:
        filename = path
    ret = []
    for event, elem in xml.etree.cElementTree.iterparse(filename):
        if elem.tag == 'Job':
            if jobs_into_dicts:
                ret.append(dict(elem.items()))
            else:
                ret.append(elem.items()[:])
        elif elem.tag in ['arguments']:
            pass
        else:
            raise ValueError('tag %s not handled' % elem.tag)
    return dict((int(j['JobID']), j) for j in ret)

def crab_lumis_from_arguments_xml(working_dir, job_filter=None, by_job=False):
    from condor import parse_good_lumis
    args = crab_arguments_xml(working_dir)
    jobs = args.values()
    lumis = defaultdict(list)
    lumis_by_job = {}
    for job in jobs:
        if job_filter is not None and job['JobID'] != job_filter:
            continue
        these_lumis = job['Lumis'].split(',')
        parsed = parse_good_lumis(these_lumis)
        if by_job:
            lumis = defaultdict(list)
        for r,l in parsed.iteritems():
            lumis[r] += l
        if by_job:
            lumis_by_job[job['JobID']] = lumis
    return lumis_by_job if by_job else lumis

def crab_job_for_run_lumi(working_dir, run, lumi):
    lumis_by_job = crab_lumis_from_arguments_xml(working_dir, by_job=True)
    for job, lumis in lumis_by_job.iteritems():
        if lumis.has_key(run) and lumi in lumis[run]:
            return job
            
def crab_runs_from_arguments_xml(working_dir):
    return sorted(crab_lumis_from_arguments_xml(working_dir).keys())

def crab_get_output_files_for_job(working_dir, job):
    d = os.path.join(working_dir, 'res')
    # look for files like CMSSW_%(job)i.std*, crab_fjr_%(job)i.xml, out_files_%(job)i.tgz and output_%(job)i_%(try)i_%3(rand)s.root
    # should do this with regexp...
    files = []
    globs = ['CMSSW_%i.std*', 'Watchdog_%i.log.gz', 'crab_fjr_%i.xml', 'out_files_%i.tgz', '*_%i_*_???.root']
    for g in globs:
        files += glob.glob(os.path.join(d, g % job))
    return files
    
def crab_cleanup_aborted_job(working_dir, job, uniq=None, debug=False):
    files = crab_get_output_files_for_job(working_dir, job)
    if debug:
        print 'crab_cleanup_aborted_job for %s, job %i:' % (working_dir, job)
    if not files:
        if debug:
            print 'nothing to do!'
        return
    if debug:
        print 'files:', ' '.join(files)
    if uniq is None:
        uniq = 'job_%i_cleanup_%i' % (job, time.time())
    new_d = os.path.join(working_dir, 'res', uniq)
    print_run_cmd('mkdir -p %s' % new_d, debug)
    print_run_cmd('mv %s %s/' % (' '.join(files), new_d), debug)

def crab_get_input_files(working_dir, jobs=None):
    args = crab_arguments_xml(working_dir)
    if jobs is None:
        jobs = args.keys()
    return dict((j, args[j]['InputFiles'].split(',')) for j in jobs)

def crab_output_files_from_fjr(working_dir):
    fjrs = glob.glob(os.path.join(working_dir, 'res', 'crab_fjr*xml'))
    fjrs.sort(key = lambda x: int(x.split('_')[-1].split('.xml')[0]))
    files = []

    # Fragile xml parsing! Also assumes only one output file per job.
    wrapper_re = re.compile(r'<FrameworkError ExitStatus="(.+)" Type="WrapperExitCode"/>')
    exe_re = re.compile(r'<FrameworkError ExitStatus="(.+)" Type="ExeExitCode"/>')
    filename_re = re.compile(r'[ \t](/store/user.*root)')
    for fjr in fjrs:
        s = open(fjr).read()
        wrapper_mo = wrapper_re.search(s)
        exe_mo = exe_re.search(s)
        filename_mo = filename_re.search(s)
        if wrapper_mo is None or exe_mo is None or filename_mo is None:
            raise RuntimeError('cannot parse %s for exit codes and output filename (wrapper_mo %s exe_mo %s filename_mo %s)' % (fjr, wrapper_mo, exe_mo, filename_mo))
        if wrapper_mo.group(1) != '0' or exe_mo.group(1) != '0':
            raise RuntimeError('exit codes for %s not 0 (wrapper %s, exe %s)' % (fjr, wrapper_mo.group(1), exe_mo.group(1)))
        files.append(filename_mo.group(1))

    return files

def crab_hadd(working_dir, new_name=None, new_dir=None, raise_on_empty=True):
    if working_dir.endswith('/'):
        working_dir = working_dir[:-1]
    if new_name is None:
        new_name = os.path.basename(working_dir).replace('crab_','')
    if not new_name.endswith('.root'):
        new_name += '.root'
    if new_dir is not None:
        new_name = os.path.join(new_dir, new_name)
    print '%s: expecting %i files if all jobs succeeded' % (working_dir, crab_get_njobs(working_dir))
    files = glob.glob(os.path.join(working_dir, 'res/*root'))
    l = len(files)
    if l == 0:
        msg = 'crab_hadd: no files found in %s' % working_dir
        if raise_on_empty:
            raise CrabError(msg)
        else:
            print msg
    elif l == 1:
        print working_dir, ': just one file found, copying'
        os.system('cp %s %s' % (files[0], new_name))
    else:
        hadd(new_name, files)
        
    return new_name

def crab_event_summary_from_stdout(working_dir, path=None):
    if path:
        #TrigReport     1   10      10000       4176       5824          0 p
        totals_re = re.compile(r'TrigReport +\d+ +\d+ +(\d+) +(\d+) +(\d+) +\d+ %s' % path)
    else:
        totals_re = re.compile(r'TrigReport Events total = (\d+) passed = (\d+) failed = (\d+)')
    res = {}
    for fn in glob.glob(os.path.join(working_dir, 'res/CMSSW_*.stdout')):
        job = int(os.path.basename(fn).split('_')[1].split('.')[0])
        for line in open(fn):
            mo = totals_re.search(line)
            if mo:
                res[job] = tuple(int(x) for x in mo.groups())
                break
        if not res.has_key(job):
            raise ValueError('totals not found in file %s' % fn)
    return res
    
if __name__ == '__main__':
    from pprint import pprint
    from mymisc import bool_from_argv
    from FWCore.PythonUtilities.LumiList import LumiList

    if bool_from_argv('-cleanUp'):
        print 'executing crab_cleanup()'
        crab_cleanup()

    elif bool_from_argv('-expectedLumis'):
        print 'writing out JSONs for expected lumis:'
        for d in crab_dirs_from_argv():
            print d
            ll = LumiList(runsAndLumis=crab_lumis_from_arguments_xml(d))
            ll.writeJSON(os.path.join(d, 'res/expectedLumis.json'))

    elif bool_from_argv('-condorClusters'):
        pprint([(d, crab_get_condor_clusters(d)) for d in crab_dirs_from_argv()])

    elif bool_from_argv('-matchCondorClusters'):
        # Get current clusters.
        clusters = defaultdict(list)
        for line in os.popen('condor_q -submitter %s' % username):
            line = line.split()
            if len(line) < 2 or line[1] != username:
                continue
            cluster, job = line[0].split('.')
            cluster, job = int(cluster), int(job)
            clusters[cluster].append(job)
        print 'current clusters:', sorted(clusters)

        dirs = [(d, crab_get_condor_clusters(d)) for d in crab_working_dirs()]
        print 'crab dirs in current directory and their clusters:'
        pprint(dirs)
        print '\nthese dirs have currently running clusters:'

        # Print sorting by most jobs to least.
        x = []
        for d, dclusters in dirs:
            cs = sorted(set(clusters.keys()).intersection(dclusters))
            if cs:
                x.append((d, cs, sum(len(clusters[c]) for c in cs)))
        x.sort(key=lambda x: x[-1], reverse=True)
        for d, cs, ltot in x:
            print d
            for c in cs:
                l = len(clusters[c])
                print '%6i: %i job%s' % (c, l, 's' if l > 1 else '')

    elif bool_from_argv('-inputFiles'):
        jobs = crab_jobs_from_argv()
        if jobs:
            dir = crab_dir_from_argv()
            x =crab_get_input_files(dir)
            import pdb
            for job, files in crab_get_input_files(dir).iteritems():
                if job in jobs:
                    for f in files:
                        print f
        else:
            for dir in crab_dirs_from_argv():
                print dir
                d = crab_get_input_files(dir)
                for k,v in d.iteritems():
                    print k
                    for f in v:
                        print f

    elif bool_from_argv('-outputFromFJR'):
        for dir in crab_dirs_from_argv():
            print dir
            for fn in crab_output_files_from_fjr(dir):
                print fn

    elif bool_from_argv('-arguments'):
        dir = crab_dir_from_argv()
        args = crab_arguments_xml(dir)
        for job in crab_jobs_from_argv():
            pprint(args[job])

    elif bool_from_argv('-reportDirs'):
        for dir in crab_dirs_from_argv():
            crab_report(dir)
