from JMTucker.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)

sample = sys.argv[1]
ntk = sys.argv[2]

version = "V27m"
year = '2017'
set_style()
ps = plot_saver(plot_dir('trigger_study/trigger_study_%s_ntk%s_%s_%s' % (sample, ntk, version.capitalize(), year)), size=(600,600), root=False, log=False)

fn = 'myOutput/output_studyNewTriggers_ntk%s_%s/%s.root' % (ntk, year, sample)
f = ROOT.TFile(fn)

trigs = ['all'
        ,'HT'
        ,'Bjet'
        ,'DisplacedDijet'
        #,'passHT_failBjet'
        #,'failHT_passBjet'
        ]

colors = [ROOT.kBlack
         ,ROOT.kRed+1
         ,ROOT.kBlue
         ,ROOT.kGreen+2
         ,ROOT.kMagenta
         ,ROOT.kCyan
         ]

hists = []
for trig in trigs :
    hist = f.Get('h_dvv_%s_coarse' % trig)
    hists.append(hist)

# FIXME I probably duplicate some things in plot_all
# that aren't needed, since I implemented it all before
# adding the ratio plots at the bottom of the script
def plot_all(hists, colors, trigs, normalize) :
    leg = ROOT.TLegend(0.45, 0.60, 0.85, 0.80)

    for i in xrange(0, len(hists)) :
        hist = hists[i]
        color = colors[i]
        trig = trigs[i]

        hist.SetTitle(';d_{VV} (cm);%s' % ('a.u.' if normalize else 'Events'))
        hist.SetLineColor(color)
        hist.SetMarkerColor(color)
        hist.SetLineWidth(2)
        integral = hist.Integral()
        scaleTo = integral
        if scaleTo == 0 : scaleTo = 1
        if normalize : hist.Scale(1./scaleTo)
        hist.SetStats(0)
        hist.SetMinimum(0)
        trig_name = trig
        if trig_name == 'all' :
            trig_name = 'no trigger'
        leg.AddEntry(hist, trig_name + ", integral = %.2f" % integral)

        if i == 0 :
            hist.Draw('p')
            if normalize : hist.GetYaxis().SetRangeUser(0,1)
        else :
            hist.Draw('p same')

        hists[i].nice = trig_name + ", integral = %.2f"  % integral

    leg.SetFillColor(0)
    leg.Draw()

    tlatex = ROOT.TLatex()
    tlatex.SetTextSize(0.03)
    sample_short_name = sample
    sample_short_name = sample_short_name.replace('_2017','')
    sample_short_name = sample_short_name.replace('_2018','')
    sample_short_name = sample_short_name.replace('mfv_neu_', 'Multijet ')
    sample_short_name = sample_short_name.replace('mfv_stopdbardbar', 'Dijet ')
    hists[0].SetTitle('%s, %s;d_{VV} (cm);%s' % (sample_short_name, "normalized to 1" if normalize else "scaled to %s lumi" % year, 'a.u.' if normalize else 'Events'))
    if normalize : ps.save('dvv_normalize')
    else :         ps.save('dvv')


for normalize in [False, True] :
    plot_all(hists, colors, trigs, normalize=normalize)
    sample_short_name = sample
    sample_short_name = sample_short_name.replace('_2017','')
    sample_short_name = sample_short_name.replace('_2018','')
    sample_short_name = sample_short_name.replace('mfv_neu_', 'Multijet ')
    sample_short_name = sample_short_name.replace('mfv_stopdbardbar', 'Dijet ')

    # FIXME I should confirm that these uncertainties are correct
    if normalize :
        ratios_plot("dvv_ratio_normalize",hists,ps,res_fit=False,legend=(0.45, 0.60, 0.85, 0.80),draw_normalized=normalize,res_divide_opt={'confint': propagate_ratio, 'force_le_1': False, 'no_zeroes' : True})
    else :
        ratios_plot("dvv_ratio"          ,hists,ps,res_fit=False,legend=(0.45, 0.60, 0.85, 0.80),draw_normalized=normalize,res_divide_opt={'confint': propagate_ratio, 'force_le_1': False, 'no_zeroes' : True},res_y_range=(0,1))
