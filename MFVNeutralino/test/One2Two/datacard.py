#!/usr/bin/env python

import sys
import ROOT; ROOT.gROOT.SetBatch()
from signal_efficiency import SignalEfficiencyCombiner

if 'bkg_fully_correlated' in sys.argv:
    bkg_correlation = 'fully'
if 'bkg_yearwise_correlated' in sys.argv:
    bkg_correlation = 'yearwise'
elif 'bkg_binwise_correlated' in sys.argv:
    bkg_correlation = 'binwise'
else: #elif 'bkg_uncorrelated' in sys.argv:
    bkg_correlation = False

include_2016 = 'include_2016' in sys.argv # includes 2015
include_sigmc = 'no_sigmc' not in sys.argv
years = ('2016','2017','2018') if include_2016 else ('2017','2018')

template = '''
# isample = {0.isample}
# nice name = {0.nice_name}
# total sig rate = {0.total_sig_rate} / {0.total_int_lumi_xsec} -> {0.total_sig_eff} eff -> hint {0.limit_hint}
'''

if include_2016:
    template += '''
imax 9
jmax 3
kmax {0.nsyst}
------------
bin           b60  b61  b62      b70  b71  b72      b80  b81  b82
observation   {0.observed_2016}  {0.observed_2017}  {0.observed_2018}
------------
bin           b60  b61  b62      b70  b71  b72      b80  b81  b82                b60  b61  b62      b70  b71  b72      b80  b81  b82              b60  b61  b62      b70  b71  b72      b80  b81  b82             b60  b61  b62      b70  b71  b72      b80  b81  b82
process       sig  sig  sig      sig  sig  sig      sig  sig  sig                bk6  bk6  bk6      bk6  bk6  bk6      bk6  bk6  bk6              bk7  bk7  bk7      bk7  bk7  bk7      bk7  bk7  bk7             bk8  bk8  bk8      bk8  bk8  bk8      bk8  bk8  bk8
process       0    0    0        0    0    0        0    0    0                  1    1    1        1    1    1        1    1    1                2    2    2        2    2    2        2    2    2               3    3    3        3    3    3        3    3    3  
rate          {0.sig_rate_2016}  {0.sig_rate_2017}  {0.sig_rate_2018}            {0.bkg_rate_2016}  0    0    0        0    0    0                0    0    0        {0.bkg_rate_2017}  0    0    0               0    0    0        0    0    0        {0.bkg_rate_2018}
------------
sig6 lnN {0.sig_uncert_2016} DASH6          DASH9    DASH9    DASH9
sig7 lnN DASH3 {0.sig_uncert_2017} DASH3    DASH9    DASH9    DASH9
sig8 lnN DASH6 {0.sig_uncert_2018}          DASH9    DASH9    DASH9
'''
    if include_sigmc:
        template += '''
sig6MC gmN {0.ngen_2016} {0.sigmc_alpha_2016} DASH6          DASH9   DASH9   DASH9
sig7MC gmN {0.ngen_2017} DASH3 {0.sigmc_alpha_2017} DASH3    DASH9   DASH9   DASH9
sig8MC gmN {0.ngen_2018} DASH6 {0.sigmc_alpha_2018}          DASH9   DASH9   DASH9
'''

else:
    template += '''
imax 6
jmax 2
kmax {0.nsyst}
------------
bin           b70  b71  b72      b80  b81  b82
observation   {0.observed_2017}  {0.observed_2018}
------------
bin           b70  b71  b72      b80  b81  b82                b70  b71  b72      b80  b81  b82             b70  b71  b72      b80  b81  b82
process       sig  sig  sig      sig  sig  sig                bk7  bk7  bk7      bk7  bk7  bk7             bk8  bk8  bk8      bk8  bk8  bk8
process       0    0    0        0    0    0                  1    1    1        1    1    1               2    2    2        2    2    2  
rate          {0.sig_rate_2017}  {0.sig_rate_2018}            {0.bkg_rate_2017}  0    0    0               0    0    0        {0.bkg_rate_2018}
------------
sig7 lnN {0.sig_uncert_2017} DASH3    DASH6   DASH6
sig8 lnN DASH3 {0.sig_uncert_2018}    DASH6   DASH6
'''
    if include_sigmc:
        template += '''
sig7MC gmN {0.ngen_2017} {0.sigmc_alpha_2017} DASH3    DASH6   DASH6
sig8MC gmN {0.ngen_2018} DASH3 {0.sigmc_alpha_2018}    DASH6   DASH6
'''


if bkg_correlation == 'fully':
    if include_2016:
        template += '''
bkg0 lnN DASH9 {0.bkg_uncert_2016} {0.bkg_uncert_2017} {0.bkg_uncert_2018}
'''
    else:
        template += '''
bkg0 lnN DASH6 {0.bkg_uncert_2017} {0.bkg_uncert_2018}
'''

elif bkg_correlation == 'yearwise':
    if include_2016:
        template += '''
bkg0 lnN DASH9    {0.bkg_uncert_2016} DASH6    DASH9                              DASH9
bkg1 lnN DASH9    DASH9                        DASH3 {0.bkg_uncert_2017} DASH3    DASH9
bkg2 lnN DASH9    DASH9                        DASH9                              DASH6 {0.bkg_uncert_2018}
'''
    else:
        template += '''
bkg0 lnN DASH6    {0.bkg_uncert_2017} DASH3    DASH6
bkg1 lnN DASH6    DASH6                        DASH3 {0.bkg_uncert_2018}
'''

