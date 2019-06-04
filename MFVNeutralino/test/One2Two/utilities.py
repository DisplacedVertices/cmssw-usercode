#!/usr/bin/env python

from JMTucker.MFVNeutralino.UtilitiesBase import *

####

_version = 'V25m'

def cmd_merge_bquarks_nobquarks():
    for year in '2017', '2018' :
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
    for year in '2017', '2018':

        if year == '2017' :
            tuple_ntracks_weights = (3,'0.83,0.17'), (4,'0.85,0.15'), (5,'0.93,0.07'), (7,'0.83,0.17')
        elif year == '2018' :
            tuple_ntracks_weights = (3,'0.86,0.14'), (4,'0.90,0.10'), (5,'0.97,0.03'), (7,'0.86,0.14')
        else :
            print("Unknown year (%s)! Exiting." % year)
            sys.exit()

        # for the f2 variation
        btag_frac_threetrk = float(tuple_ntracks_weights[0][1].split(",")[0])
        btag_frac_fivetrk  = float(tuple_ntracks_weights[2][1].split(",")[0])
        frac_variation = (btag_frac_fivetrk / btag_frac_threetrk) - 1

        for ntracks,weights in tuple_ntracks_weights :
            files = ['2v_from_jets_%s_%dtrack_btags_%s.root' % (year, ntracks, _version), '2v_from_jets_%s_%dtrack_nobtags_%s.root' % (year, ntracks, _version)]
            for fn in files:
                if not os.path.isfile(fn):
                    raise RuntimeError('%s not found' % fn)

            # nominal
            cmd = 'mergeTFileServiceHistograms -w %s -i %s -o 2v_from_jets_%s_%dtrack_btag_corrected_%s.root' % (weights, ' '.join(files), year, ntracks, _version)
            print cmd
            os.system(cmd)

            # f2 variation up
            weight_btag_up   = min( float(weights.split(",")[0]) * (1+frac_variation), 1)
            weight_nobtag_up = 1-weight_btag_up
            weights_up = '%.2f,%.2f' % (weight_btag_up, weight_nobtag_up)
            cmd = 'mergeTFileServiceHistograms -w %s -i %s -o 2v_from_jets_%s_%dtrack_btag_corrected_vary_3trk_to_5trk_up_%s.root' % (weights_up, ' '.join(files), year, ntracks, _version)
            print cmd
            os.system(cmd)

            # f2 variation down
            weight_btag_down   = min( float(weights.split(",")[0]) * (1-frac_variation), 1)
            weight_nobtag_down = 1-weight_btag_down
            weights_down = '%.2f,%.2f' % (weight_btag_down, weight_nobtag_down)
            cmd = 'mergeTFileServiceHistograms -w %s -i %s -o 2v_from_jets_%s_%dtrack_btag_corrected_vary_3trk_to_5trk_down_%s.root' % (weights_down, ' '.join(files), year, ntracks, _version)
            print cmd
            os.system(cmd)


####

if __name__ == '__main__':
    main(locals())
