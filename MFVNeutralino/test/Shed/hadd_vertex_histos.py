import sys, os, re
from collections import Counter
from pprint import pprint
from JMTucker.Tools import eos, SampleFiles
from JMTucker.Tools.hadd import hadd

if len(sys.argv) < 3:
    sys.exit('usage: %s dataset sample\n  where dataset and sample are as registered in SampleFiles. sample can be "*" to mean all samples having the dataset.' % sys.argv[0])

dataset = sys.argv[1]
sample = sys.argv[2]
interactive = True
verbosity = 0

if '-f' in sys.argv:
    interactive = False

while '-v' in sys.argv:
    verbosity += 1
    sys.argv.remove('-v')

if sample == '*':
    samples = []
    for s, ds in SampleFiles.keys():
        if ds == dataset:
            samples.append(s)
else:
    samples = [sample]

bn_re = re.compile(r'(.*)_(\d+)\.root')
path_re = re.compile(r'(/store.*/\d{6}_\d{6})/')

hadds = []

for sample in samples:
    if verbosity >= 1:
        print sample
    fns = SampleFiles.get_fns(sample, dataset)
    vh_fns = []

    # since the files can be spread out over multiple datedirs due to
    # resubmissions, put the file in the date dir that has most of the files
    new_vh_paths = Counter()
    
    for fn in fns:
        assert fn.endswith('.root')
        if verbosity >= 2:
            print fn
        if not eos.exists(fn):
            raise IOError('does not exist on eos: %r' % fn)

        dn, bn = os.path.split(fn)
        mo = bn_re.search(bn)
        if not mo:
            raise ValueError('could not parse fn %r' % fn)

        _, jobnum = mo.groups()
        jobnum = int(jobnum)

        path_mo = path_re.search(fn)
        if not path_mo:
            raise ValueError('could not parse path for %r' % fn)
        new_vh_paths[path_mo.group(1)] += 1

        vh_fn = os.path.join(dn, 'vertex_histos_%s.root' % jobnum)
        if verbosity >= 3:
            print dn, bn, jobnum, vh_fn
        if not eos.exists(vh_fn):
            raise IOError('no %r for %r' % vh_fn, fn)
        vh_fns.append(eos.canon(vh_fn))

    new_vh_path = new_vh_paths.most_common(1)[0][0]
    new_vh_fn = eos.canon(os.path.join(new_vh_path, 'vertex_histos.root'))
    if verbosity >= 3:
        print new_vh_fn
    if eos.exists(new_vh_fn):
        raise ValueError('exists already: %r' % new_vh_fn)

    hadds.append((new_vh_fn, vh_fns))

print 'will hadd and rm these:'
pprint(hadds)
if interactive:
    raw_input('ok?')
for new_fn, fns in hadds:
    if hadd(new_fn, fns):
        for fn in fns:
            eos.rm(fn)
