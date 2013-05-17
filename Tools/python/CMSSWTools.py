import FWCore.ParameterSet.Config as cms

#process.source.firstLuminosityBlock = cms.untracked.uint32(2)

def replay_event(process, filename, rle, new_process_name='REPLAY'):
    '''Set the process up to replay the given event (rle is a 2- or
    3-tuple specifying it) using the random engine state saved in the
    file.'''
    
    if process.source.type_() == 'EmptySource':
        process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring(filename))        
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
