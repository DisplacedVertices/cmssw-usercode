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
            tuple_ntracks_weights                    = (3,'0.83,0.17'), (4,'0.85,0.15'), (5,'0.93,0.07'), (7,'0.83,0.17')
            tuple_ntracks_weights_SFs_20percent_down = (3,'0.90,0.10'), (4,'0.92,0.08'), (5,'0.97,0.03'), (7,'0.90,0.10')
            tuple_ntracks_weights_SFs_20percent_up   = (3,'0.78,0.22'), (4,'0.81,0.19'), (5,'0.89,0.11'), (7,'0.78,0.22')
            tuple_ntracks_weights_SFs_10percent_down = (3,'0.86,0.14'), (4,'0.88,0.12'), (5,'0.95,0.05'), (7,'0.87,0.13')
            tuple_ntracks_weights_SFs_10percent_up   = (3,'0.80,0.20'), (4,'0.83,0.17'), (5,'0.91,0.09'), (7,'0.81,0.19')
        elif year == '2018' :
            tuple_ntracks_weights                    = (3,'0.86,0.14'), (4,'0.90,0.10'), (5,'0.97,0.03'), (7,'0.86,0.14')
            tuple_ntracks_weights_SFs_20percent_down = (3,'0.92,0.08'), (4,'0.95,0.05'), (5,'0.99,0.01'), (7,'0.92,0.08')
            tuple_ntracks_weights_SFs_20percent_up   = (3,'0.82,0.18'), (4,'0.86,0.14'), (5,'0.95,0.05'), (7,'0.82,0.18')
            tuple_ntracks_weights_SFs_10percent_down = (3,'0.89,0.11'), (4,'0.92,0.08'), (5,'0.98,0.02'), (7,'0.89,0.11')
            tuple_ntracks_weights_SFs_10percent_up   = (3,'0.84,0.16'), (4,'0.88,0.12'), (5,'0.96,0.04'), (7,'0.84,0.16')
        else :
            print("Unknown year (%s)! Exiting." % year)
            sys.exit()

        # for the f2 variation
        btag_frac_threetrk = float(tuple_ntracks_weights[0][1].split(",")[0])
        btag_frac_fivetrk  = float(tuple_ntracks_weights[2][1].split(",")[0])
        frac_variation = (btag_frac_fivetrk / btag_frac_threetrk) - 1

        # for the nominal and the f2 variation
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


        # for the SF variations
        for syst in ['vary_SFs_20percent_down', 'vary_SFs_20percent_up', 'vary_SFs_10percent_down', 'vary_SFs_10percent_up'] :

            if syst == 'vary_SFs_20percent_down' : 
                tuple_ntracks_weights_syst = tuple_ntracks_weights_SFs_20percent_down
            elif syst == 'vary_SFs_20percent_up' : 
                tuple_ntracks_weights_syst = tuple_ntracks_weights_SFs_20percent_up
            elif syst == 'vary_SFs_10percent_down' : 
                tuple_ntracks_weights_syst = tuple_ntracks_weights_SFs_10percent_down
            elif syst == 'vary_SFs_10percent_up' : 
                tuple_ntracks_weights_syst = tuple_ntracks_weights_SFs_10percent_up

            for ntracks,weights in tuple_ntracks_weights_syst :
                files = ['2v_from_jets_%s_%dtrack_btags_%s.root' % (year, ntracks, _version), '2v_from_jets_%s_%dtrack_nobtags_%s.root' % (year, ntracks, _version)]
                for fn in files:
                    if not os.path.isfile(fn):
                        raise RuntimeError('%s not found' % fn)

                # for each syst
                cmd = 'mergeTFileServiceHistograms -w %s -i %s -o 2v_from_jets_%s_%dtrack_btag_corrected_%s_%s.root' % (weights, ' '.join(files), year, ntracks, syst, _version)
                print cmd
                os.system(cmd)


####

if __name__ == '__main__':
    main(locals())
