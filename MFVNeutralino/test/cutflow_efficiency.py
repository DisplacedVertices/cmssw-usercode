#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import ROOT
from array import array

gen_eff_cut = 15
gen_rec_cut = 20

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
h2x_1000_tau0035000um_M0350
h2x_1000_tau0350000um_M0350
h2x_1000_tau3500000um_M0350
h2x_1000_tau0010000um_M0150
h2x_1000_tau0100000um_M0150
h2x_1000_tau1000000um_M0150
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
mfv_gluinoviarhad_tau10000um_M1000
mfv_gluinoviarhad_ddbar_tau00300um_M0400
mfv_gluinoviarhad_ddbar_tau00300um_M1000
mfv_gluinoviarhad_ddbar_tau01000um_M0400
mfv_gluinoviarhad_ddbar_tau01000um_M1000
mfv_gluinoviarhad_ddbar_tau10000um_M0400
mfv_gluinoviarhad_ddbar_tau10000um_M1000
mfv_gluinoviarhad_bbbar_tau00300um_M0400
mfv_gluinoviarhad_bbbar_tau00300um_M1000
mfv_gluinoviarhad_bbbar_tau01000um_M0400
mfv_gluinoviarhad_bbbar_tau01000um_M1000
mfv_gluinoviarhad_bbbar_tau10000um_M0400
mfv_gluinoviarhad_bbbar_tau10000um_M1000'''.split('\n')

sampleNames = r'''$\tilde{N} \rightarrow tbs$,      $\tau = 100~\mum$, $M =  200~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau = 100~\mum$, $M =  300~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau = 100~\mum$, $M =  400~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau = 100~\mum$, $M =  600~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau = 100~\mum$, $M =  800~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau = 100~\mum$, $M = 1000~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau = 300~\mum$, $M =  200~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau = 300~\mum$, $M =  300~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau = 300~\mum$, $M =  400~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau = 300~\mum$, $M =  600~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau = 300~\mum$, $M =  800~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau = 300~\mum$, $M = 1000~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau =    1~\mm$, $M =  200~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau =    1~\mm$, $M =  300~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau =    1~\mm$, $M =  400~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau =    1~\mm$, $M =  600~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau =    1~\mm$, $M =  800~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau =    1~\mm$, $M = 1000~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau =  9.9~\mm$, $M =  200~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau =  9.9~\mm$, $M =  300~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau =  9.9~\mm$, $M =  400~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau =  9.9~\mm$, $M =  600~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau =  9.9~\mm$, $M =  800~\GeV$
$\tilde{N} \rightarrow tbs$,      $\tau =  9.9~\mm$, $M = 1000~\GeV$
 $X^0 \rightarrow q\bar{q}$,      $\tau =  3.5~\cm$, $M =  350~\GeV$
 $X^0 \rightarrow q\bar{q}$,      $\tau =   35~\cm$, $M =  350~\GeV$
 $X^0 \rightarrow q\bar{q}$,      $\tau =  350~\cm$, $M =  350~\GeV$
 $X^0 \rightarrow q\bar{q}$,      $\tau =    1~\cm$, $M =  150~\GeV$
 $X^0 \rightarrow q\bar{q}$,      $\tau =   10~\cm$, $M =  150~\GeV$
 $X^0 \rightarrow q\bar{q}$,      $\tau =  100~\cm$, $M =  150~\GeV$
