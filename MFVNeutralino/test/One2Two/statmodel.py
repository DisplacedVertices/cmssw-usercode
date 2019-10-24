ebins = {'MCscaled_2017_3track':       (0.0072, 0.0083, 0.0340),
         'MCscaled_2017_4track':       (0.0158, 0.0232, 0.1156),
         'MCscaled_2017_5track':       (0.0540, 0.1120, 0.4153),
         'MCscaled_2018_3track':       (0.0086, 0.0092, 0.0379),
         'MCscaled_2018_4track':       (0.0176, 0.0237, 0.1194),
         'MCscaled_2018_5track':       (0.0512, 0.0967, 0.3643),
         'MCscaled_2017p8_3track':     (0.0056, 0.0062, 0.0252),
         'MCscaled_2017p8_4track':     (0.0122, 0.0167, 0.0832),
         'MCscaled_2017p8_5track':     (0.0371, 0.0734, 0.2782),
         'MCeffective_2017_3track':    (0.0108, 0.0125, 0.0508),
         'MCeffective_2017_4track':    (0.0236, 0.0341, 0.1672),
         'MCeffective_2017_5track':    (0.0788, 0.1632, 0.5972),
         'MCeffective_2018_3track':    (0.0158, 0.0168, 0.0700),
         'MCeffective_2018_4track':    (0.0322, 0.0429, 0.2182),
         'MCeffective_2018_5track':    (0.0957, 0.1774, 0.6730),
         'MCeffective_2017p8_3track':  (0.0089, 0.0100, 0.0406),
         'MCeffective_2017p8_4track':  (0.0192, 0.0265, 0.1331),
         'MCeffective_2017p8_5track':  (0.0605, 0.1203, 0.4470),
         'data10pc_2017_3track':       (0.0096, 0.0088, 0.0230),
         'data10pc_2017_4track':       (0.0232, 0.0293, 0.0886),
         'data10pc_2017_5track':       (0.0639, 0.1315, 0.4846),
         'data10pc_2018_3track':       (0.0101, 0.0088, 0.0228),
         'data10pc_2018_4track':       (0.0308, 0.0408, 0.2095),
         'data10pc_2018_5track':       (0.0898, 0.1711, 0.6318),
         'data10pc_2017p8_3track':     (0.0070, 0.0063, 0.0164),
         'data10pc_2017p8_4track':     (0.0172, 0.0209, 0.0642),
         'data10pc_2017p8_5track':     (0.0529, 0.1051, 0.3884),
         'data100pc_2017_3track':      (0.0048, 0.0056, 0.0225),
         'data100pc_2017_4track':      (0.0087, 0.0125, 0.0619),
         'data100pc_2017_5track':      (1,      1,      1     ),
         'data100pc_2018_3track':      (0.0053, 0.0058, 0.0236),
         'data100pc_2018_4track':      (0.0098, 0.0132, 0.0660),
         'data100pc_2018_5track':      (1,      1,      1     ),
         'data100pc_2017p8_3track':    (0.0036, 0.0041, 0.0162),
         'data100pc_2017p8_4track':    (0.0064, 0.0089, 0.0450),
         'data100pc_2017p8_5track':    (1,      1,      1     ),
         }

def _ksort(s, o=['MCscaled', 'MCeffective', 'data10pc', 'data100pc', '2017', '2018', '2017p8']):
    s = s.replace('sm_','').split('_')
    try:
        return (o.index(s[0]), o.index(s[1]), s[2][0])
    except ValueError:
        return -1


if __name__ == '__main__':
    import sys

    if 'parse' in sys.argv:
        from JMTucker.Tools.ROOTTools import *
        for fn in sorted([s for s in sys.argv[1:] if s.endswith('.root')], key=_ksort):
            f = ROOT.TFile(fn)
            hn = f.Get('h_2v_dvvc_bins_rmses')
            hd = f.Get('h_true_2v_dvv_norm')
            v = lambda i: hn.GetBinContent(i) / hd.GetBinContent(i)
            name = fn.replace('.root','').replace('sm_','')
            print '    %-30s: (%.4f, %.4f, %.4f),' % ('"%s"' % name, v(1), v(2), v(3))

    elif 'compare' in sys.argv:
        from JMTucker.Tools import colors
        from ebins2 import ebins2
        for k in sorted(ebins.keys(), key=_ksort):
            na = (-1,-1,-1)
            e  = ebins .get(k, na)
            e2 = ebins2.get(k, na)
            diff = tuple(b-a for a,b in zip(e,e2))
            mdiff = max(abs(d) for d in diff)
            c = colors.none
            if mdiff > 0.05:
                c = colors.boldred
            elif mdiff > 0.02:
                c = colors.yellow
            print c('%-30s: %7.4f %7.4f %7.4f      %7.4f %7.4f %7.4f       %7.4f %7.4f %7.4f' % ((k,) + e + e2 + diff))
