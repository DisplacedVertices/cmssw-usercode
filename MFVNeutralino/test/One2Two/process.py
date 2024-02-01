import os, sys, re
from glob import glob
from JMTucker.Tools import colors
from JMTucker.Tools.ROOTTools import ROOT, detree
from JMTucker.Tools.general import bool_from_argv
from JMTucker.Tools.hadd import hadd

def stats(fn_or_f, obs, l, header='sigma_sig_limit'):
    if type(fn_or_f) == file:
        f = fn_or_f
    else:
        f = file(fn_or_f, 'wt')
    l.sort()
    n = len(l)
    if n % 2 == 0:
        median = (l[n/2] + l[n/2-1])/2.
    else:
        median = l[n/2]
    lo68 = l[int(n/2 - 0.34*n)]
    hi68 = l[int(n/2 + 0.34*n)]
    lo95 = l[int(n/2 - 0.475*n)]
    hi95 = l[int(n/2 + 0.475*n)]
    f.write(header + ':Expected  2.5%: r < ' + '%f\n' % lo95)
    f.write(header + ':Expected 16.0%: r < ' + '%f\n' % lo68)
    f.write(header + ':Expected 50.0%: r < ' + '%f\n' % median)
    f.write(header + ':Expected 84.0%: r < ' + '%f\n' % hi68)
    f.write(header + ':Expected 97.5%: r < ' + '%f\n' % hi95)
    f.write(header + ':Observed Limit: r < ' + '%f\n' % obs)
    f.close()
    return median, lo68, hi68, lo95, hi95

njobs, ntoysperjob = 50, 100
#njobs, ntoysperjob = 5, 20

def fromtree(fn, _jobre=re.compile(r'_(\d+)\.root$')):
    bn = os.path.basename(fn)
    f = ROOT.TFile(fn)
    ll = [x for x in detree(f.Get('limit'), 'limit:iToy', xform=(float,int))]
    if bn.startswith('expected'):
        mo = _jobre.search(bn)
        if mo:
            njobsexp = 1
            ntoysexp = ntoysperjob
        else:
            njobsexp = njobs
            ntoysexp = njobs * ntoysperjob

        if len(ll) == 2*ntoysexp: # for some reason, there are two entries for every iToy when --saveToys used
            ll2 = []
            for mi,(l,i) in enumerate(ll):
                assert (mi/2 % ntoysperjob)+1 == i
                if mi % 2 == 1:
                    ll2.append(l)
                elif mi % 2*ntoysperjob == 0: # and the limit value saved in the first entry for the first toy in each batch is ~1e-300!
                    assert l < 1e-300
                elif mi > 0:
                    assert l == ll2[-1]
            assert len(ll2) == ntoysexp
            return ll2
        else:
            if len(ll) != ntoysexp:
                try :
                    raise ValueError('fromtree %s failed: len(ll) = %i != %i' % (fn, len(ll), ntoysexp))
                except ValueError :
                    print "trying to skip"
                    return []
                
            jobordercheck = [b for _,b in ll]
            jobordershouldbe = range(1,ntoysperjob+1)*njobsexp
            if jobordercheck != jobordershouldbe:
                raise ValueError('fromtree %s failed: jobordercheck %r != $r' % (fn, jobordercheck, jobordershouldbe))
            return [a for a,_ in ll]
    else:
        assert bn == 'observed.root' and len(ll) == 1 and ll[0][1] == 0
        return [ll[0][0]]

def doit(path, out_fn):
    try :
        x = fromtree(os.path.join(path, 'observed.root'))
    except AttributeError or ValueError :
        print "%s not found, skipping" % os.path.join(path, 'observed.root')
        return
    if len(x) != 1:
        print 'using observed_byhand for this!'
        x = fromtree(os.path.join(path, 'observed_byhand.root'))
    obs = x[0]

    exp_fn = os.path.join(path, 'expected.root')
    if not os.path.isfile(exp_fn):
        exp_fns = glob(exp_fn.replace('.root','_*.root'))
        if len(exp_fns) != njobs:
            #return # FIXME!!!! only do this if comfortable with the failed jobs
            raise ValueError('only found %i files, expected %i' % (len(exp_fns), njobs))
        if not hadd(exp_fn, exp_fns):
            raise ValueError('problem hadding %s from %s files' % (exp_fn, len(exp_fns)))

    try :
        exp = fromtree(exp_fn)
    except AttributeError or ValueError :
        print "%s not found, skipping" % exp_fn
        return
    if len(exp) != njobs*ntoysperjob:
        try :
            raise ValueError('unexpected number of points in %s' % exp_fn) # this can't be given the asserts in fromtree right now
        except ValueError :
            print "trying to skip due to error"
            return

    stats(out_fn, obs, exp)

def rrange(path):
    l = fromtree(os.path.join(path, 'expected.root'))
    minl, maxl = min(l), max(l)
    print 'rm *.root %(path)s/observed_byhand.root ; combine -M BayesianToyMC %(path)s/datacard.txt --rMin %(minl)f --rMax %(maxl)f | tee %(path)s/byhand ; mv higgsCombineTest.BayesianToyMC.mH120.root %(path)s/observed_byhand.root' % locals()


