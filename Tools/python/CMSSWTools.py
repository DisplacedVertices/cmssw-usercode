import os, sys, glob, FWCore.ParameterSet.Config as cms

class CMSSWSettings(object):
    def __init__(self):
        from JMTucker.Tools.Year import year
        self.year = year
        self.is_mc = True
        #self.is_miniaod
        #self.repro

# following FWCore.ParameterSet.MassReplace.MassSearchReplaceAnyInputTagVisitor
class InputTagCollector(object):
    @staticmethod
    def input_tag(x):
       return x if isinstance(x, cms.InputTag) else cms.InputTag(x)

    def __init__(self):
        self._result = []
    def result(self):
        return self._result

    def doit(self, pizable, base):
        if isinstance(pizable, cms._Parameterizable):
            for name, value in pizable.parameters_().items():
                pytype = value.pythonTypeName()
                based_name = '%s.%s' % (base, name)
                if pytype == 'cms.PSet':
                    self.doit(value, based_name)
                elif pytype == 'cms.VPSet':
                    for i, x in enumerate(value):
                        self.doit(x, "%s[%d]" % (based_name, i))
                elif pytype == 'cms.VInputTag':
                    for i, x in enumerate(value):
                         self._result.append(('%s[%i]' % (based_name, i), self.input_tag(x)))
                elif pytype.endswith('.InputTag'):
                    self._result.append((based_name, self.input_tag(value)))

    def enter(self,visitee):
        self.doit(visitee, '')
    def leave(self,visitee):
        pass

class ReferencedTagsTaskAdder(object):
    # for some reason the patTask doesn't have everything in it, or I don't understand something

    def __init__(self, process, task=None):
        self.process = process
        self.task = process.patTask if task is None else task
        self.seen = set()

    def doit(self, name, obj, seen=set()):
        self.seen.add(name)
        for _, tag in input_tags_referenced(obj):
            if hasattr(self.process, tag.moduleLabel):
                obj2 = getattr(process, tag.moduleLabel)
                if tag.moduleLabel not in self.task.moduleNames():
                    self.task.add(obj2)
                if tag.moduleLabel not in self.seen:
                    self.doit(tag.moduleLabel, obj2)

    def modules_to_add(self, *finals):
        before = set(self.task.moduleNames())
        for f in finals:
            if type(f) == str:
                f = getattr(process, f)
            self.doit(name, f)
        after = set(self.task.moduleNames())
        return before, after, sorted(after - before)

def add_analyzer(process, name, *args, **kwargs):
    '''Add a simple EDAnalyzer with its own separate path.'''
    
    if kwargs.has_key('_path'):
        path_name = kwargs['_path']
        del kwargs['_path']
    else:
        path_name = 'p' + name
    obj = cms.EDAnalyzer(name, *args, **kwargs)
    setattr(process, name, obj)
    if hasattr(process, path_name):
        pobj = getattr(process, path_name)
        pobj *= obj # ugh
    else:
        setattr(process, path_name, cms.Path(obj))

def basic_process(name, filenames=['file:input.root']):
    process = cms.Process(name)
    process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
    process.maxLuminosityBlocks = cms.untracked.PSet(input = cms.untracked.int32(-1))
    process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
    process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring(*filenames))
    return process

def cmssw_base(extra=''):
    b = os.environ['CMSSW_BASE']
    return os.path.join(b, extra) if extra else b

def input_files(process, fns):
    if type(fns) == str:
        if not fns.endswith('.root'):
            files_from_file(process, fns)
            return
        fns = [fns]
    files = []
    for fn in fns:
        if not fn.startswith('/store') and not fn.startswith('root://'):
            fn = 'file:' + fn
        files.append(fn)
    process.source.fileNames = cms.untracked.vstring(*files)

def files_from_file(process, fn, n=-1):
    fns = [line.strip() for line in open(fn).read().split('\n') if line.strip().endswith('.root')]
    if n > 0:
        fns = fns[:n]
    process.source.fileNames = cms.untracked.vstring(*fns)
    return fns

