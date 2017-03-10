import os, sys, glob, FWCore.ParameterSet.Config as cms

#process.source.firstLuminosityBlock = cms.untracked.uint32(2)

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

def files_from_file(process, fn):
    fns = [line.strip() for line in open(fn).read().split('\n') if line.strip().endswith('.root')]
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
        print 'set_events_to_process from argv:', nums
        set_events_to_process(process, [nums])
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

def geometry_etc(process, tag):
    global_tag(process, tag)
    process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
    process.load('Configuration.StandardSequences.MagneticField_cff')
    process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
    
def global_tag(process, tag):
    process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
    from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
    process.GlobalTag = GlobalTag(process.GlobalTag, tag, '')

def glob_store(pattern):
    if not pattern.startswith('/store'):
        raise ValueError('pattern must start with /store')
    magic = '/pnfs/cms/WAX/11/store'
    if not os.path.isdir(magic):
        raise ValueError('not at fermilab?')
    return [x.replace(magic, '/store') for x in glob.glob(pattern.replace('/store', magic))]

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

def output_file(process, filename, output_commands):
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
        set_events_to_process(process, [rle])
    process.RandomNumberGeneratorService.restoreStateLabel = cms.untracked.string('randomEngineStateProducer')
    process.setName_(new_process_name)

def report_every(process, i):
    if not hasattr(process, 'MessageLogger'):
        process.load('FWCore.MessageLogger.MessageLogger_cfi')
    process.MessageLogger.cerr.FwkReport.reportEvery = i

def sample_files(process, sample, dataset, a=0, b=None):
    import JMTucker.Tools.SampleFiles as sf
    if b is None:
        b = a+1
    process.source.fileNames = sf.get(sample, dataset)[1][a:b]

def set_events_to_process_ex(run_events, run=None):
    if run is not None:
        for event in run_events:
            if type(event) != int:
                raise ValueError('with run=%s, expected run_events to be flat list of event numbers, but encountered item %r' % (run, event))
        run_events = [(run, event) for event in run_events]
    lengths = list(set(len(x) for x in run_events))
    if len(lengths) != 1 or lengths[0] not in (2,3):
        raise ValueError('expected either list of (run,event) or (run,ls,event) in run_events')
    return run_events

def set_events_to_process(process, run_events, run=None):
    '''Set the PoolSource parameter eventsToProcess appropriately,
    given the desired runs/event numbers passed in. If run is None,
    run_events must be a list of 2-tuples, each entry being a (run,
    event) pair. Otherwise, the run number is taken from run, and
    run_events is just a list of event numbers to be paired with run.

    run_events can also be a list of 3-tuples, where the middle entry
    in each is the lumisection number.
    '''
    run_events = set_events_to_process_ex(run_events, run)
    process.source.eventsToProcess = cms.untracked.VEventRange(*[cms.untracked.EventRange(x[0],x[-1],x[0],x[-1]) for x in run_events])
    if len(run_events[0]) == 3:
        process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange(*[cms.untracked.LuminosityBlockRange(x[0],x[1],x[0],x[1]) for x in run_events])

def set_events_to_process_by_filter(process, run_events=None, run=None, run_events_fn='set_events_to_process_by_filter.txt', path_name=None):
    '''Like the other function, only run specific events specified in
    run_events. Here we use the EventIdVeto plugin with a temp file
    listing the events. This works better with splitting among batch
    jobs where event numbers might be duplicated in different lumis,
    or the particular combination of events/lumisToProcess
    specifications result in no events and invalid root files returned
    in certain jobs.

    The run_events list must include luminosity block (i.e. a list of
    3-tuples).

    Or if run_events is None, take the list pre-made from run_events_fn (no
    value checking done).
    
    We return the filename for the list of events so that it can be
    passed to e.g. CRABSubmitter.
    '''
    if run_events is not None:
        run_events = set_events_to_process_ex(run_events, run)
        if len(run_events[0]) == 3:
            raise ValueError('run_events must be a list of 3-tuples (run, lumi, event)')

        f = open(run_events_fn, 'wt')
        for rle in run_events:
            f.write('(%i,%i,%i),\n' % rle)
        f.close()

    if hasattr(process, 'EventIdVeto'):
        raise ValueError('process already has EventIdVeto object')
    process.EventIdVeto = cms.EDFilter('EventIdVeto',
                                       use_run = cms.bool(False),
                                       list_fn = cms.string(run_events_fn)
                                       )
    for p in process.paths.keys():
        getattr(process, p).insert(0, ~process.EventIdVeto)

    if path_name is not None:
        setattr(process, path_name, cms.Path(~process.EventIdVeto))

    process.maxEvents.input = cms.untracked.int32(-1)
    for x in 'skipEvents eventsToSkip lumisToSkip eventsToProcess lumisToProcess firstRun firstLuminosityBlock firstEvent'.split():
        if hasattr(process.source, x):
            delattr(process.source, x)

    return run_events_fn

def set_lumis_to_process_from_json(process, json):
    '''What CRAB does when you use lumi_mask.'''

    from FWCore.PythonUtilities.LumiList import LumiList
    process.source.lumisToProcess = LumiList(json).getVLuminosityBlockRange()

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

def tfileservice(process, filename='tfileservice.root'):
    process.TFileService = cms.Service('TFileService', fileName = cms.string(filename))

def tracer(process):
    process.Tracer = cms.Service('Tracer')