if __name__ == '__main__':
    def _try(fcn,msg,*args):
        try:
            fcn(*args)
        except:
            print msg

    if bool_from_argv('copycrab'):
        import shutil
        from JMTucker.Tools.CRAB3ToolsBase import crab_dirs_root, crab_dirs_from_argv, crab_get_output_dir

        dest = crab_dirs_root(sys.argv[1])
        if not os.path.isdir(dest):
            os.mkdir(dest)

        for wd in crab_dirs_from_argv():
            isample = int(os.path.basename(wd).replace('crab_signal_',''))
            sampledir = os.path.join(dest, 'crab_signal_%05i' % isample)
            if not os.path.isdir(sampledir):
                os.mkdir(sampledir)
            od = os.path.join('/eos/uscms', crab_get_output_dir(wd)[1:], '0000')
            obs_fn = os.path.join(od, 'observed.root')
            if not os.path.isfile(obs_fn):
                obs_fn = os.path.join(od, 'observed_1.root')
            _try(shutil.copy2, 'could not copy observed.root for %s' % wd, obs_fn, os.path.join(sampledir, 'observed.root'))
            for fn in glob(os.path.join(od, 'expected_*.root')):
                _try(shutil.copy2, 'could not copy %s for %s' % (fn, wd), fn, os.path.join(sampledir, os.path.basename(fn)))
            #for fn in glob(os.path.join(od, 'combine_output*')):
            #    shutil.copy2(fn, os.path.join(sampledir, os.path.basename(fn)))

    elif bool_from_argv('unpackcrab'):
        import tempfile, shutil
        from JMTucker.Tools.CRAB3ToolsBase import crab_dirs_root, crab_dirs_from_argv, crab_get_output_dir

        dest = crab_dirs_root(sys.argv[1])
        if not os.path.isdir(dest):
            os.mkdir(dest)

        nds = []
        if 0:
            for wd in crab_dirs_from_argv():
                od = os.path.join('/eos/uscms', crab_get_output_dir(wd)[1:])
                nds += glob(os.path.join(od, '000?'))
                print wd, od, nds
        elif 1:
            for wd in crab_dirs_from_argv():
                nds += [wd]
            
        for nd in nds:
            fns = glob(os.path.join(nd, 'output_*.txz'))
            for fn in fns:
                job = int(os.path.basename(fn).replace('.txz','').rsplit('_',1)[1])
                job0 = job-1

                # argh lzma tarfile isn't avail in py2
                tmpdir = tempfile.mkdtemp()
                os.system('tar --directory=%s -xf %s' % (tmpdir, fn))
                #os.system('ls -l %s' % tmpdir)
                isample = int(open(os.path.join(tmpdir, 'isample.txt')).readlines()[job0])

                sampledir = os.path.join(dest, 'crab_signal_%05i' % isample)
                if not os.path.isdir(sampledir):
                    os.mkdir(sampledir)

                firstjob_lines = open(os.path.join(tmpdir, 'firstjob.txt')).readlines()
                ijob0 = None
                for i in xrange(job0, -1, -1):
                    if bool(int(firstjob_lines[i])):
                        ijob0 = job0 - i
                        break
                assert ijob0 is not None and 0 <= ijob0 < 50
                ijob = ijob0 + 1
                print fn, job, job0, isample, ijob0

                if ijob0 == 0:
                    shutil.copy2(os.path.join(tmpdir, 'observed.root'), os.path.join(sampledir, 'observed.root'))
                try :
                    shutil.copy2(os.path.join(tmpdir, 'expected.root'), os.path.join(sampledir, 'expected_%i.root' % ijob)) # follow crab convention
                except IOError :
                    print "IOError for %i, continue" %ijob
                    continue
                x = os.path.join(sampledir, 'combine_output_%i.txt' % ijob)
                shutil.copy2(os.path.join(tmpdir, 'combine_output.txt'), x)
                os.system('gzip %s' % x)

                shutil.rmtree(tmpdir)

    elif bool_from_argv('precheck'):
        files = ['combine_output_%i.txtgz', 'observed_%i.root', 'expected_%i.root']
        is_crab = bool_from_argv('is_crab')
        if is_crab:
            jobs = list(range(1,njobs+1))
        else:
            jobs = list(range(njobs))

        for path in sys.argv[1:]:
            for j in jobs:
                for bn in files:
                    fn = os.path.join(path, bn % j)
                    if not os.path.isfile(fn):
                        print 'missing file', fn

            first_j = 1 if is_crab else 0
            obs_fn_final = os.path.join(path, 'observed.root')
            obs_fn = os.path.join(path, 'observed_%i.root' % first_j)
            _try(os.rename, 'could not rename %s -> %s' % (obs_fn, obs_fn_final), obs_fn, obs_fn_final)
            for j in jobs:
                if j != first_j:
                    p = os.path.join(path, 'observed_%i.root' % j)
                    _try(os.remove, 'could not rm %s' % p, p)

    else:
        remake = bool_from_argv('remake')
        for path in sys.argv[1:]:
            out_fn = os.path.join(path, 'results')
            if not remake and os.path.isfile(out_fn):
                continue
            print path
            doit(path, out_fn)
