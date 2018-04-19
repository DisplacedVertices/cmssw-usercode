#!/usr/bin/env python

from JMTucker.Tools.CMSSWTools import *
process = basic_process('PickByVeto')
report_every(process, 1000000)

process.veto = cms.EDFilter('EventIdVeto',
                            use_run = cms.bool(False),
                            list_fn = cms.string('veto.gz'),
                            debug = cms.untracked.bool(False),
                            )

process.p = cms.Path(~process.veto)

process.out = cms.OutputModule('PoolOutputModule',
                               fileName = cms.untracked.string('pick.root'),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
                               )

process.outp = cms.EndPath(process.out)

if 'debug' in sys.argv:
    process.options.wantSummary = True
    process.veto.debug = True
    report_every(process, 1)

####

parser, args_printer = friendly_argparse()
parser.add_argument('+job', type=int, help='which job')
parser.add_argument('+per', type=int, help='how many files per job')
parser.add_argument('+sample', help='which sample to use', choices=['qcdht1000', 'qcdht1500', 'qcdht2000'])
parser.add_argument('+out-fn', help='output filename')
args = parser.parse_args()

x = [y is not None for y in (args.job, args.per, args.sample)]
if any(x):
    if not all(x):
        raise ValueError('if supplying any of +job, +per, +sample, must supply all')

    args.event_list_fn = 'vetolist.%s' % args.sample
    args.file_list_fn = 'filelist.%s.gz' % args.sample
    args_printer('args', args)

    if args.job < 0:
        raise ValueError('job must be non-negative')
    if args.per <= 0:
        raise ValueError('per must be positive')

    for x in (args.event_list_fn, args.file_list_fn):
        if not os.path.isfile(x):
            raise IOError('file not found: %s' % x)

    process.veto.list_fn = args.event_list_fn

    import gzip
    files = [x.strip() for x in gzip.open(args.file_list_fn) if x.strip()]
    files = files[args.job*args.per:(args.job+1)*args.per]
    if not files:
        raise ValueError('out of files')
    process.source.fileNames = files

    if args.out_fn is not None:
        process.out.fileName = args.out_fn
else:
    file_event_from_argv(process)

####

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Year import year
    import JMTucker.Tools.Samples as Samples 
    if year == 2015:
        samples = Samples.data_samples_2015 + Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015
    elif year == 2016:
        samples = Samples.data_samples + Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext

    for sample in samples:
        # JMTBAD need to unify the way crabsubmitter and condorsubmitter do this crap
        sample.files_per = 50
        sample.json = 'json.%s' % sample.name

    def vetolist_fn(sample):
        fn = 'vetolist.%s.gz' % sample.name
        assert os.path.isfile(fn)
        return fn

    def pset_modifier(sample):
        to_add = ['process.veto.list_fn = "%s"' % vetolist_fn(sample)]
        if not sample.is_mc:
            to_add.append('process.veto.use_run = True')
        return to_add, []

    def cfg_modifier(cfg, sample):
        cfg.JobType.inputFiles = [vetolist_fn(sample)]
        cfg.Data.lumiMask = 'json.%s' % sample.name

    from JMTucker.Tools.MetaSubmitter import *
    batch_name = 'Pick1VtxV1'
    ms = MetaSubmitter(batch_name)
    ms.common.ex = year
    ms.common.pset_modifier = pset_modifier
    ms.common.publish_name = batch_name + '_' + str(year)
    ms.crab.cfg_modifier = cfg_modifier
    ms.crab.splitting = 'FileBased'
    ms.crab.units_per_job = 50
    ms.crab.total_units = -1
    ms.condor.input_files = ['vetolist.%s.gz' % s.name for s in samples]
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
