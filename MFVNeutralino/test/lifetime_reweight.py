import ROOT
import array
import sys, os, math

#"/uscms/home/joeyr/crabdirs/MiniTreeV27darksectorreview_withGenInfom/mfv_HtoLLPto4j_tau10mm_M1000_450_2017.root"
#in_fname = "/uscms/home/joeyr/crabdirs/MiniTreeV27darksectorreview_withGenInfom/mfv_ZprimetoLLPto4b_tau1mm_M4500_2200_2017.root"

def main() :
    fpath = "/uscms/home/joeyr/crabdirs/MiniTreeV27darksectorreview_withGenInfom"
    os.system("mkdir -p "+fpath+"/reweighted/")

    generated_ctaus = [0.1, 1, 10, 100, 1000, 10000]

    #for model in ["HtoLLP", "ZprimetoLLP"] : 
    for model in ["HtoLLP"] :

        if model == "HtoLLP" :
            all_masses = ["1000_100","1000_450","400_150","400_40","600_250","600_60","800_350","800_80"]
        elif model == "ZprimetoLLP" :
            all_masses = ["1000_100","1000_450","1500_150","1500_700","2000_200","2000_950","2500_1200","2500_250","3000_1450","3000_300","3500_1700","3500_350","4000_1950","4000_400","4500_2200","4500_450"]

        for decay in ["4j", "4b"] :
            for masses in all_masses :
                for year in ["2016", "2017", "2018"] :
                    name_template = "mfv_%sto%s_tauCTAUmm_M%s_%s.root" % (model, decay, masses, year)

                    # get our pairings of low and high ctaus that we'll reweight from
                    for idx in xrange(0, len(generated_ctaus)-1) :
                        gen_ctau_low = generated_ctaus[idx]
                        gen_ctau_high = generated_ctaus[idx+1]

                        # e.g., for 1mm, the initial ctau to weight to is 2mm
                        out_ctau = 2*gen_ctau_low

                        while out_ctau < gen_ctau_high :
                            # do the reweighting! both from e.g. 1mm up to 2mm and from 10mm down to 2mm
                            makeReweightedTree(fpath, name_template, gen_ctau_low, out_ctau)
                            makeReweightedTree(fpath, name_template, gen_ctau_high, out_ctau)

                            # formatting for float value of 0.1mm -> file name string of 0p1mm
                            out_ctau_str = str(out_ctau).replace(".","p")
                            
                            # makeReweightedTree formats the outputs as e.g. "mfv_HtoLLPto4j_tau5from1mm_M1000_450_2017.root", i.e. keeping the string "from" between the output and input ctau, so that we can hadd them here
                            hadded_name = name_template.replace("CTAU", out_ctau_str)
                            hadd_inputs = name_template.replace("CTAU", out_ctau_str+"from*")

                            hadded_name = fpath+"/reweighted/"+hadded_name
                            hadd_inputs = fpath+"/reweighted/"+hadd_inputs

                            os.system("hadd %s %s" % (hadded_name, hadd_inputs) )

                            # e.g. for the 1-10mm range, increment by 1mm
                            out_ctau += gen_ctau_low



