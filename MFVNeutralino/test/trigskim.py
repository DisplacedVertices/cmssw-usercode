from DVCode.Tools.CMSSWTools import *

process = basic_process('TrigSkim')
report_every(process, 1000000)
output_file(process, 'trigskim.root', ['keep *'])

import DVCode.MFVNeutralino.EventFilter as tf
tf.setup_event_filter(process)

#process.options.wantSummary = True
#set_lumis_to_process_from_json(process, 'jsons/ana_2015.json')
#process.maxEvents.input = 1000

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import DVCode.Tools.Samples as Samples 
    Samples.JetHT2015C.xrootd_url = 'root://se01.indiacms.res.in/'
    Samples.JetHT2015C.json = 'jsons/ana_2015.json'
    samples = [Samples.JetHT2015C]
    Samples.JetHT2015C.condor = True
    Samples.JetHT2015C.files_per = 5

    from DVCode.Tools.MetaSubmitter import MetaSubmitter
    ms = MetaSubmitter('TrigSkim_try3')
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