elif bkg_correlation == 'binwise':
    if include_2016:
        template += '''
bkg0 lnN DASH9    {0.bkg_uncert_2016_0} - - DASH6    DASH3 {0.bkg_uncert_2017_0} - - DASH3    DASH6 {0.bkg_uncert_2018_0} - -
bkg1 lnN DASH9    - {0.bkg_uncert_2016_1} - DASH6    DASH3 - {0.bkg_uncert_2017_1} - DASH3    DASH6 - {0.bkg_uncert_2018_1} -
bkg2 lnN DASH9    - - {0.bkg_uncert_2016_2} DASH6    DASH3 - - {0.bkg_uncert_2017_2} DASH3    DASH6 - - {0.bkg_uncert_2018_2}
'''
    else:
        template += '''
bkg0 lnN DASH6    {0.bkg_uncert_2017_0} - - DASH3    DASH3 {0.bkg_uncert_2018_0} - -
bkg1 lnN DASH6    - {0.bkg_uncert_2017_1} - DASH3    DASH3 - {0.bkg_uncert_2018_1} -
bkg2 lnN DASH6    - - {0.bkg_uncert_2017_2} DASH3    DASH3 - - {0.bkg_uncert_2018_2}
'''

else:
    if include_2016:
        template += '''
bkg0 lnN DASH9    {0.bkg_uncert_2016_0} - - DASH6    DASH9                                    DASH9
bkg1 lnN DASH9    - {0.bkg_uncert_2016_1} - DASH6    DASH9                                    DASH9
bkg2 lnN DASH9    - - {0.bkg_uncert_2016_2} DASH6    DASH9                                    DASH9
bkg3 lnN DASH9    DASH9                              DASH3 {0.bkg_uncert_2017_0} - - DASH3    DASH9
bkg4 lnN DASH9    DASH9                              DASH3 - {0.bkg_uncert_2017_1} - DASH3    DASH9
bkg5 lnN DASH9    DASH9                              DASH3 - - {0.bkg_uncert_2017_2} DASH3    DASH9
bkg6 lnN DASH9    DASH9                              DASH9                                    DASH6 {0.bkg_uncert_2018_0} - -
bkg7 lnN DASH9    DASH9                              DASH9                                    DASH6 - {0.bkg_uncert_2018_1} -
bkg8 lnN DASH9    DASH9                              DASH9                                    DASH6 - - {0.bkg_uncert_2018_2}
'''
    else:
        template += '''
bkg0 lnN DASH6    {0.bkg_uncert_2017_0} - - DASH3    DASH6
bkg1 lnN DASH6    - {0.bkg_uncert_2017_1} - DASH3    DASH6
bkg2 lnN DASH6    - - {0.bkg_uncert_2017_2} DASH3    DASH6
bkg3 lnN DASH6    DASH6                              DASH3 {0.bkg_uncert_2018_0} - -
bkg4 lnN DASH6    DASH6                              DASH3 - {0.bkg_uncert_2018_1} -
bkg5 lnN DASH6    DASH6                              DASH3 - - {0.bkg_uncert_2018_2}
'''

for d in 3,6,9:
    template = template.replace('DASH%i' % d, ' '.join('-'*d))

def make(isample):
    combiner = SignalEfficiencyCombiner(years)
    r = combiner.combine(isample)
    r.nsyst = template.count('lnN') + template.count('gmN')

    def h2l(h):
        assert h.GetNbinsX() == 3
        return [h.GetBinContent(ib) for ib in xrange(1,3+1)]
    def get(n):
        return h2l(combiner.f.Get(n))
    def st(x, typ=float):
        if type(x) in (list,tuple):
            l = x
        elif type(x) == str:
            l = get(x)
        elif issubclass(type(x), ROOT.TH1):
            l = h2l(x)
        else:
            raise ValueError('duh %r' % x)
        fmt = '%.9g' if typ == float else '%s'
        return ' '.join(fmt % typ(v) for v in l)

    for year in years:
        setattr(r, 'observed_%s'    % year, st('h_observed_%s'      % year))
        setattr(r, 'bkg_rate_%s'    % year, st('h_bkg_dvv_rebin_%s' % year))
        setattr(r, 'sig_rate_%s'    % year, st(r.hs_dvv_rebin[year]))
        setattr(r, 'sig_uncert_%s'  % year, st(r.hs_uncert[year]))

        ngen = r.ngens[year]
        setattr(r, 'ngen_%s'        % year, str(ngen))
        setattr(r, 'sigmc_alpha_%s' % year, st([x / ngen for x in r.rates[year]]))

        bkg_uncert = get('h_bkg_uncert_%s' % year)
        setattr(r, 'bkg_uncert_%s' % year, bkg_uncert)
        for i,v in enumerate(bkg_uncert):
            setattr(r, 'bkg_uncert_%s_%i' % (year, i), v)

    print template.format(r)


if __name__ == '__main__':
    try:
        isample = int(sys.argv[1])
    except ValueError:
        from limitsinput import name2isample
        isample = name2isample(ROOT.TFile('limitsinput.root'), sys.argv[1])
    make(isample)
