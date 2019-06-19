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
            tuple_ntracks_weights                    = (3,'0.830,0.170'), (4,'0.854,0.146'), (5,'0.925,0.075'), (7,'0.832,0.168')
            tuple_ntracks_weights_bcjet_SFs_up       = (3,'0.809,0.191'), (4,'0.833,0.167'), (5,'0.911,0.089'), (7,'0.812,0.188')
            tuple_ntracks_weights_bcjet_SFs_down     = (3,'0.855,0.145'), (4,'0.876,0.124'), (5,'0.939,0.061'), (7,'0.857,0.143')
            tuple_ntracks_weights_ljet_SFs_up        = (3,'0.831,0.169'), (4,'0.854,0.146'), (5,'0.924,0.076'), (7,'0.832,0.168')
            tuple_ntracks_weights_ljet_SFs_down      = (3,'0.832,0.168'), (4,'0.853,0.147'), (5,'0.925,0.075'), (7,'0.834,0.166')
            tuple_ntracks_weights_data               = (3,'0.830,0.170'),
        elif year == '2018' :
            tuple_ntracks_weights                    = (3,'0.860,0.140'), (4,'0.899,0.101'), (5,'0.968,0.032'), (7,'0.861,0.139')
            tuple_ntracks_weights_bcjet_SFs_up       = (3,'0.844,0.156'), (4,'0.886,0.114'), (5,'0.961,0.039'), (7,'0.847,0.153')
            tuple_ntracks_weights_bcjet_SFs_down     = (3,'0.877,0.123'), (4,'0.914,0.086'), (5,'0.976,0.024'), (7,'0.879,0.121')
            tuple_ntracks_weights_ljet_SFs_up        = (3,'0.861,0.139'), (4,'0.901,0.099'), (5,'0.969,0.031'), (7,'0.863,0.137')
            tuple_ntracks_weights_ljet_SFs_down      = (3,'0.859,0.141'), (4,'0.898,0.102'), (5,'0.969,0.031'), (7,'0.861,0.139')
            tuple_ntracks_weights_data               = (3,'0.859,0.141'),
        else :
            print("Unknown year (%s)! Exiting." % year)
            sys.exit()

        # for the f2 variation
        btag_frac_threetrk = float(tuple_ntracks_weights[0][1].split(",")[0])
        btag_frac_fourtrk = float(tuple_ntracks_weights[1][1].split(",")[0])
        btag_frac_fivetrk  = float(tuple_ntracks_weights[2][1].split(",")[0])
        frac_variation = (btag_frac_fivetrk / btag_frac_threetrk) - 1
        frac_variation_var = (btag_frac_fourtrk / btag_frac_threetrk) - 1

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
            weight_btag_up   = min( float(weights.split(",")[0]) * (1.0/(1+frac_variation)*(1+2*frac_variation)), 1)
            weight_nobtag_up = 1-weight_btag_up
            weights_up = '%.3f,%.3f' % (weight_btag_up, weight_nobtag_up)
            cmd = 'mergeTFileServiceHistograms -w %s -i %s -o 2v_from_jets_%s_%dtrack_btag_corrected_vary_3trk_to_5trk_up_%s.root' % (weights_up, ' '.join(files), year, ntracks, _version)
            print cmd
            os.system(cmd)

            # f2 variation down
            weight_btag_down   = min( float(weights.split(",")[0]) * (1.0/(1+frac_variation)*(1+frac_variation_var)), 1)
            weight_nobtag_down = 1-weight_btag_down
            weights_down = '%.3f,%.3f' % (weight_btag_down, weight_nobtag_down)
            cmd = 'mergeTFileServiceHistograms -w %s -i %s -o 2v_from_jets_%s_%dtrack_btag_corrected_vary_3trk_to_5trk_down_%s.root' % (weights_down, ' '.join(files), year, ntracks, _version)
            print cmd
            os.system(cmd)

        # for data
        for ntracks,weights in tuple_ntracks_weights_data :
            files = ['2v_from_jets_data_%s_%dtrack_btags_%s.root' % (year, ntracks, _version), '2v_from_jets_data_%s_%dtrack_nobtags_%s.root' % (year, ntracks, _version)]
            for fn in files:
                if not os.path.isfile(fn):
                    raise RuntimeError('%s not found' % fn)

            cmd = 'mergeTFileServiceHistograms -w %s -i %s -o 2v_from_jets_data_%s_%dtrack_btag_corrected_%s.root' % (weights, ' '.join(files), year, ntracks, _version)
            print cmd
            os.system(cmd)


        # for the SF variations
        for syst in ['vary_bcjet_SFs_up', 'vary_bcjet_SFs_down', 'vary_ljet_SFs_up', 'vary_ljet_SFs_down'] :

            if syst == 'vary_bcjet_SFs_up' : 
                tuple_ntracks_weights_syst = tuple_ntracks_weights_bcjet_SFs_up
            elif syst == 'vary_bcjet_SFs_down' : 
                tuple_ntracks_weights_syst = tuple_ntracks_weights_bcjet_SFs_down
            elif syst == 'vary_ljet_SFs_up' : 
                tuple_ntracks_weights_syst = tuple_ntracks_weights_ljet_SFs_up
            elif syst == 'vary_ljet_SFs_down' : 
                tuple_ntracks_weights_syst = tuple_ntracks_weights_ljet_SFs_down

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
