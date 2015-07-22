#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import ROOT

reconstructed = ['NoCuts', 'TrigSel', 'CleaningFilters', 'OfflineJets', 'PreSel', 'TwoVtxNoCuts', 'TwoVtxGeo2ddist', 'TwoVtxNtracks', 'TwoVtxBs2derr', 'TwoVtxMindrmax', 'TwoVtxMaxdrmax', 'TwoVtxDrmin', 'TwoVtxNjetsntks', 'TwoVtxNtracksptgt3', 'TwoVtxDvv600um']
generated = ['NoCuts', '', '', 'FourJets', 'SumHT', '', 'Geo2ddist', '', '', 'Mindrmax', 'Maxdrmax', '', 'Nquarks2', 'Sumpt200', 'Dvv600um']

samples = '''mfv_neutralino_tau0100um_M0200
mfv_neutralino_tau0100um_M0300
mfv_neutralino_tau0100um_M0400
mfv_neutralino_tau0100um_M0600
mfv_neutralino_tau0100um_M0800
mfv_neutralino_tau0100um_M1000
mfv_neutralino_tau0300um_M0200
mfv_neutralino_tau0300um_M0300
mfv_neutralino_tau0300um_M0400
mfv_neutralino_tau0300um_M0600
mfv_neutralino_tau0300um_M0800
mfv_neutralino_tau0300um_M1000
mfv_neutralino_tau1000um_M0200
mfv_neutralino_tau1000um_M0300
mfv_neutralino_tau1000um_M0400
mfv_neutralino_tau1000um_M0600
mfv_neutralino_tau1000um_M0800
mfv_neutralino_tau1000um_M1000
mfv_neutralino_tau9900um_M0200
mfv_neutralino_tau9900um_M0300
mfv_neutralino_tau9900um_M0400
mfv_neutralino_tau9900um_M0600
mfv_neutralino_tau9900um_M0800
mfv_neutralino_tau9900um_M1000
h2x_1000_350_tau3p5cm
h2x_1000_350_tau35cm
h2x_1000_350_tau350cm
h2x_1000_150_tau1cm
h2x_1000_150_tau10cm
h2x_1000_150_tau100cm
mfv_empirical_uds_tau00300um_M0400
mfv_empirical_uds_tau00300um_M1000
mfv_empirical_uds_tau01000um_M0400
mfv_empirical_uds_tau01000um_M1000
mfv_empirical_uds_tau10000um_M0400
mfv_empirical_uds_tau10000um_M1000
mfv_gluino_tau00300um_M0400
mfv_gluino_tau00300um_M1000
mfv_gluino_tau01000um_M0400
mfv_gluino_tau01000um_M1000
mfv_gluino_tau10000um_M0400
mfv_gluino_tau10000um_M1000
mfv_empirical_udsomemu_tau00300um_M0400
mfv_empirical_udsomemu_tau00300um_M1000
mfv_empirical_udsomemu_tau01000um_M0400
mfv_empirical_udsomemu_tau01000um_M1000
mfv_empirical_udsomemu_tau10000um_M0400
mfv_empirical_udsomemu_tau10000um_M1000
mfv_gluinoviarhad_tau00300um_M0400
mfv_gluinoviarhad_tau00300um_M1000
mfv_gluinoviarhad_tau01000um_M0400
mfv_gluinoviarhad_tau01000um_M1000
mfv_gluinoviarhad_tau10000um_M0400
mfv_gluinoviarhad_tau10000um_M1000'''.split('\n')

matched = []
not_matched = []
for sample in samples:
    print sample
    file = ROOT.TFile('crab/MFVResolutionsV20/%s.root'%sample)
    nevents = file.Get('mfvResolutionsNoCuts/h_gen_dvv').GetEntries()
    print '%26s%26s%10s%10s%10s' % ('reconstructed', 'generated', 'reco eff', 'gen eff', 'gen/reco')
    for i, rec in enumerate(reconstructed):
        rec_hist = file.Get('mfvResolutions%s/h_gen_dvv'%rec)
        rec_eff = rec_hist.GetEntries()/nevents
        rec_err = (rec_eff * (1-rec_eff) / nevents)**0.5
        if generated[i] != '':
            gen_hist = file.Get('mfvGen%s/h_gen_dvv'%generated[i])
            gen_eff = gen_hist.GetEntries()/nevents
            gen_err = (gen_eff * (1-gen_eff) / nevents)**0.5
            gen_rec_div = gen_eff/rec_eff if rec_eff != 0 else 9999
            gen_rec_err = (gen_rec_div * ((rec_err/rec_eff)**2 + (gen_err/gen_eff)**2))**0.5 if rec_eff != 0 and gen_eff != 0 else 9999
            if generated[i] == 'Dvv600um':
                print '%20s%6d%20s%6d%10.3f%10.3f%10.3f%10.3f%10.3f%10.3f\n' % (rec, rec_hist.GetEntries(), generated[i], gen_hist.GetEntries(), rec_eff, gen_eff, gen_rec_div, rec_err, gen_err, gen_rec_err)
                if gen_eff >= 0.8*rec_eff and gen_eff <= 1.2*rec_eff:
                    matched.append(sample)
                else:
                    not_matched.append(sample)
            else:
                print '%20s%6d%20s%6d%10.3f%10.3f%10.3f' % (rec, rec_hist.GetEntries(), generated[i], gen_hist.GetEntries(), rec_eff, gen_eff, gen_rec_div)
        else:
            print '%20s%6d' % (rec, rec_hist.GetEntries())

print 'samples with gen eff within 20% of reco eff:'
for i in matched:
    print '\t', i
print
print 'samples with gen eff NOT within 20% of reco eff:'
for i in not_matched:
    print '\t', i
