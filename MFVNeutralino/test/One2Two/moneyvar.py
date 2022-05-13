import ROOT
import numpy as np
import scipy.stats as stats

# Always use the same template file
f_c = ROOT.TFile('2v_from_jets_mc_2017_5track_default_V27m.root')

# Loop over M0600 files
for ctau in ['000300', '001000', '010000']:
    mc_name = 'mfv_neu_tau' + ctau + 'um_M0800_2017.root'
    print mc_name + '\n----------------------------------\n'

    f_m = ROOT.TFile('/uscms_data/d3/shogan/crab_dirs/HistosV28Bm/' + mc_name)

    # Loop over the three money variables: dVV, sum_dBV, sqsum_dBV
    for mvars in [['h_c1v_dvv', 'h_svdist2d', 'dVV'], ['h_c1v_sumdbv', 'h_sum_bsbs2ddist', 'sum_dBV'], ['h_c1v_sqsumdbv', 'h_sqsum_bsbs2ddist', 'sqsum_dBV']]:

        dvv_c = f_c.Get(mvars[0])
        dvv_m = f_m.Get("mfvVertexHistosFullSel").Get(mvars[1])

        dvv_c.Scale(1.0/dvv_c.Integral())
        dvv_m.Scale(1.0/dvv_m.Integral())
        
        # begin calculating the EMD
        mpl_c = np.array([])
        mpl_m = np.array([])
        mpl_x = np.array([])
        
        nbins = dvv_m.GetNbinsX()
        integral = 0.0
        
        for i in range(1, nbins):
            tmp_c = dvv_c.GetBinContent(i)
            tmp_m = dvv_m.GetBinContent(i)
            integral += min(tmp_c, tmp_m)
            
            mpl_x = np.append(mpl_x, dvv_m.GetBinCenter(i))
            mpl_c = np.append(mpl_c, tmp_c)
            mpl_m = np.append(mpl_m, tmp_m)
            
        earth_mover_distance = 100 * stats.wasserstein_distance(mpl_x, mpl_x, mpl_c, mpl_m)
        print '%10s :   %.2f' % (mvars[2], earth_mover_distance)