def file_event_from_argv(process, warn=True):
    '''Set the filename and event to run on from argv.'''
    files = []
    nums = []
    for arg in sys.argv[1:]:
        if arg.endswith('.root'):
            files.append(arg)
        else:
            try:
                nums.append(int(arg))
            except ValueError:
                pass
    if files:
        files_ = []
        for file in files:
            if not file.startswith('/store') and not file.startswith('root://'):
                file = 'file:' + file
            files_.append(file)
        files = files_
        print 'files from argv:'
        for file in files:
            print file
        process.source.fileNames = files
    elif warn:
        print 'file_event_from_argv warning: no filename found'
    l = len(nums)
    if l == 1:
        print 'maxEvents from argv:', nums[0]
        process.maxEvents.input = nums[0]
    elif l == 2 or l == 3:
        nums = tuple(nums)
        print 'set_events from argv:', nums
        set_events(process, [nums])
    elif warn:
        print 'file_event_from_argv warning: did not understand event number'

def find_output_files(process):
    '''Get the TFileService and PoolOutputModule filenames if these
    services exist in process.'''

    d = {}
    if hasattr(process, 'TFileService'):
        d['TFileService'] = [process.TFileService.fileName.value()]
    d['PoolOutputModule'] = [v.fileName.value() for v in process.outputModules.itervalues()]
    return d

def friendly_argparse(**kwargs):
    '''Set up an ArgumentParser that doesn't conflict with cmsRun arg
    parsing: use + as prefix for options, and consume all positional
    arguments away. Also return a printer function for the args.'''

    import argparse
    parser = argparse.ArgumentParser(prefix_chars='+', **kwargs) # prefix + to not clash with cmsRun
    parser.add_argument('cmsrunargs', nargs='*') # let cmsRun have positionals
    def printer(name, args):
        to_print = [x for x in dir(args) if not x.startswith('_') and x != 'cmsrunargs']
        maxl = max(len(x) for x in to_print)
        print name + ' BEGIN'
        for x in dir(args):
            if not x.startswith('_') and x != 'cmsrunargs':
                print x.ljust(maxl + 5), getattr(args,x)
        print name + ' END'
    return parser, printer

def geometry_etc(process, tag=None):
    global_tag(process, tag)
    process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
    process.load('Configuration.StandardSequences.MagneticField_cff')
    process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
    
def global_tag(process, tag=None):
    if not tag:
        tag = which_global_tag()
    process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
    from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
    process.GlobalTag = GlobalTag(process.GlobalTag, tag, '')

def glob_store(pattern):
    if not pattern.startswith('/store'):
        raise ValueError('pattern must start with /store')
    magic = '/eos/uscms/store'
    if not os.path.isdir(magic):
        raise ValueError('not at fermilab?')
    return [x.replace(magic, '/store') for x in glob.glob(pattern.replace('/store', magic))]

def input_tags_referenced(thing):
    '''Get all the InputTags referenced under thing.
    thing can be a single module or a sequence/path.'''
    coll = InputTagCollector()
    if isinstance(thing, cms._ModuleSequenceType):
        thing.visit(coll)
    elif isinstance(thing, cms._Module):
        thing.visitNode(coll)
    return coll.result()

def is_edm_file(fn):
    return os.system('edmFileUtil %s >/dev/null 2>&1' % fn) == 0

def json_path(bn):
    return os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/test/jsons', bn)

def merge_edm_files(out_fn, fns):
    print 'merging %i edm files to %s' % (len(fns), out_fn)
    cmd = 'cmsRun $CMSSW_BASE/src/JMTucker/Tools/python/Merge_cfg.py argv %s out=%s >%s.mergelog 2>&1' % (' '.join(fns), out_fn, out_fn)
    #print cmd
    return os.system(cmd) == 0

