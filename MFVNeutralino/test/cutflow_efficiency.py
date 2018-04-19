#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import ROOT, to_array, clopper_pearson
from JMTucker.Tools import Samples, colors

file_path = '/uscms_data/d3/jchu/crab_dirs/mfv_8025/TheoristRecipeV44'
plot_path = 'plots/theorist_recipe' # plot_dir()!!!
save_plot = False

gen_rec_cut = 20

match = ''
#match = '_match'

ctau = ''
#ctau = 'tau00100um'
#ctau = 'tau00300um'
#ctau = 'tau01000um'
#ctau = 'tau10000um'
#ctau = 'tau30000um'

#gen_num = 'FourJets'
#gen_num = 'HT40'
#gen_num = 'Bsbs2ddist'
#gen_num = 'Geo2ddist'
#gen_num = 'Sumpt350'
gen_num = 'Dvv400um'

rec_den = 'NoCuts'
gen_den = 'NoCuts'
iden = 0

#rec_den = 'OfflineJets'
#gen_den = 'FourJets'
#iden = 1

#rec_den = 'PreSel'
#gen_den = 'HT40'
#iden = 3

#rec_den = 'TwoVtxBsbs2ddist'
#gen_den = 'Bsbs2ddist'
#iden = 5

#rec_den = 'TwoVtxGeo2ddist'
#gen_den = 'Geo2ddist'
#iden = 6

#rec_den = 'TwoVtxBs2derr'
#gen_den = 'Sumpt350'
#iden = 8

reconstructed = ['NoCuts', 'OfflineJets', 'TrigSel', 'PreSel', 'TwoVtxNoCuts', 'TwoVtxBsbs2ddist', 'TwoVtxGeo2ddist', 'TwoVtxNtracks', 'TwoVtxBs2derr', 'TwoVtxDvv400um']
generated = ['NoCuts', 'FourJets', '', 'HT40', '', 'Bsbs2ddist', 'Geo2ddist', '', 'Sumpt350', 'Dvv400um']

samples = Samples.mfv_signal_samples + Samples.mfv_stopdbardbar_samples + Samples.mfv_stopbbarbbar_samples + Samples.mfv_xxddbar_samples + Samples.mfv_neuuds_samples + Samples.mfv_neuudmu_samples + Samples.mfv_neuude_samples + Samples.mfv_misc_samples
#samples = Samples.all_signal_samples

def style(sample):
    model = sample.model
    if model == 'mfv_neu':
        return 20
    elif model == 'mfv_stopdbardbar':
        return 22
    elif model == 'mfv_stopbbarbbar':
        return 23
    elif model == 'mfv_xxddbar':
        return 33
    elif model == 'mfv_neuuds':
        return 21
    elif model == 'mfv_neuudmu':
        return 34
    elif model == 'mfv_neuude':
        return 29
    elif model == 'mfv_neucdb':
        return 27
    elif model == 'mfv_neucds':
        return 26
    elif model == 'mfv_neutbb':
        return 32
    elif model == 'mfv_neutds':
        return 24
    elif model == 'mfv_neuubb':
        return 25
    elif model == 'mfv_neuudb':
        return 30
    elif model == 'mfv_neuudtu':
        return 28

def color(sample):
    mass = sample.mass
    if mass == 300:
        return 1
    elif mass == 400:
        return 2
    elif mass == 500:
        return 3
    elif mass == 600:
        return 4
    elif mass == 800:
        return 6
    elif mass == 1200:
        return 7
    elif mass == 1600:
        return 8
    elif mass == 3000:
        return 9

