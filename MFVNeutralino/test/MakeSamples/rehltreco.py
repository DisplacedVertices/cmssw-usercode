from JMTucker.Tools.Samples import mfv_signal_samples

samples = mfv_signal_samples

from JMTucker.Tools.CRAB3Submitter import CRABSubmitter

cs = CRABSubmitter('mfv_run2_76x_rehltreco',
                   pset_template_fn = 'rawhlt.py',
                   dataset = 'sim',
                   splitting = 'EventAwareLumiBased',
                   units_per_job = 1000,
                   total_units = -1,
                   aaa = True,
                   publish_name = '76_reco_10k',
                   input_files = ['reco.py', 'merge_fjrs.py'],
                   output_files = 'reco.root',
                   script_exe = 'rehltreco.sh',
                   )

cs.submit_all(samples)
