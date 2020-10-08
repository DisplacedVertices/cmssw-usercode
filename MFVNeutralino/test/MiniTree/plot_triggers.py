from JMTucker.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)

sample = sys.argv[1]
ntk = sys.argv[2]
print sample+", ntk = "+ntk

version = "V27p1m"
year = '2017'
set_style()
ps = plot_saver(plot_dir('trigger_study/trigger_study_%s_ntk%s_%s_%s' % (sample, ntk, version.capitalize(), year)), size=(600,600), root=False, log=True, pdf=False)

fn = 'output_studyNewTriggers/output_studyNewTriggers_ntk%s_%s/%s.root' % (ntk, year, sample)
f = ROOT.TFile(fn)

trigs = ['all'
        #,'HT'
        ,'Bjet'
        ,'DisplacedDijet'
        ,'passDisplacedDijet_failBjet'
        ,'failDisplacedDijet_passBjet'
        ]

colors = [ROOT.kBlack
         #,ROOT.kRed+1
         ,ROOT.kBlue
         ,ROOT.kGreen+2
         ,ROOT.kMagenta
         ,ROOT.kCyan
         ]

markers = [20
          #,4
          ,25
          ,30
          ,26
          ,32
          ]

dbv_hists = []
dbv_coarse_hists = []
dvv_hists = []
dvv_coarse_hists = []

for trig in trigs :
    dbv_hist = f.Get('h_dbv_%s' % trig)
    dbv_coarse_hist = f.Get('h_dbv_%s_coarse' % trig)
    dvv_hist = f.Get('h_dvv_%s' % trig)
    dvv_coarse_hist = f.Get('h_dvv_%s_coarse' % trig)

    dbv_hists.append(dbv_hist)
    dbv_coarse_hists.append(dbv_coarse_hist)
    dvv_hists.append(dvv_hist)
    dvv_coarse_hists.append(dvv_coarse_hist)

# FIXME I probably duplicate some things in plot_all
# that aren't needed, since I implemented it all before
# adding the ratio plots at the bottom of the script
def plot_all(hists, colors, markers, trigs, normalize) :
    leg = ROOT.TLegend(0.45, 0.75, 0.85, 0.95)
    ymax = 0

    for i in xrange(0, len(hists)) :
        hist = hists[i]
        color = colors[i]
        marker = markers[i]
        trig = trigs[i]

        xlabel = "d_{VV} (cm)"
        if "dbv" in hist.GetName() : xlabel = "d_{BV} (cm)"

        hist.SetTitle(';%s;%s' % (xlabel, 'a.u.' if normalize else 'Events'))
        hist.SetLineColor(color)
        hist.SetMarkerColor(color)
        hist.SetMarkerStyle(marker)
        hist.SetLineWidth(2)
        
        move_overflows_into_visible_bins(hist, opt='under over')
        integral = hist.Integral(0, hist.GetNbinsX()+1)
        scaleTo = integral
        if scaleTo == 0 : scaleTo = 1
        if normalize : hist.Scale(1./scaleTo)

        hist.SetStats(0)
        #hist.SetMinimum(0)
        #hist.GetYaxis().SetRangeUser(0,hist.GetMaximum())

        trig_name = trig
        if trig_name == 'all' :
            trig_name = 'passed presel'
        leg.AddEntry(hist, trig_name + ", integral = %.2f" % integral)

        #if i == 0 :
        #    hist.Draw('p')
        #else :
        #    hist.Draw('p same')

        # for the ratio histogram
        hists[i].nice = trig_name + ", integral = %.2f"  % integral

        # for y-axis range
        ymax = max(ymax, hist.GetMaximum())

    leg.SetFillColor(0)
    #leg.Draw()

    tlatex = ROOT.TLatex()
    tlatex.SetTextSize(0.03)
    sample_short_name = sample
    sample_short_name = sample_short_name.replace('_2017','')
    sample_short_name = sample_short_name.replace('_2018','')
    sample_short_name = sample_short_name.replace('mfv_neu_', 'Multijet ')
    sample_short_name = sample_short_name.replace('mfv_stopdbardbar', 'Dijet ')
    hist_title = sample_short_name + ", "
    if normalize :
        hist_title += "normalized to 1"
    else :
        hist_title += "scaled to %s lumi" % year
        if sample_short_name != "background" :
            hist_title += ", #sigma = 1fb"

    hists[0].SetMaximum(ymax*1.05)

    xlabel = "d_{VV} (cm)"
    if "dbv" in hists[0].GetName() : xlabel = "d_{BV} (cm)"
    hists[0].SetTitle('%s;%s;%s' % (hist_title, xlabel, 'a.u.' if normalize else 'Events'))

    #if normalize : ps.save('dvv_normalize')
    #else :         ps.save('dvv')


for hists in [dbv_hists, dbv_coarse_hists, dvv_hists, dvv_coarse_hists] :
    #for normalize in [False, True] :
    for normalize in [False] :
        plot_all(hists, colors, markers, trigs, normalize=normalize)

        if hists == dbv_hists :
            category = "dbv"
        elif hists == dbv_coarse_hists :
            category = "dbv_coarse"
        elif hists == dvv_hists :
            category = "dvv"
        elif hists == dvv_coarse_hists :
            category = "dvv_coarse"

        if normalize :
            ratios_plot("%s_ratio_normalize" % category,hists,ps,res_fit=False,legend=(0.45, 0.73, 0.85, 0.93),draw_normalized=normalize,res_divide_opt={'confint': propagate_ratio, 'force_le_1': False, 'no_zeroes' : True})
        else :
            ratios_plot("%s_ratio" % category          ,hists,ps,res_fit=False,legend=(0.45, 0.73, 0.85, 0.93),draw_normalized=normalize,res_divide_opt={'confint': propagate_ratio, 'force_le_1': False, 'no_zeroes' : True},res_y_range=(0,1))
