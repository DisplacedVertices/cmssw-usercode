import glob, sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.source.fileNames = glob.glob('/store/user/tucker/mfv_neutralino_tau1000um_M0400/repubmerge/150618_233219/0000/merge*.root')
process.TFileService.fileName = 'corrforgeomeff.root'
process.maxEvents.input = 1000
add_analyzer('MFVCorrelationsForGeomEff')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter

    Samples.mfv_neutralino_tau1000um_M0200.ana_dataset_override = '/mfv_neutralino_tau1000um_M0200/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0300.ana_dataset_override = '/mfv_neutralino_tau1000um_M0300/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0400.ana_dataset_override = '/mfv_neutralino_tau1000um_M0400/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0600.ana_dataset_override = '/mfv_neutralino_tau1000um_M0600/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0800.ana_dataset_override = '/mfv_neutralino_tau1000um_M0800/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M1000.ana_dataset_override = '/mfv_neutralino_tau1000um_M1000/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'

    samples = [Samples.mfv_neutralino_tau1000um_M0200, Samples.mfv_neutralino_tau1000um_M0300, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau1000um_M0600, Samples.mfv_neutralino_tau1000um_M0800, Samples.mfv_neutralino_tau1000um_M1000]

    for sample in Samples.mfv_signal_samples:
        sample.ana_scheduler = 'remoteGlidein'

    cs = CRABSubmitter('MFVCorrelationsForGeomEff',
                       total_number_of_events = -1,
                       events_per_job = 20000,
                       use_ana_dataset = True,
                       USER_skip_servers = 'cern_vocms0117',
                       )
    cs.submit_all(samples)

    
