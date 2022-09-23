import ROOT

for mydir in ['Fat0', 'Fat2', 'Fat4', 'Skinny0', 'Skinny1', 'Skinny2', 'Skinny3', 'Skinny4', 'Skinny5']:
    presel_array  = []
    trigger_array = []
    for fname in ['mfv_combined.root', 'ggh_combined.root', 'ttbar_2017.root']:
    
        fstring = '/uscms_data/d3/shogan/crab_dirs/HistosV30TmTriBjet' + mydir + '/' + fname

        f = ROOT.TFile(fstring)
        h = f.Get('mfvFilterHistosNoCuts').Get('h_filt_nsurvive')

        presel_array.append(round(h.GetBinContent(2)))
        trigger_array.append(round(h.GetBinContent(13)))

    print mydir, ' ', presel_array, ' ', trigger_array

