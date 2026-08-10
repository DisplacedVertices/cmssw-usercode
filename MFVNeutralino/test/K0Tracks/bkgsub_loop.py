import sys, os
from JMTucker.Tools.ROOTTools import *
set_style()

ROOT.TH1.SetDefaultSumw2()

batch = sys.argv[1]
in_fn = sys.argv[2]
in_bn = os.path.basename(in_fn)
os.system('mkdir %s' % batch)
#print 'mkdir %s' % batch
out_fn = os.path.join(batch, in_bn)
out_f = ROOT.TFile(out_fn, 'recreate') #Alec moved
sample = in_bn.replace('.root', '')

ps = plot_saver(plot_dir('v0bkgsub_%s/%s' % (batch, sample)), size=(600,600))

# fit for s and b using sidebands

in_f = ROOT.TFile(in_fn)
in_f.Get('massall/h_nvtx').Draw()
ps.save('nvtx')
in_f.Get('massall/h_premass').Draw()
ps.save('prefit_mass')

abseta_names = ["abseta_lt1", "abseta_gt1lt1p9", "abseta_gt1p9"]
pt_names = ["pt_gt2lt2p2", "pt_gt2p2lt2p5", "pt_gt2p5lt3", "pt_gt3lt4", "pt_gt4"]
dxy_names = ["dxy_ltp03", "dxy_gtp03ltp06", "dxy_gtp06ltp09", "dxy_gtp09ltp13", "dxy_gtp13ltp17", "dxy_gtp17ltp23", "dxy_gtp23ltp3", "dxy_gtp3", "dbv_gtp2ltp4", "dbv_gtp4ltp6", "dbv_gtp6ltp8", "dbv_gtp8lt1", "dbv_gt1lt1p2", "dbv_gt1p2lt1p4", "dbv_gt1p4lt1p6", "dbv_gt1p6lt1p9"]
#dxy_fit_err_array = [] #commented to account for eta
#dbv_fit_err_array = [] #commented to account for eta
#hbkgloplushi_sum_array = []
#hbkg_sum_array = []
dict_dxy_fit_err_arrays = {}
dict_dbv_fit_err_arrays = {}

