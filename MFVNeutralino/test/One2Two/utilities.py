#!/usr/bin/env python

from JMTucker.MFVNeutralino.UtilitiesBase import *
from f2_vals import dict_of_f2_tuples
####

_version = 'V27p1Bm'

def cmd_merge_bquarks_nobquarks():
    for year in ['2017', '2018'] :
        if year == '2017' :
            weights = '0.79,0.21'
        elif year == '2018' :
            weights = '0.81,0.19'
        for ntracks in 3,4,5,7:
            files = ['2v_from_jets_%s_%dtrack_bquarks_%s.root' % (year, ntracks, _version), '2v_from_jets_%s_%dtrack_nobquarks_%s.root' % (year, ntracks, _version)]
            for fn in files:
                if not os.path.isfile(fn):
                    raise RuntimeError('%s not found' % fn)
            cmd = 'mergeTFileServiceHistograms -w %s -i %s -o 2v_from_jets_%s_%dtrack_bquark_corrected_%s.root' % (weights, ' '.join(files), year, ntracks, _version)
            print cmd
            os.system(cmd)

def cmd_merge_btags_nobtags():
    #for is_data in False, True:
    #    for year in ['2017', '2018', '2017p8']:
    for is_data in False, :
        for year in ['2017']:
            if is_data:
                year = 'data_%s' % year
            for sys_var in ['nom','bcjet_up','bcjet_down','ljet_up','ljet_down', 'vary_dphi', 'vary_eff']:
                tuple_ntracks_weights = dict_of_f2_tuples.get('%s_%s' % (year, sys_var), ())

                frac_variation = 1
                if sys_var == 'nom':
                    btag_frac_threetrk = btag_frac_fourtrk = btag_frac_fivetrk = 1
                    for ntk, wt in tuple_ntracks_weights:
                        frac = float(wt.split(",")[0])
                        if ntk == 3:
                            btag_frac_threetrk = frac
                        if ntk == 4:
                            btag_frac_fourtrk = frac
                        if ntk == 5:
                            btag_frac_fivetrk = frac
                    if btag_frac_threetrk == 1 or btag_frac_fourtrk == 1 or btag_frac_fivetrk == 1:
                        print "WARNING: You might not have run everything (intentional or not) so don't trust your result"

                    # ratio of 5-trk to 4-trk f2 values, for the f2 systematic variation
                    frac_variation = (btag_frac_fivetrk / btag_frac_fourtrk) - 1

                for ntracks,weights in tuple_ntracks_weights :
                    files = ['2v_from_jets_%s_%dtrack_btags_%s.root' % (year, ntracks, _version), '2v_from_jets_%s_%dtrack_nobtags_%s.root' % (year, ntracks, _version)]
                    if sys_var in ['vary_dphi', 'vary_eff']:
                        files = ['2v_from_jets_%s_%dtrack_%s_btags_%s.root' % (year, ntracks, sys_var, _version), '2v_from_jets_%s_%dtrack_%s_nobtags_%s.root' % (year, ntracks, sys_var, _version)]
                    for fn in files:
                        if not os.path.isfile(fn):
                            raise RuntimeError('%s not found' % fn)

                    cmd = 'mergeTFileServiceHistograms -w %s -i %s -o 2v_from_jets_%s_%dtrack_btag_corrected_%s_%s.root' % (weights, ' '.join(files), year, ntracks, sys_var, _version)
                    print cmd
                    os.system(cmd)

                    if sys_var == 'nom':
                        # f2 variation up
                        weight_btag_up   = min( float(weights.split(",")[0]) * (1.0/(1+frac_variation)*(1+2*frac_variation)), 1)
                        weight_nobtag_up = 1-weight_btag_up
                        weights_up = '%f,%f' % (weight_btag_up, weight_nobtag_up)
                        cmd = 'mergeTFileServiceHistograms -w %s -i %s -o 2v_from_jets_%s_%dtrack_btag_corrected_vary_4trk_to_5trk_up_%s.root' % (weights_up, ' '.join(files), year, ntracks, _version)
                        print cmd
                        os.system(cmd)

                        # f2 variation down
                        weight_btag_down   = min( float(weights.split(",")[0]) * (1.0/(1+frac_variation)), 1)
                        weight_nobtag_down = 1-weight_btag_down
                        weights_down = '%f,%f' % (weight_btag_down, weight_nobtag_down)
                        cmd = 'mergeTFileServiceHistograms -w %s -i %s -o 2v_from_jets_%s_%dtrack_btag_corrected_vary_4trk_to_5trk_down_%s.root' % (weights_down, ' '.join(files), year, ntracks, _version)
                        print cmd
                        os.system(cmd)

####

if __name__ == '__main__':
    main(locals())