$\tilde{N} \rightarrow uds$,      $\tau = 300~\mum$, $M =  400~\GeV$
$\tilde{N} \rightarrow uds$,      $\tau = 300~\mum$, $M = 1000~\GeV$
$\tilde{N} \rightarrow uds$,      $\tau =    1~\mm$, $M =  400~\GeV$
$\tilde{N} \rightarrow uds$,      $\tau =    1~\mm$, $M = 1000~\GeV$
$\tilde{N} \rightarrow uds$,      $\tau =    1~\cm$, $M =  400~\GeV$
$\tilde{N} \rightarrow uds$,      $\tau =    1~\cm$, $M = 1000~\GeV$
$\tilde{g} \rightarrow tbs$,      $\tau = 300~\mum$, $M =  400~\GeV$
$\tilde{g} \rightarrow tbs$,      $\tau = 300~\mum$, $M = 1000~\GeV$
$\tilde{g} \rightarrow tbs$,      $\tau =    1~\mm$, $M =  400~\GeV$
$\tilde{g} \rightarrow tbs$,      $\tau =    1~\mm$, $M = 1000~\GeV$
$\tilde{g} \rightarrow tbs$,      $\tau =    1~\cm$, $M =  400~\GeV$
$\tilde{g} \rightarrow tbs$,      $\tau =    1~\cm$, $M = 1000~\GeV$
$\tilde{N} \rightarrow ud\mu$,    $\tau = 300~\mum$, $M =  400~\GeV$
$\tilde{N} \rightarrow ud\mu$,    $\tau = 300~\mum$, $M = 1000~\GeV$
$\tilde{N} \rightarrow ud\mu$,    $\tau =    1~\mm$, $M =  400~\GeV$
$\tilde{N} \rightarrow ud\mu$,    $\tau =    1~\mm$, $M = 1000~\GeV$
$\tilde{N} \rightarrow ud\mu$,    $\tau =    1~\cm$, $M =  400~\GeV$
$\tilde{N} \rightarrow ud\mu$,    $\tau =    1~\cm$, $M = 1000~\GeV$
$\tilde{g} \rightarrow tbs$,      $\tau = 300~\mum$, $M =  400~\GeV$
$\tilde{g} \rightarrow tbs$,      $\tau = 300~\mum$, $M = 1000~\GeV$
$\tilde{g} \rightarrow tbs$,      $\tau =    1~\mm$, $M =  400~\GeV$
$\tilde{g} \rightarrow tbs$,      $\tau =    1~\mm$, $M = 1000~\GeV$
$\tilde{g} \rightarrow tbs$,      $\tau =    1~\cm$, $M =  400~\GeV$
$\tilde{g} \rightarrow tbs$,      $\tau =    1~\cm$, $M = 1000~\GeV$
$\tilde{g} \rightarrow d\bar{d}$, $\tau = 300~\mum$, $M =  400~\GeV$
$\tilde{g} \rightarrow d\bar{d}$, $\tau = 300~\mum$, $M = 1000~\GeV$
$\tilde{g} \rightarrow d\bar{d}$, $\tau =    1~\mm$, $M =  400~\GeV$
$\tilde{g} \rightarrow d\bar{d}$, $\tau =    1~\mm$, $M = 1000~\GeV$
$\tilde{g} \rightarrow d\bar{d}$, $\tau =    1~\cm$, $M =  400~\GeV$
$\tilde{g} \rightarrow d\bar{d}$, $\tau =    1~\cm$, $M = 1000~\GeV$
$\tilde{g} \rightarrow b\bar{b}$, $\tau = 300~\mum$, $M =  400~\GeV$
$\tilde{g} \rightarrow b\bar{b}$, $\tau = 300~\mum$, $M = 1000~\GeV$
$\tilde{g} \rightarrow b\bar{b}$, $\tau =    1~\mm$, $M =  400~\GeV$
$\tilde{g} \rightarrow b\bar{b}$, $\tau =    1~\mm$, $M = 1000~\GeV$
$\tilde{g} \rightarrow b\bar{b}$, $\tau =    1~\cm$, $M =  400~\GeV$
$\tilde{g} \rightarrow b\bar{b}$, $\tau =    1~\cm$, $M = 1000~\GeV$'''.split('\n')

def style(sample):
    model = sample.split('_tau')[0]
    if model == 'mfv_neutralino':
        return 20
    if model == 'h2x_1000':
        return 21
    if model == 'mfv_empirical_uds':
        return 22
    if model == 'mfv_gluino':
        return 23
    if model == 'mfv_empirical_udsomemu':
        return 24
    if model == 'mfv_gluinoviarhad':
        return 29
    if model == 'mfv_gluinoviarhad_ddbar':
        return 33
    if model == 'mfv_gluinoviarhad_bbbar':
        return 34

def color(sample):
    mass = sample.split('M')[1]
    if mass == '0150':
        return 1
    if mass == '0200':
        return 2
    if mass == '0300':
        return 3
    if mass == '0350':
        return 4
    if mass == '0400':
        return 6
    if mass == '0600':
        return 7
    if mass == '0800':
        return 8
    if mass == '1000':
        return 9

matched = []
not_matched = []
x = []
y = []
gs = []
l = ROOT.TLegend(0.75,0.1,0.95,0.9)
for j,sample in enumerate(samples):
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
                print r'%s & $%4.3f \pm %4.3f$ & $%4.3f \pm %4.3f$ & $%4.3f \pm %4.3f$ \\' % (sampleNames[j], rec_eff, rec_err, gen_eff, gen_err, gen_rec_div, gen_rec_err)
                if gen_eff > 0.01*gen_eff_cut:
                    x.append(int(sample.split('tau')[1].split('um')[0]))
                    y.append(gen_rec_div)
                    g = ROOT.TGraph(1, array('d', [int(sample.split('tau')[1].split('um')[0])]), array('d', [gen_rec_div]))
                    g.SetMarkerStyle(style(sample))
                    g.SetMarkerColor(color(sample))
                    gs.append(g)
                    label = sampleNames[j].split(',')[0] + sampleNames[j].split(',')[2]
                    label = label.replace('\\','#').replace('~#GeV',' GeV').replace('$','').replace(' M',', M')
                    l.AddEntry(g, label, 'P')
                if gen_eff >= (1-0.01*gen_rec_cut)*rec_eff and gen_eff <= (1+0.01*gen_rec_cut)*rec_eff:
                    matched.append(sample)
                else:
                    not_matched.append(sample)
            else:
                print '%20s%6d%20s%6d%10.3f%10.3f%10.3f' % (rec, rec_hist.GetEntries(), generated[i], gen_hist.GetEntries(), rec_eff, gen_eff, gen_rec_div)
        else:
            print '%20s%6d' % (rec, rec_hist.GetEntries())

print 'samples with gen eff within %s%% of reco eff:' % gen_rec_cut
for i in matched:
    print '\t', i
print
print 'samples with gen eff NOT within %s%% of reco eff:' % gen_rec_cut
for i in not_matched:
    print '\t', i

c = ROOT.TCanvas()
c.SetRightMargin(0.3)
g_all = ROOT.TGraph(len(x), array('d', x), array('d', y))
g_all.SetTitle(';c#tau (#mum);gen. eff. / reco. eff.')
g_all.Draw('AP')
for g in gs:
    g.Draw('P')
l.SetFillColor(0)
l.Draw()
c.SaveAs('plots/theorist_recipe/gen_vs_reco_eff.pdf')
