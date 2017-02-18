from JMTucker.Tools.CMSSWTools import *

process = basic_process('TrigSkim')
report_every(process, 1000000)
output_file(process, 'trigskim.root', ['keep *'])

import JMTucker.MFVNeutralino.TriggerFilter as tf
tf.setup_trigger_filter(process)

#process.options.wantSummary = True
#set_lumis_to_process_from_json(process, 'ana_2015.json')
#process.maxEvents.input = 1000

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 
    Samples.JetHT2015C.xrootd_url = 'root://cmseos.fnal.gov/'
    Samples.JetHT2015C.json = 'ana_2015.json'
    samples = [Samples.JetHT2015C]
    Samples.JetHT2015C.condor = False
    Samples.JetHT2015C.files_per = 5

    from JMTucker.Tools.MetaSubmitter import MetaSubmitter
    ms = MetaSubmitter('TrigSkim_try2')
    ms.common.publish_name = 'TrigSkim'
    ms.crab.job_control_from_sample = True
    ms.submit(samples)