def make_tarball(fn, include_bin=True, include_python=False, include_interface=False, verbose=False):
    '''Make a tarball for the current work area. Paths in the tarball
    are relative to $CMSSW_BASE.
    '''
    scram_arch = os.environ['SCRAM_ARCH']
    base = os.path.normpath(os.environ['CMSSW_BASE'])
    src = os.path.join(base, 'src')

    # https://github.com/dmwm/CRABClient/blob/376f2962bceb5eb68a243d83b394b35c73b03220/src/python/CRABClient/JobType/UserTarball.py
    to_add = ['lib', 'biglib', 'module', 'external']
    if include_python:
        to_add += ['cfipython']
    if include_bin:
        to_add += ['bin']
    to_add = [os.path.join(base, x + '/' + scram_arch) for x in to_add]
    if include_python:
        to_add += [os.path.join(base, 'python')] # doesn't have scram_arch subdir
    to_add = [x for x in to_add if os.path.exists(x)]

    extras = ['data']
    if include_python:
        extras.append('python')
    if include_interface:
        extras.append('interface')

    if extras:
        for root, dirs, files in os.walk(src, topdown=True):
            rel_root = os.path.relpath(root, base)
            if rel_root.count('/') != 2:
                dirs = []
            for x in ['.git', '.svn', 'CVS']:
                if x in dirs:
                    dirs.remove(x)
            for d in dirs:
                if d in extras:
                    to_add.append(os.path.join(root, d))

    if verbose:
        print 'adding to tarball:'

    import tarfile
    with tarfile.open(fn, "w:gz") as tar:
        for abs_d in to_add:
            rel_d = os.path.relpath(abs_d, base)
            if verbose:
                print abs_d, rel_d
            tar.add(abs_d, arcname=rel_d)

def max_events(process, n):
    if not hasattr(process, 'maxEvents'):
        process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(n))
    else:
        process.maxEvents.input = n

def no_event_sort(process):
    process.source.noEventSort = cms.untracked.bool(True)

def output_file(process, filename, output_commands, select_events=[]):
    process.out = cms.OutputModule('PoolOutputModule',
                                   fileName = cms.untracked.string(filename),
                                   compressionLevel = cms.untracked.int32(4),
                                   compressionAlgorithm = cms.untracked.string('LZMA'),
                                   eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
                                   outputCommands = cms.untracked.vstring(*output_commands),
                                   dropMetaData = cms.untracked.string('ALL'),
                                   fastCloning = cms.untracked.bool(False),
                                   overrideInputFileSplitLevels = cms.untracked.bool(True)
                                   )
    if select_events:
        process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring(*select_events))
    process.outp = cms.EndPath(process.out)

def random_service(process, seeds):
    '''Set up the RandomNumberGeneratorService. seeds is a dict taking
    labels of modules to the random number seed for that module. If
    the seed is <0, then a random seed is generated.'''

    r = process.RandomNumberGeneratorService = cms.Service('RandomNumberGeneratorService')
    for k,v in seeds.iteritems():
        if v < 0:
            from random import SystemRandom
            v = SystemRandom().randint(1, 900000000)
        setattr(r, k, cms.PSet(initialSeed = cms.untracked.uint32(v)))

def registration_warnings(process):
    if not hasattr(process, 'MessageLogger'):
        process.load('FWCore.MessageService.MessageLogger_cfi')
    for x in ['GetManyWithoutRegistration', 'GetByLabelWithoutRegistration']:
        process.MessageLogger.categories.append(x)
        setattr(process.MessageLogger.cerr, x, cms.untracked.PSet(reportEvery = cms.untracked.int32(1),
                                                                  optionalPSet = cms.untracked.bool(True),
                                                                  limit = cms.untracked.int32(10000000)
                                                                  ))

def replay_event(process, filename, rle, new_process_name='REPLAY'):
    '''Set the process up to replay the given event (rle is a 2- or
    3-tuple specifying it) using the random engine state saved in the
    file.'''

    if process.source.type_() == 'EmptySource':
        process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring())
    if filename is None and rle is None:
        file_event_from_argv(process)
    else:
        process.source.fileNames = cms.untracked.vstring(filename)
        set_events(process, [rle])
    process.RandomNumberGeneratorService.restoreStateLabel = cms.untracked.string('randomEngineStateProducer')
    process.setName_(new_process_name)

