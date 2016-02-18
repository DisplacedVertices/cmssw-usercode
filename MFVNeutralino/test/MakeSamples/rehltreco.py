from JMTucker.Tools.Samples import mfv_signal_samples

samples = mfv_signal_samples[:1]

from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
cs = CRABSubmitter('mfv_run2_76x_rawhltreco',
                   pset_template_fn = 'rawhlt.py',
                   dataset = 'sim',
                   splitting = 'EventAwareLumiBased',
                   units_per_job = 100,
                   total_units = 200,
                   aaa = True,
                   publish_name = '76reco_10k',
                   input_files = ['reco.py', 'merge_fjrs.py'],
                   output_files = 'reco.root',
                   script_exe = 'rehltreco.sh',
                   )
cs.submit_all(samples)
