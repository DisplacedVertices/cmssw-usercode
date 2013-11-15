import os, sys, glob, FWCore.ParameterSet.Config as cms

#process.source.firstLuminosityBlock = cms.untracked.uint32(2)

def add_analyzer(process, name, **kwargs):
    '''Add a simple EDAnalyzer with its own separate path.'''
    
    if kwargs.has_key('_path'):
        path_name = kwargs['_path']
        del kwargs['_path']
    else:
        path_name = 'p' + name
    obj = cms.EDAnalyzer(name, **kwargs)
    setattr(process, name, obj)
    if hasattr(process, path_name):
        pobj = getattr(process, path_name)
        pobj *= obj # ugh
    else:
        setattr(process, path_name, cms.Path(obj))

def file_event_from_argv(process):
    '''Set the filename and event to run on from argv.'''
    file = None
    nums = []
    for arg in sys.argv[1:]:
        if arg.endswith('.root'):
            file = arg
        else:
            try:
                nums.append(int(arg))
            except ValueError:
                pass
    if file is not None:
        if not file.startswith('/store'):
            file = 'file:' + file
        print 'filename from argv:', file
        process.source.fileNames = [file]
    else:
        print 'file_event_from_argv warning: no filename found'
    l = len(nums)
    if l == 1:
        print 'maxEvents from argv:', nums[0]
        process.maxEvents.input = nums[0]
    elif l == 2 or l == 3:
        nums = tuple(nums)
        print 'set_events_to_process from argv:', nums
        set_events_to_process(process, [nums])
    else:
        print 'file_event_from_argv warning: did not understand event number'

def glob_store(pattern):
    if not pattern.startswith('/store'):
        raise ValueError('pattern must start with /store')
    magic = '/pnfs/cms/WAX/11/store'
    if not os.path.isdir(magic):
        raise ValueError('not at fermilab?')
    return [x.replace(magic, '/store') for x in glob.glob(pattern.replace('/store', magic))]
    
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

def set_events_to_process(process, run_events, run=None):
    '''Set the PoolSource parameter eventsToProcess appropriately,
    given the desired runs/event numbers passed in. If run is None,
    run_events must be a list of 2-tuples, each entry being a (run,
    event) pair. Otherwise, the run number is taken from run, and
    run_events is just a list of event numbers to be paired with run.

    run_events can also be a list of 3-tuples, where the middle entry
    in each is the lumisection number. This is ignored for now.
    '''
    if run is not None:
        for event in run_events:
            if type(event) != int:
                raise ValueError('with run=%s, expected run_events to be flat list of event numbers, but encountered item %r' % (run, event))
        run_events = [(run, event) for event in run_events]
    lengths = list(set(len(x) for x in run_events))
    if len(lengths) != 1 or lengths[0] not in (2,3):
        raise ValueError('expected either list of (run,event) or (run,ls,event) in run_events')
    process.source.eventsToProcess = cms.untracked.VEventRange(*[cms.untracked.EventRange(x[0],x[-1],x[0],x[-1]) for x in run_events])
    if lengths[0] == 3:
        process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange(*[cms.untracked.LuminosityBlockRange(x[0],x[1],x[0],x[1]) for x in run_events])

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

    if not hasattr(categories, '__iter__'):
        categories = (categories,)
    for category in categories:
        process.MessageLogger.categories.append(category)
        setattr(process.MessageLogger.cerr, category, cms.untracked.PSet(limit=cms.untracked.int32(0)))
