ebins = {
    "MCscaled_2017_3track"        : (0.0073, 0.0086, 0.0329),
    "MCscaled_2017_4track"        : (0.0167, 0.0231, 0.1032),
    "MCscaled_2017_5track"        : (0.0563, 0.1073, 0.3836),
    "MCscaled_2018_3track"        : (0.0082, 0.0079, 0.0365),
    "MCscaled_2018_4track"        : (0.0172, 0.0192, 0.1132),
    "MCscaled_2018_5track"        : (0.0575, 0.0463, 0.2022),
    "MCscaled_2017p8_3track"      : (0.0055, 0.0058, 0.0247),
    "MCscaled_2017p8_4track"      : (0.0121, 0.0148, 0.0779),
    "MCscaled_2017p8_5track"      : (0.0411, 0.0471, 0.1901),
    "MCeffective_2017_3track"     : (0.0110, 0.0128, 0.0488),
    "MCeffective_2017_4track"     : (0.0246, 0.0336, 0.1504),
    "MCeffective_2017_5track"     : (0.0818, 0.1556, 0.5553),
    "MCeffective_2018_3track"     : (0.0153, 0.0146, 0.0683),
    "MCeffective_2018_4track"     : (0.0314, 0.0348, 0.2054),
    "MCeffective_2018_5track"     : (0.1079, 0.0859, 0.3793),
    "MCeffective_2017p8_3track"   : (0.0089, 0.0095, 0.0398),
    "MCeffective_2017p8_4track"   : (0.0192, 0.0235, 0.1233),
    "MCeffective_2017p8_5track"   : (0.0689, 0.0779, 0.3099),
    "data10pc_2017_3track"        : (0.0128, 0.0213, 0.0901),
    "data10pc_2017_4track"        : (0.0227, 0.0483, 0.2491),
    "data10pc_2017_5track"        : (0.0454, 0.1318, 0.4754),
    "data10pc_2018_3track"        : (0.0136, 0.0216, 0.0926),
    "data10pc_2018_4track"        : (0.0252, 0.0508, 0.2652),
    "data10pc_2018_5track"        : (0.0591, 0.1726, 0.6118),
    "data10pc_2017p8_3track"      : (0.0094, 0.0152, 0.0657),
    "data10pc_2017p8_4track"      : (0.0169, 0.0348, 0.1809),
    "data10pc_2017p8_5track"      : (0.0361, 0.1055, 0.3698),
    "data100pc_2017_3track"       : (0.0041, 0.0067, 0.0286),
    "data100pc_2017_4track"       : (0.0073, 0.0154, 0.0791),
    "data100pc_2017_5track"       : (0.0148, 0.0431, 0.1546),
    "data100pc_2018_3track"       : (0.0043, 0.0069, 0.0296),
    "data100pc_2018_4track"       : (0.0080, 0.0162, 0.0834),
    "data100pc_2018_5track"       : (0.0175, 0.0508, 0.1854),
    "data100pc_2017p8_3track"     : (0.0030, 0.0049, 0.0207),
    "data100pc_2017p8_4track"     : (0.0054, 0.0112, 0.0572),
    "data100pc_2017p8_5track"     : (0.0115, 0.0336, 0.1179),
    }

ebins["data100pc_2016_5track"] = (0.02, 0.05, 0.18) # manual entry from last values used in run2_paper1--don't drop this line when pasting the output of __main__.parse

def _ksort(s, o=['MCscaled', 'MCeffective', 'data10pc', 'data100pc', '2017', '2018', '2017p8']):
    s = s.replace('sm_','').split('_')
    try:
        return (o.index(s[0]), o.index(s[1]), s[2][0])
    except ValueError:
        return -1


if __name__ == '__main__':
    import sys

    if 'parse' in sys.argv:
        from DVCode.Tools.ROOTTools import *
        print 'ebins2 = {'
        for fn in sorted([s for s in sys.argv[1:] if s.endswith('.root')], key=_ksort):
            f = ROOT.TFile(fn)
            hn = f.Get('h_2v_dvvc_bins_rmses')
            hd = f.Get('h_true_2v_dvv_norm')
            v = lambda i: hn.GetBinContent(i) / hd.GetBinContent(i)
            name = fn.replace('.root','').replace('sm_','')
            print '    %-30s: (%.4f, %.4f, %.4f),' % ('"%s"' % name, v(1), v(2), v(3))
        print '}'

    elif 'compare' in sys.argv:
        from DVCode.Tools import colors
        from ebins2 import ebins2
        for k in sorted(ebins.keys(), key=_ksort):
            e  = ebins .get(k, (-1,-1,-1))
            e2 = ebins2.get(k, e)
            diff = tuple(b-a for a,b in zip(e,e2))
            mdiff = max(abs(d) for d in diff)
            c = colors.none
            if mdiff > 0.05:
                c = colors.boldred
            elif mdiff > 0.02:
                c = colors.yellow
            print c('%-30s: %7.4f %7.4f %7.4f      %7.4f %7.4f %7.4f       %7.4f %7.4f %7.4f' % ((k,) + e + e2 + diff))