for abseta in abseta_names:
    dabseta = out_f.mkdir(abseta)
    dabseta.cd()
    dabseta.pwd()
    if 'lt1' in abseta:
        fit_exclude = 0.480, 0.515
    if 'lt1p9' in abseta:
        fit_exclude = 0.470, 0.525
    if 'gt1p9' in abseta:
        fit_exclude = 0.470, 0.530
    for pt in pt_names:
        dpt = dabseta.mkdir(pt)
        dpt.cd()
        dpt.pwd()
        abseta_pt_dxy_fit_err_array_name = abseta+pt+"dxy_fit_err_array"
        abseta_pt_dbv_fit_err_array_name = abseta+pt+"dbv_fit_err_array"
        abseta_pt_dxy_fit_err_array_values = []
        abseta_pt_dbv_fit_err_array_values = []
 
        for dxy in dxy_names:
            #out_f.pwd()
            #dpt = out_f.mkdir(pt)
            #dpt.cd()
            #dpt.pwd()
            #dpt = out_f.pt
            #dpt.cd()
            #dpt.pwd()
            ddxy = dpt.mkdir(dxy)
            #ddxy.cd()
            ddxy.pwd()

            if 'dxy' in dxy:
                h = in_f.Get('massall/'+abseta+'/'+pt+'/'+dxy+'/h_mass_bin')
            if 'dbv' in dxy:
                h = in_f.Get('massall/'+abseta+'/'+pt+'/'+dxy+'/h_mass_dbvbin')

            # must keep these numbers in sync
            fit_range = 0.400, 0.690
            #fit_range = 0.420, 0.580 #fit range before the mass range was extended in the ntuple
            #fit_exclude = 0.475, 0.525 #probably the optimal general range, but use the above definition in the nested loops to specialize it for each abseta bin

            for n in range(1, h.GetNbinsX()+1):
                if h.GetBinContent(n) == 0:
                    h.SetBinError(n,1)

            npars = 3 # 2 if sample.startswith('ZeroBias') else 3
            while 1:
                def fitfunc(x, p):
                    x = x[0]
                    if x >= fit_exclude[0] and x <= fit_exclude[1]:
                        ROOT.TF1.RejectPoint()
                        return 0.
                    return sum(p[i] * x**i for i in xrange(npars))

                fcn = ROOT.TF1('fcn', fitfunc, fit_range[0], fit_range[1], npars)

                #Alec removed WL and added E to the fit options here
                res = h.Fit(fcn, 'R N S Q E')
                res.Print()

                #Alec commented this out to remove the requirement that the fit parabola be concave down, then added "break"
                #if npars == 3 and fcn.GetParameter(2) > 0:
                #    print 'fit wants positive quadratic term, trying again with linear fit'
                #    npars = 2
                #else:
                #    break
                break

            fit_pars = [fcn.GetParameter(i) for i in xrange(npars)]
            fit_errs = [fcn.GetParError(i) for i in xrange(npars)]

            fdraw = ROOT.TF1('fdraw', 'pol%i' % (npars-1), *fit_range)
            fdraw.SetParameters(*fit_pars)

            full_fit_err = fdraw.IntegralError(fit_range[0], fit_range[1])
            exclude_fit_err = fdraw.IntegralError(fit_exclude[0], fit_exclude[1])
            #Divide errors by the bin width (.005) so the errors are properly the error on the background event count rather than on the integral of the fit function
            if 'dxy' in dxy:
                #dxy_fit_err_array.append(full_fit_err)
                abseta_pt_dxy_fit_err_array_values.append(exclude_fit_err/0.005)
            if 'dbv' in dxy:
                #dbv_fit_err_array.append(full_fit_err)
                abseta_pt_dbv_fit_err_array_values.append(exclude_fit_err/0.005)

            # calc fit residuals
            print('Number of bins in plot:', h.GetNbinsX())
            xax = h.GetXaxis()
            hbkg = ROOT.TH1F('hbkg', h.GetTitle(), h.GetNbinsX(), xax.GetXmin(), xax.GetXmax())
            hres = h.Clone('hres')
            xax = hres.GetXaxis()
            xax.SetRangeUser(*fit_range)
            maxr = 0
            for ibin in xrange(xax.FindBin(fit_range[0]), xax.FindBin(fit_range[1])):
                xlo = xax.GetBinLowEdge(ibin)
                xhi = xax.GetBinLowEdge(ibin+1)
                xmd = (xlo + xhi)/2
                w = xhi - xlo
                c  = hres.GetBinContent(ibin)
                ce = hres.GetBinError(ibin)
                i  = fdraw.Integral(xlo, xhi) / w
                ie = fdraw.IntegralError(xlo, xhi) / w
                r = (i - c) / i
                re = ce / i # (ie**2 + ce**2)**0.5 / i
                hbkg.SetBinContent(ibin, i)
                hbkg.SetBinError(ibin, ie)
                if fit_exclude[0] <= xmd <= fit_exclude[1]:
                    r, re = 0, 0
                #print i, ie, c, ce, r, re
                maxr = max(maxr, abs(r)+re)
                hres.SetBinContent(ibin, r)
                hres.SetBinError(ibin, re)

            h.Draw('hist e')
            h.SetStats(0)
            h.GetXaxis().SetRangeUser(0.28,1.3)
            h.GetYaxis().SetLabelSize(0.025)
            h.GetYaxis().SetTitleOffset(1.5)
            fdraw.Draw('same')

            insert = ROOT.TPad("insert","insert",0.431, 0.671, 0.863, 0.869)
            insert.SetRightMargin(0.01)
            insert.SetLeftMargin(0.15)
            insert.SetTopMargin(0.01)
            insert.SetBottomMargin(0.01)
            insert.Draw()
            insert.cd()
            hres.GetYaxis().SetTitle('fit residual')
            hres.GetYaxis().SetLabelSize(0.065)
            hres.GetXaxis().SetLabelSize(0.065)
            hres.GetYaxis().SetTitleSize(0.08)
            hres.GetXaxis().SetTitleSize(0.08)
            hres.GetYaxis().SetTitleOffset(0.75)
            hres.GetYaxis().SetRangeUser(-maxr*1.05, maxr*1.05)
            hres.SetStats(0)
            hres.Fit('pol1')
            ps.c.cd()
            ps.save('mass_fit')
            del insert

            # scan mass window for best yield, purity, and significance z = s/sqrt(b + sigb^2)
            # -- but mass window is now fixed in histos to 490-505 MeV, so if you want to change it you have to do it there and rerun hists
            class do(object):
                xax = h.GetXaxis()
                ibinc = xax.FindBin(0.4976)
                def __init__(self,lo,hi,prnt=False):
                    ibinlo = self.ibinc - lo
                    ibinhi = self.ibinc + hi
                    xlo = self.xax.GetBinLowEdge(ibinlo)
                    xhi = self.xax.GetBinLowEdge(ibinhi+1)
                    ne, be = ROOT.Double(), ROOT.Double()
                    n = h.IntegralAndError(ibinlo, ibinhi, ne)
                    b = hbkg.IntegralAndError(ibinlo, ibinhi, be)
                    s = n - b
                    if b<=0:#Alec added
                        b = 1
                    se = (ne**2 + be**2)**0.5
                    z = s / (b + be**2)**0.5
                    p = s/n
                    if prnt:
                        print('%.3f-%.3f: %10.1f +- %5.1f  %10.1f +- %5.1f  %10.1f +- %5.1f : %5.2f : %5.1f' % (xlo, xhi, n, ne, b, be, s, se, p, z))
                    for X in 'xlo xhi n ne b be s se p z'.split():
                        setattr(self, X, eval(X))

            max_s, max_p, max_z = 0, 0, 0
            for lo in xrange(50):
                for hi in xrange(50):
                    d = do(lo,hi)
                    if (d.s > max_s or d.p > max_p or d.z > max_z) and d.p >= 0.85:
                        do(lo,hi,True)
                    if d.s > max_s:
                        max_s = d.s
                    if d.p > max_p:
                        max_p = d.p
                    if d.z > max_z:
                        max_z = d.z
            print
            the_d = do(1,1, True) # print the one we're using
            #print 'performed fit for:'
            #print pt
            #print dxy
            assert abs(the_d.xlo-0.490) < 1e-5 and abs(the_d.xhi-0.505) < 1e-5 # check that we're in sync with histos

            #out_f = ROOT.TFile(out_fn, 'recreate')

            def is_th2(h):
                return issubclass(type(h), ROOT.TH2)

            def integ(h):
                if is_th2(h):
                    return h.Integral(0,h.GetNbinsX()+2,0,h.GetNbinsY()+2)
                else:
                    return h.Integral(0,h.GetNbinsX()+2)

            # do the bkg subtraction in whatever variables you want as long as the hists exist
            # written out to file in folders so the cmp script can do the rest

            scans = False
            if "dxy" in dxy:
                variables = [
                    ('h_mass_bin',1, 1, None, -1),
                    #('h_chi2dof', 1, 1, None, -1),
                    #('h_rho', 1, 1, None, 1),
                    #('h_dbv', 1, 1, None, 1),
                    #('h_ct', 1, 1, None, 1),
                    #('h_ctau', 1, 1, None, 1),
                    #('h_p', 1, 1, None, -1),
                    #('h_pt', 1, 1, None, -1),
                    #('h_eta', 1, 1, None, 0),
                    #('h_phi', 1, 1, None, 0),
                    #('h_deltazpv', 1, 1, None, -1),
                    #('h_costh3', 1, 1, None, 1),
                    #('h_costh2', 1, 1, None, 1),
                    #('h_trackdeltaz', 1, 1, None, -1),
                    #('h_tracks_pt', 2, 1, None, 0),
                    #('h_tracks_eta', 2, 1, None, 0),
                    #('h_tracks_phi', 2, 1, None, 0),
                    #('h_tracks_dxy', 2, 1, None, 0),
                    #('h_tracks_absdxy', 2, 1, None, 0),
                    #('h_tracks_dz', 2, 1, None, 0),
                    #('h_tracks_dzpv', 2, 1, None, 0),
                    #('h_tracks_dxyerr', 2, 1, None, 0),
                    #('h_tracks_dszerr', 2, 1, None, 0),
                    #('h_tracks_nsigmadxy', 2, 1, None, 0),
                    #('h_tracks_npxlayers', 2, 1, None, 0),
                    #('h_tracks_nstlayers', 2, 1, None, 0),
                    #('h_tracks_dxyerr_v_pt', 2, None, (0, 40), 0),
                    #('h_dbv_v_pt', 1, None, None, 0),
                    #('h_tracks_absdxy_v_pt', 2, 1, None, 1),
                    #('h_tracks_absdxy_v_alphapt', 2, None, None, 1)
                    #('h_ptgt2lt5_dxygtp02ltp1_maxtracks_absdxy_v_alphapt', 2, None, None, 1)
                    ]
            if "dbv" in dxy:
                variables = [
                    ('h_mass_dbvbin',1, 1, None, -1),
                ]

            for hname, integ_factor, rebin, x_range, scan_dir in variables:
                #hon = in_f.Get('masson/'+pt+'/'+dxy+'/%s' % hname)
                #hbkglo = in_f.Get('masslo/'+pt+'/'+dxy+'/%s' % hname)
                #hbkghi = in_f.Get('masshi/'+pt+'/'+dxy+'/%s' % hname)
                hon = in_f.Get('masson/%s/%s/%s/%s' % (abseta, pt, dxy, hname))
                hbkglo = in_f.Get('masslo/%s/%s/%s/%s' % (abseta, pt, dxy, hname))
                hbkghi = in_f.Get('masshi/%s/%s/%s/%s' % (abseta, pt, dxy, hname))
                hall = in_f.Get('massall/%s/%s/%s/%s' % (abseta, pt, dxy, hname))

                #d = out_f.mkdir(pt+'/'+dxy+'/'+hname)
                #d = out_f.mkdir('%s/%s/%s' % (pt, dxy, hname)) 
                #dpt = out_f.mkdir(pt)
                #dpt.cd()
                #ddxy = dpt.mkdir(dxy)
                #ddxy.cd()
                d = ddxy.mkdir(hname)
                print('saved output file for:')
                print(abseta+'/'+pt+'/'+dxy+'/'+hname)
                d.cd()
                d.pwd()
                hon = hon.Clone('hon')
                hbkglo = hbkglo.Clone('hbkglo')
                hbkghi = hbkghi.Clone('hbkghi')
                if "h_mass" in hname:
                    hsig = hall.Clone('hsig')
                    hsig.SetBinContent(116,0)
                    hsig.Add(hbkg, -1)
                    print('Using mass plot background fit as the background to subtract')

                    #hbkgloplushi = hbkglo.Clone('hbkgloplushi')
                    #hbkgloplushi.Add(hbkghi)
                    #hbkgloplushi_sum = 0
                    #hbkg_sum = 0
                    #for ibin in xrange(xax.FindBin(fit_range[0]), xax.FindBin(fit_range[1])):
                    #    hbkgloplushi_sum += hbkgloplushi.GetBinContent(ibin)
                    #    hbkg_sum += hbkg.GetBinContent(ibin)
                    #hbkgloplushi_sum_array.append(hbkgloplushi_sum)
                    #hbkg_sum_array.append(hbkg_sum)
                else:
                    hbkg = hbkglo.Clone('hbkg')
                    hbkg.Add(hbkghi)
                    hsig = hon.Clone('hsig')
                    hbkg.Scale(the_d.b / integ(hbkg))
                    hsig.Add(hbkg, -1) 
                    print('Using mass range to roughly extract the background to subtract')
                #hsig = hon.Clone('hsig')

                #if abs(integ(hon) - integ_factor * the_d.n) > 1e-5:
                #    raise ValueError('hint %s n %s' % (hint, the_d.n))

                #hbkg.Scale(the_d.b / integ(hbkg))
                #hsig.Add(hbkg, -1)
 
                for h,c in zip((hon, hbkg, hsig), (1, 4, 2)):
                    h.SetLineColor(c)
                    h.SetLineWidth(2)
                    h.SetStats(0)
                    if rebin:
                        h.Rebin(rebin)
                    if not is_th2(h) and x_range:
                        h.GetXaxis().SetRangeUser(*x_range)

                if is_th2(hon):
                    #p_hon, p_hbkg, p_hsig = pfs = [h.ProfileX() for h in hon, hbkg, hsig]
                    for h in hon, hbkg, hsig:
                        p_hon, p_hbkg, p_hsig = pfs = h.ProfileX()
                    for p in pfs:
                        p.SetLineWidth(2)
                        p.SetStats(0)
                        if x_range:
                            p.GetXaxis().SetRangeUser(*x_range)
                    p_hon.Draw('hist')
                    p_hbkg.Draw('hist same')
                    p_hsig.Draw('hist same')
                else:
                    hon.Draw('hist e')
                    hbkg.Draw('hist e same')
                    hsig.Draw('hist e same')

                ps.save(hname)

                if scans and scan_dir:
                    #hsig_cumu, hbkg_cumu = [cumulative_histogram(h, 'ge' if scan_dir == 1 else 'le') for h in hsig, hbkg]
                    for h in hsig, hbkg:
                        hsig_cumu, hbkg_cumu = cumulative_histogram(h, 'ge' if scan_dir == 1 else 'le')
                    print(hname)
                    max_z = 0
                    for ibin in xrange(1, hsig.GetNbinsX()+1):
                        s = hsig_cumu.GetBinContent(ibin)
                        b = hbkg_cumu.GetBinContent(ibin)
                        be = hbkg_cumu.GetBinError(ibin)
                        if b > 0 and s+b > 0:
                            p = s/(s+b)
                            z = s/(b + be**2)**0.5
                            print('%7.5f' % hsig.GetXaxis().GetBinLowEdge(ibin), 's = %10.1f (%.3f)' % (s, s/the_d.s), 'b = %10.1f +- %6.1f (%.3f)' % (b,be,b/the_d.b), 'p = %.3f' % p, 'z = %4.1f' % z)

                for h in hon, hbkg, hsig:
                    h.Write()

            # copy over normalization hist
            h = in_f.Get('mfvWeight/h_sums').Clone('h_sums')
            h.SetDirectory(out_f.mkdir('mfvWeight'))

        dict_dxy_fit_err_arrays[abseta_pt_dxy_fit_err_array_name] = abseta_pt_dxy_fit_err_array_values
        dict_dbv_fit_err_arrays[abseta_pt_dbv_fit_err_array_name] = abseta_pt_dbv_fit_err_array_values
        #out_f.Write()

#print('Fit uncertainty of each pt/dxy bin: ', dxy_fit_err_array)
#print('Fit uncertainty of each pt/dbv bin: ', dbv_fit_err_array)
#print('hbkgloplushi_sum_array:', hbkgloplushi_sum_array)
#print('hbkg_sum_array:', hbkg_sum_array)

for abseta in abseta_names:
    for pt in pt_names:
        print(abseta, " ", pt , " : ", dict_dxy_fit_err_arrays[abseta+pt+"dxy_fit_err_array"])

for abseta in abseta_names:
    for pt in pt_names:
        print(abseta, " ", pt , " : ", dict_dbv_fit_err_arrays[abseta+pt+"dbv_fit_err_array"])

out_f.Close()