def makeReweightedTree(fpath, name_template, in_ctau_mm, out_ctau_mm) :

    debug = True
    apply_gen_filter = True # could do this only if Zprime is in the filename # FIXME do this cleanup, or at least check that it only affects the Zprime samples

    in_ctau_str = str(in_ctau_mm).replace(".","p")
    out_ctau_str = str(out_ctau_mm).replace(".","p")
    
    in_fname = fpath+"/"+name_template.replace("CTAU", in_ctau_str)
    in_file = ROOT.TFile(in_fname, "OPEN")

    out_fname = name_template.replace("CTAU", out_ctau_str+"from"+in_ctau_str)
    print "making %s" % (fpath+"/reweighted/"+out_fname)
    out_file = ROOT.TFile(fpath+"/reweighted/"+out_fname, "RECREATE")
    in_tree = in_file.Get("mfvMiniTree/t")
    nopresel_tree = in_file.Get("mfvMiniTreePreSelEvtFilt/t") # only for custom MiniTrees where we even save events with no vertices, to truly see ctau or count sumw from all events

    # sum of weights for normalizations, must come from the nopresel_tree (i.e. number of events generated, *after* applying any gen filtering)
    sumw = 0
    sumw2 = 0

    # output directory for the tree itself
    out_dir = out_file.mkdir("mfvMiniTree")
    out_dir.cd()
    out_tree = in_tree.CloneTree(0)

    weight_branch = array.array('f', [0])
    out_tree.SetBranchAddress("weight", weight_branch)

    # for debugging purposes
    printed_once = False

    if debug :
        h_input_ctau = ROOT.TH1F("input ctau", "input ctau", 100, 0, 5)
        h_output_ctau = ROOT.TH1F("output ctau", "output ctau", 100, 0, 5)

    for tree in [in_tree, nopresel_tree] :

        fill_output_tree = True
        add_to_sumw = False

        if tree == nopresel_tree :
            fill_output_tree = False
            add_to_sumw = True

        for entry in tree :

            # mostly needed for Zprime samples where Zprime -> qq was accidentally enabled, so the LLP mass is set to 0 GeV
            if apply_gen_filter :
                if entry.gen_lsp_mass[0] < 1 or entry.gen_lsp_mass[1] < 1 : 
                    if not printed_once :
                        print "sample: %s, gen_lsp_mass[0]: %.3f, gen_lsp_mass[1]: %.3f" % (in_fname, entry.gen_lsp_mass[0], entry.gen_lsp_mass[1])
                        printed_once = True
                    continue

            # initialize and set 4-vectors in rest-frame
            rest_tlv1 = ROOT.TLorentzVector() 
            rest_tlv2 = ROOT.TLorentzVector() 
            rest_tlv1.SetPtEtaPhiM(entry.gen_lsp_pt[0], entry.gen_lsp_eta[0], entry.gen_lsp_phi[0], entry.gen_lsp_mass[0])
            rest_tlv2.SetPtEtaPhiM(entry.gen_lsp_pt[1], entry.gen_lsp_eta[1], entry.gen_lsp_phi[1], entry.gen_lsp_mass[1])

            # get the lab frame displacements from beamspot, gen-level PV, and gen-level decay point positions
            lab_disp1 = ((entry.bsx + entry.gen_x[0] - entry.gen_pv_x0) ** 2 + (entry.bsy + entry.gen_y[0] - entry.gen_pv_y0) ** 2 + (entry.bsz + entry.gen_z[0] - entry.gen_pv_z0) ** 2) ** 0.5
            lab_disp2 = ((entry.bsx + entry.gen_x[1] - entry.gen_pv_x0) ** 2 + (entry.bsy + entry.gen_y[1] - entry.gen_pv_y0) ** 2 + (entry.bsz + entry.gen_z[1] - entry.gen_pv_z0) ** 2) ** 0.5

            # compute rest frame "displacement" as ctau = lab_disp / (gamma*beta)
            rest_disp1 = lab_disp1 / rest_tlv1.Gamma() / rest_tlv1.Beta()
            rest_disp2 = lab_disp2 / rest_tlv2.Gamma() / rest_tlv2.Beta()

            # note that the float division by 10. is important, or we could have a bunch of int division here!
            # need to do use cm here since the x/y/z are all in our natural CMS units of cm
            in_ctau_cm  = in_ctau_mm/10. 
            out_ctau_cm = out_ctau_mm/10.

            weight1 = (in_ctau_cm / out_ctau_cm) * math.exp( -(1/out_ctau_cm - 1/in_ctau_cm)*rest_disp1 )
            weight2 = (in_ctau_cm / out_ctau_cm) * math.exp( -(1/out_ctau_cm - 1/in_ctau_cm)*rest_disp2 )

            new_weight = entry.weight * weight1 * weight2

            if add_to_sumw :
                sumw += new_weight
                sumw2 += new_weight**2

                # fill plots of original and output ctau, for testing.
                # only do it here for the nopresel tree, to get the full ctau distribution without any bias from cuts applied
                if debug :
                    #print weight1, weight2, new_weight
                    h_input_ctau.Fill(rest_disp1, entry.weight)
                    h_input_ctau.Fill(rest_disp2, entry.weight)
                    h_output_ctau.Fill(rest_disp1, new_weight)
                    h_output_ctau.Fill(rest_disp2, new_weight)

            if fill_output_tree :
                weight_branch[0] = new_weight
                out_tree.Fill()

    # write out the sumw hist
    sumw_dir = out_file.mkdir("mfvWeight")
    sumw_dir.cd()
    h_sums = in_file.Get("mfvWeight/h_sums").Clone()
    h_sums.Reset()
    # NOTE that we are filling all of the bins identically; this is fine for now since we don't use all of the bins for the limit calculation, but may not be ideal for all uses!
    for ibin in xrange(1, h_sums.GetNbinsX()+1) :
        h_sums.SetBinContent(ibin, sumw)
        h_sums.SetBinError(ibin, math.sqrt(sumw2))
    h_sums.Write()

    # write out the tree
    out_dir.cd()
    out_tree.Write()

    if debug :
        os.system("mkdir -p "+fpath+"/debugging_hists")
        out_hist_file = ROOT.TFile(fpath+"/debugging_hists/hists_"+out_fname, "RECREATE")
        out_hist_file.cd()
        h_input_ctau.Write()
        h_output_ctau.Write()

main()