def report_every(process, i):
    if not hasattr(process, 'MessageLogger'):
        process.load('FWCore.MessageLogger.MessageLogger_cfi')
    process.MessageLogger.cerr.FwkReport.reportEvery = i

def sample_files(process, sample, dataset, n=-1):
    import JMTucker.Tools.SampleFiles as sf
    sf.set_process(process, sample, dataset, n)

def set_events(process, events, run=None):
    '''Set the PoolSource parameter eventsToProcess appropriately,
    given the desired runs/event numbers passed in. If run is None,
    run_events must be a list of 3-tuples, each entry being (run, lumi,
    event). If run is a number, list must be of 2-tuples (lumi, event).
    '''
    if type(run) == int:
        for event in events:
            if type(event) != tuple or len(event) != 2:
                raise ValueError('with run=%s, expected events to be list of (lumi,event) pairs, but encountered item %r' % (run, event))
        events = [(run,) + event for event in events]
    lengths = list(set(len(x) for x in events))
    if len(lengths) != 1 or lengths[0] != 3:
        raise ValueError('expected either list of (lumi,event) or (run,lumi,event) in events')
    process.source.eventsToProcess = cms.untracked.VEventRange(*[cms.untracked.EventRange(x[0],x[1],x[2], x[0],x[1],x[2]) for x in events])

def set_lumis(process, *args, **kwargs):
    '''What CRAB does when you use lumi_mask.'''

    from FWCore.PythonUtilities.LumiList import LumiList
    process.source.lumisToProcess = LumiList(*args, **kwargs).getVLuminosityBlockRange()

def set_seeds(process, seed=12191982, size=2**24):
    '''Set all the seeds for the RandomNumberGeneratorService in a
    deterministic way, starting with the master seed above.

    Warning: modifies python's RNG state.
    '''
    import random
    random.seed(seed)
    svc = process.RandomNumberGeneratorService
    for k,v in svc.parameters_().iteritems():
        getattr(svc, k).initialSeed = random.randint(0, size)

def silence_messages(process, categories):
    '''Make MessageLogger shut up about the categories listed.'''

    print 'silencing MessageLogger about these categories:', categories
    if not hasattr(process, 'MessageLogger'):
        process.load('FWCore.MessageLogger.MessageLogger_cfi')
    if not hasattr(categories, '__iter__'):
        categories = (categories,)
    for category in categories:
        process.MessageLogger.categories.append(category)
        setattr(process.MessageLogger.cerr, category, cms.untracked.PSet(limit=cms.untracked.int32(0)))

def simple_memory_check(process):
    process.add_(cms.Service('SimpleMemoryCheck'))

def remove_tfileservice(process):
    try:
        del process.TFileService
    except KeyError:
        pass

def tfileservice(process, filename='tfileservice.root'):
    process.TFileService = cms.Service('TFileService', fileName = cms.string(filename))

def tracer(process):
    process.Tracer = cms.Service('Tracer')

def want_summary(process, val=True):
    if not hasattr(process, 'options'):
        process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(val))
    else:
        process.options.wantSummary = cms.untracked.bool(val)

def which_global_tag(settings=None):
    if not settings:
        settings = CMSSWSettings()
    if settings.year == 2017:
        if settings.is_mc:
            return '94X_mc2017_realistic_v10' # JMTBAD v14 or v16
        else:
            return '94X_dataRun2_ReReco_EOY17_v6' # JMTBAD maybe should be 94X_dataRun2_v10 from looking in https://cms-conddb.cern.ch/cmsDbBrowser/diff/Prod/gts/94X_dataRun2_ReReco_EOY17_v6/94X_dataRun2_v10
    elif settings.year == 2018:
        if settings.is_mc:
            return '102X_upgrade2018_realistic_v12'
        else:
            return '102X_dataRun2_Prompt_v11'
    else:
        raise ValueError('what year is it')