matched = []
not_matched = []
x = []
y = []
ex = []
ey = []
gs = []
l1 = ROOT.TLegend(0.75,0.1,0.95,0.5)
l2 = ROOT.TLegend(0.75,0.5,0.95,0.9)
for sample in samples:
    if ctau not in sample.name:
        continue

    fn = os.path.join(os.path.expanduser(file_path), '%s.root' % sample.name)
    if not os.path.isfile(fn):
        print colors.red('%s is missing' % fn) + '\n'
        continue

    print sample.name

    f = ROOT.TFile(fn)
    nrec = f.Get('mfvTheoristRecipe%s/h_gen%s_dvv' % (rec_den, match)).GetEntries()
    ngen = f.Get('mfvGen%s/h_gen%s_dvv' % (gen_den, match)).GetEntries()
    print '%26s%26s%20s%20s%20s' % ('reconstructed', 'generated', 'reco eff +/- error', 'gen eff +/- error', 'gen/reco +/- error')
    for i, rec in enumerate(reconstructed):
        if i < iden:
            continue
        rec_hist = f.Get('mfvTheoristRecipe%s/h_gen%s_dvv' % (rec, match))
        rec_eff,l,u = clopper_pearson(rec_hist.GetEntries(), nrec)
        rec_err = (u-l)/2
        if generated[i] != '':
            gen_hist = f.Get('mfvGen%s/h_gen%s_dvv' % (generated[i], match))
            gen_eff,l,u = clopper_pearson(gen_hist.GetEntries(), ngen)
            gen_err = (u-l)/2
            gen_rec_div = gen_eff/rec_eff if rec_eff != 0 else 9999
            gen_rec_err = (gen_rec_div * ((rec_err/rec_eff)**2 + (gen_err/gen_eff)**2))**0.5 if rec_eff != 0 and gen_eff != 0 else 9999
            if generated[i] == gen_num:
                print '%20s%6d%20s%6d%10.3f%10.3f%10.3f%10.3f%10.3f%10.3f\n' % (rec, rec_hist.GetEntries(), generated[i], gen_hist.GetEntries(), rec_eff, rec_err, gen_eff, gen_err, gen_rec_div, gen_rec_err)
                print r'%s & $%4.3f \pm %4.3f$ & $%4.3f \pm %4.3f$ & $%4.3f \pm %4.3f$ \\' % (sample.latex, rec_eff, rec_err, gen_eff, gen_err, gen_rec_div, gen_rec_err)
                x.append(rec_eff)
                y.append(gen_eff)
                ex.append(rec_err)
                ey.append(gen_err)
                g = ROOT.TGraphErrors(1, to_array(rec_eff), to_array(gen_eff), to_array(rec_err), to_array(gen_err))
                g.SetMarkerStyle(style(sample))
                g.SetMarkerColor(color(sample))
                gs.append(g)
                label = sample.latex.split(',')[0] + sample.latex.split(',')[2]
                label = label.replace('\\','#').replace('#GeV',' GeV').replace('$','').replace(' M',', M')
                if sample.tau == 1000 or ctau != '':
                    if style(sample) == 20:
                        l1.AddEntry(g, label.split(', ')[1], 'P')
                    if color(sample) == 6:
                        l2.AddEntry(g, label.split(', ')[0], 'P')
                if gen_eff >= (1-0.01*gen_rec_cut)*rec_eff and gen_eff <= (1+0.01*gen_rec_cut)*rec_eff:
                    matched.append(sample.name)
                else:
                    not_matched.append(sample.name)
                break
            else:
                print '%20s%6d%20s%6d%10.3f%10.3f%10.3f%10.3f%10.3f%10.3f' % (rec, rec_hist.GetEntries(), generated[i], gen_hist.GetEntries(), rec_eff, rec_err, gen_eff, gen_err, gen_rec_div, gen_rec_err)
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
c.SetTickx()
c.SetTicky()
c.SetRightMargin(0.3)
g_all = ROOT.TGraphErrors(len(x), to_array(x), to_array(y), to_array(ex), to_array(ey))
g_all.SetTitle(';reconstructed-level efficiency;generator-level efficiency')
g_all.GetXaxis().SetLimits(0,1)
g_all.GetHistogram().GetYaxis().SetRangeUser(0,1)
g_all.Draw('AP')
for g in gs:
    g.Draw('P')
l1.SetFillColor(0)
l1.Draw()
l2.SetFillColor(0)
l2.Draw()
line0 = ROOT.TLine(0,0,1,1)
line0.SetLineStyle(7)
line1 = ROOT.TLine(0,0,1,1-0.01*gen_rec_cut)
line2 = ROOT.TLine(0,0,1-0.01*gen_rec_cut,1)
line0.Draw()
line1.Draw()
line2.Draw()
if save_plot:
    c.SaveAs(os.path.join(plot_path, 'gen_vs_reco_eff_%s_divide_%s%s%s.pdf' % (gen_num, gen_den, '' if ctau == '' else '_%s'%ctau, match)))
