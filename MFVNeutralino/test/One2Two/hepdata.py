#!/usr/bin/env python

# need to install hepdata_lib with pip
#   pip install --user hepdata_lib
# pip doesn't come with SLC6 or CMSSW <= 8 but it does with >= 9

tdr_path = '/uscms_data/d2/tucker/tdr'
submission_path = '/uscms_data/d2/tucker/hepdata_tmp_3'

paper_code = 'EXO-17-018'
nfigures_expected = [2, 1, 2, 1, 4, 4, 6, 6]
arxiv = '1808.03078'
cds = '2633728'
inspire = '1685992'
doi = '10.1103/PhysRevD.98.092011'

# symbols in abstract/captions that need to be defined (if one is substring of another, put the longer one first)
syms_replaces = [
    (r'\GeV', r' GeV'),
    (r'\TeV', r' TeV'),
    (r'\mm', r' mm'),
    (r'\PSGcz', r'$\tilde{\chi}^{0}$'),
    (r'\PSg', r'$\tilde{g}$'),
    (r'\PSQt', r'$\tilde{t}$'),
    (r'\unit', r' '),
    (r'{fb}', r'fb'),
    (r'\fbinv', r'$~\textrm{fb}^{-1}$'),
    (r'\CL', 'C.L.'),
    (r'\cmsLeft', 'upper'), # in PRD copy, "left" and "right" translate to upper and lower in the column format
    (r'\cmsRight', 'lower'),
    (r'\dbv', '$d_{BV}$'),
    (r'\dvvc', '$d_{VV}^{C}$'),
    (r'\dvv', '$d_{VV}$'),
    (r'\%', '%'),
    ]

########################################################################

from JMTucker.Tools import colors
from JMTucker.Tools.ROOTTools import ROOT
import os, string, textwrap, hepdata_lib as hepdata
from copy import deepcopy
from math import hypot
from pprint import pprint

paper_path = os.path.join(tdr_path, 'papers/%s/trunk' % paper_code)
paper_fn = os.path.join(paper_path, paper_code + '.tex')

# time for some fragile parsing
abstract = None
figure = None
figures = []

class Figure:
    def __init__(self):
        self.name = None
        self.label = None
        self.caption = None
        self.files = []
        self.subfigs = []
        self.rootfns = {}
        self.roots = {}
        self.canvases = {}
        self.pdfs = {}
        self.objs = {} # the raw value dicts read from root files
        self.reps = {} # representative of the dependent variables for all the objects
        self.tables = {} # the hepdata objects

    def finalize(self, nfiles_expected):
        if not all((self.name,
                    self.label,
                    self.caption,
                    type(self.caption) == str,
                    len(self.files) == nfiles_expected,
                    )):
            return False

        self.fig = int(self.name.replace('fig', ''))
        self.uno = len(self.files) == 1

        for fn in self.files:
            if not os.path.isfile(fn):
                print 'no file', fn
                return False
            rootfn = fn.replace('.pdf', '.root')
            if not os.path.isfile(rootfn):
                rootfn = None
            
            subfig = fn[fn.index('.pdf')-1]
            if subfig not in string.ascii_lowercase:
                assert self.uno
                subfig = 'a'
            self.subfigs.append(subfig)

            self.pdfs[subfig] = fn
            self.rootfns[subfig] = rootfn
            r = self.roots[subfig] = hepdata.RootFileReader(rootfn) if rootfn else rootfn
            if rootfn:
                c = self.canvases[subfig] = r.tfile.Get('c0')
                if not c:
                    self.canvases[subfig] = r.tfile.Get('c')
            self.objs[subfig] = {}
            self.reps[subfig] = None

            table_name = 'Figure %i' % self.fig
            if not self.uno:
                table_name += subfig
            t = self.tables[subfig] = hepdata.Table(table_name)
            t.description = self.caption
            t.location = table_name
            t.add_image(fn)

        return True

    def check_objs(self):
        for subfig in self.objs.iterkeys():
            o = self.objs[subfig]
            r = self.reps[subfig]
            for z in o.itervalues():
                if z['x'] != r['x'] or (z.has_key('x_edges') and z['x_edges'] != r['x_edges']):
                    import pdb
                    pdb.set_trace()

def dedouble(s):
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s

for line in open(paper_fn):
    line = line.strip()
    if not line:
        continue

    if line.startswith(r'\abstract{'):
        abstract = []
    elif line.startswith(r'\begin{figure'):
        figure = Figure()
    else:
        if type(abstract) == list:
            if line != '}':
                abstract.append(line)
            else:
                abstract = dedouble(' '.join(abstract))

        elif figure:
            if line.startswith(r'\end{figure'):
                figures.append(figure)
                figure = None

            elif line.startswith(r'\caption{'):
                figure.caption = [line.replace(r'\caption{', '')]

            elif type(figure.caption) == list:
                figure.caption.append(line)
                if line.endswith('}'):
                    figure.caption = ' '.join(figure.caption)
                    figure.caption = dedouble(figure.caption[:-1])

            elif line.startswith(r'\includegraphics'):
                bn = line[line.index('{')+1:line.index('}')]
                name = bn[:10] # Figure_XXX
                assert name.startswith('Figure_')
                name = name.replace('Figure_', 'fig')
                if figure.name:
                    assert name == figure.name
                else:
                    figure.name = name
                figure.files.append(os.path.join(paper_path, bn))

            elif line.startswith(r'\label'):
                label = line[line.index('{')+1:line.index('}')]
                assert label.startswith('fig:')
                label = label[4:]
                assert figure.label is None
                figure.label = label

def printwrap(s):
    for line in textwrap.wrap(s):
        print line

print colors.bold('parsed abstract:')
printwrap(repr(abstract))

for a,b in syms_replaces:
    abstract = abstract.replace(a,b)

print '\n', colors.bold('revised abstract:')
printwrap(abstract)

print '\n', colors.bold('parsed figures:')
for figure in figures:
    print '\n', colors.bold('%s %s' % (figure.name, figure.label))
    printwrap(repr(figure.caption))
    for fn in figure.files:
        print '   ', fn
print

assert abstract

syms_left = set()

for figure in figures:
    exec '%s = figure' % figure.name

    for a,b in syms_replaces:
        figure.caption = figure.caption.replace(a,b)

    print '\n', colors.bold('%s %s revised caption' % (figure.name, figure.label))
    printwrap(figure.caption)

    for word in figure.caption.split():
        if '\\' in word:
            sym = word[word.find('\\'):]
            sym = sym[0] + ''.join(x for x in sym[1:] if x in string.ascii_letters + string.digits)
            if sym != '\\':
                syms_left.add(sym)

if syms_left:
    print '\n', colors.bold('remaining possibly undefined syms:'), '\n', sorted(syms_left), '\n'

assert len(figures) == len(nfigures_expected) and all(figure.finalize(nexp) for figure, nexp in zip(figures, nfigures_expected))

for figure in figures:
    print colors.bold('%s %s' % (figure.name, figure.label))
    for subfig in figure.subfigs:
        if figure.rootfns[subfig]:
            print '    %s:' % subfig, figure.rootfns[subfig], [x.GetName() for x in figure.canvases[subfig].GetListOfPrimitives() if x.GetName() and x.GetName()[0] != 'T']
        else:
            print '    %s: no root files' % subfig

########################################################################

def _check(o,keys):
    assert sorted(o.iterkeys()) == sorted(keys)
    s = set(len(x) for x in o.itervalues())
    assert len(s) == 1
    return s.pop()
def hist_check(h):
    return _check(h, ['dy','x','x_edges','y'])
def graph_check(g):
    return _check(g, ['x','dx','y','dy'])
def hist2d_check(h):
    return _check(h, ['x','x_edges','y','y_edges','z','dz'])

#def truncate_hist(h, nbins):
#    hist_check(h)
#    for z in 'x','x_edges','y','dy':
#        h[z] = h[z][:nbins]
#    return h

def graph_on_hist(g, h):
    graph_check(g)
    n = hist_check(h)

    dy0 = 0. if type(g['dy']) == float else (-0.,0.)
    hg = {
        'y': [0.]*n,
        'dy': [dy0]*n,
        'x': h['x'],
        'x_edges': h['x_edges']
        }

    used = set()
    for x,y,dx,dy in zip(g['x'], g['y'], g['dx'], g['dy']):
        assert dx == (-0., 0.)
        for i,(xa,xb) in enumerate(h['x_edges']):
            if xa <= x < xb:
                if i in used:
                    raise ValueError('x = %f maps to already used i = %i' % (x, i))
                used.add(i)
                break
        else:
            raise ValueError('x = %f not contained in x_edges %r' % (x, h['x_edges']))
        assert abs(x-h['x'][i]) < 1e-6
        hg['y'][i] = y
        hg['dy'][i] = dy
    return hg

def lower_edge(h):
    for i in xrange(hist2d_check(h)):
        h['x'][i] = h['x_edges'][i][0]
        h['y'][i] = h['y_edges'][i][0]
    return h

def upper_limit_on_zero(h):
    n = hist_check(h)
    ul = 1.841054761
    for i in xrange(n):
        if h['y'][i] == 0.:
            dy0, dy1 = h['dy'][i]
            assert dy0 == -0. and (dy1 == 0. or abs(dy1-ul) < 1e-6)
            h['dy'][i] = (-0., ul)
    return h

def add_variable(t, v, vals, uncs=[]):
    v.values = vals
    for unc, unc_vals in uncs:
        if unc_vals:
            unc.values = unc_vals
        v.add_uncertainty(unc)
    t.add_variable(v)

########################################################################

# rest of the script is more paper dependent and may have (unlabeled) gotchas

signames = ('sig00p3mm', 'sig01p0mm', 'sig10p0mm') # for Figs. 2,4
nicesigname = {'sig00p3mm': '0.3', 'sig01p0mm': '1', 'sig10p0mm': '10'}

####

figures = figures[1:] # drop the feynman diagram one

# gotcha: exclusion curve isn't on the limit grid
fig006excl = deepcopy(fig006)
fig006excl.name = 'fig006excl'
for subfig in 'ab':
    fig006excl.tables[subfig].name = 'figure_6%s_excl' % subfig
fig006excl.roots = fig006.roots # the deepcopy of the root files crashes

####

fig002.objs['a']['sig00p3mm'] = fig002.roots['a'].read_hist_1d('c0/h_signal_-46_dvv_mm', xlim=(0., 4.))
fig002.objs['a']['sig01p0mm'] = fig002.roots['a'].read_hist_1d('c0/h_signal_-53_dvv_mm', xlim=(0., 4.))
fig002.objs['a']['sig10p0mm'] = fig002.roots['a'].read_hist_1d('c0/h_signal_-60_dvv_mm', xlim=(0., 4.))
fig002.objs['a']['sig10p0mm']['y'][-1] += 18.2 - 1 # gotcha (broken y-axis in paper)
fig002.reps['a'] = fig002.objs['a']['sig00p3mm']

####

fig003.reps['a'] = fig003.objs['a']['eff_neu']  = lower_edge(fig003.roots['a'].read_hist_2d('c/signal_efficiency_mfv_neu',           xlim=(300,2800), ylim=(0.1,100)))
fig003.reps['b'] = fig003.objs['b']['eff_stop'] = lower_edge(fig003.roots['b'].read_hist_2d('c/signal_efficiency_mfv_stopdbardbar',  xlim=(300,2800), ylim=(0.1,100)))
for subfig in 'ab':
    fig003.reps[subfig]['dz_syst'] = [z*0.24 for z in fig003.reps[subfig]['z']] # gotcha (add flat 24% syst uncert from Table 2)

####

fig004.objs['a']['sig00p3mm'] = fig004.roots['a'].read_hist_1d('c0/h_signal_-46_dbv_mm', xlim=(0., 4.))
fig004.objs['a']['sig01p0mm'] = fig004.roots['a'].read_hist_1d('c0/h_signal_-53_dbv_mm', xlim=(0., 4.))
fig004.objs['a']['sig10p0mm'] = fig004.roots['a'].read_hist_1d('c0/h_signal_-60_dbv_mm', xlim=(0., 4.))
r = fig004.reps['a'] = fig004.objs['a']['sig00p3mm']

fig004.objs['a']['observed']  = upper_limit_on_zero(graph_on_hist(fig004.roots['a'].read_graph('c0/Graph'), r))

# gotcha: hand-edit the first bins in the yaml to have 0 error with label "Exact ($d_{BV}$ > 0.1 mm)"

####

for subfig in 'abcd':
    r = fig005.reps[subfig] = fig005.objs[subfig]['predicted'] = fig005.roots[subfig].read_hist_1d('c0/h_c1v_dvv_mm', xlim=(0., 4.))
    fig005.objs[subfig]['observed'] = upper_limit_on_zero(graph_on_hist(fig005.roots[subfig].read_graph('c0/Graph'), r))

####

fig006.reps['a'] = fig006.objs['a']['lim2d_neu']  = lower_edge(fig006.roots['a'].read_hist_2d('c/observed', xlim=(300,2800), ylim=(0.1,100)))
fig006.reps['b'] = fig006.objs['b']['lim2d_stop'] = lower_edge(fig006.roots['b'].read_hist_2d('c/observed', xlim=(300,2800), ylim=(0.1,100)))

for subfig, particle in zip('ab', ('neu', 'stopdbardbar')):
    fig006excl.objs[subfig]['observed'] = fig006excl.roots[subfig].read_graph('c/mfv_%s_observed_fromrinterp_nm_exc_g' % particle)
    fig006excl.objs[subfig]['expected'] = fig006excl.roots[subfig].read_graph('c/mfv_%s_expect50_fromrinterp_nm_exc_g' % particle)

####

for f in fig007, fig008:
    for subfig in 'abcdef':
        for g in 'expect95', 'expect68', 'expect50', 'observed':
            f.objs[subfig][g] = f.roots[subfig].read_graph('c/%s' % g)
        f.reps[subfig] = f.objs[subfig]['expect50']
        # gotcha: 68%, 95% aren't symmetric about the median, reframe in terms of that for the stupid hepdata data model
        assert set(f.objs[subfig]['expect50']['dy']) == set([(-0.,0.)])
        for cl in '68', '95':
            f.objs[subfig]['expect50']['dy'+cl] = [(yn+dyn[0]-yo, yn+dyn[1]-yo) for yo, yn, dyn in zip(f.objs[subfig]['expect50']['y'], f.objs[subfig]['expect'+cl]['y'], f.objs[subfig]['expect'+cl]['dy'])]

####

for figure in figures:
    figure.check_objs()

########################################################################

sub = hepdata.Submission()

sub.comment = abstract

sub.add_link('CMS-Results', 'https://cms-results.web.cern.ch/cms-results/public-results/publications/%s/' % paper_code)
sub.add_link('arXiv', 'https://arxiv.org/abs/%s' % arxiv)
sub.add_link('CDS', 'https://cds.cern.ch/record/%s' % cds)
sub.add_link('DOI', 'https://doi.org/%s' % doi)
sub.add_record_id(inspire, 'inspire')

####

f = fig002
t = f.tables['a']

add_variable(t, hepdata.Variable('$d_{VV}$', is_independent=True, is_binned=True, units='mm'), f.reps['a']['x_edges'])

for signame in signames:
    o = f.objs['a'][signame]
    v = hepdata.Variable(r'Predicted multijet signal yield, $c\tau = %s~\textrm{mm}$, $m = 800~\textrm{GeV}$, $\sigma = 1~\textrm{fb}$' % nicesigname[signame], is_independent=False, is_binned=False)
    u = hepdata.Uncertainty('Statistical (~sqrt(n_generated))')
    add_variable(t, v, o['y'], [(u, o['dy'])])

sub.add_table(t)

####

f = fig003
for subfig in 'ab':
    o = f.reps[subfig]
    t = f.tables[subfig]
    t.location += ' (%s plot)' % {'a': 'upper', 'b': 'lower'}[subfig]
    particle = {'a': r'\tilde{\chi}^{0} / \tilde{g}', 'b': r'\tilde{t}'}[subfig]

    add_variable(t, hepdata.Variable(r'$m_{%s}$'     % particle, is_independent=True, is_binned=False, units='GeV'), o['x'])
    add_variable(t, hepdata.Variable(r'$c\tau_{%s}$' % particle, is_independent=True, is_binned=False, units='mm'),  o['y'])

    v = hepdata.Variable(r'Efficiency (full selection + $d_{VV}$ > 0.4 mm)', is_independent=False, is_binned=False)
    add_variable(t, v, o['z'], [(hepdata.Uncertainty('Statistical'), o['dz']), (hepdata.Uncertainty('Systematic (Table 2)'), o['dz_syst'])])

    sub.add_table(t)

####

f = fig004
t = f.tables['a']

add_variable(t, hepdata.Variable('$d_{BV}$', is_independent=True, is_binned=True, units='mm'), f.reps['a']['x_edges'])

for signame in signames:
    o = f.objs['a'][signame]
    v = hepdata.Variable(r'Predicted multijet signal yield, $c\tau = %s~\textrm{mm}$, $m = 800~\textrm{GeV}$, $\sigma = 1~\textrm{fb}$' % nicesigname[signame], is_independent=False, is_binned=False)
    u = hepdata.Uncertainty('Statistical (~sqrt(n_generated))')
    add_variable(t, v, o['y'], [(u, o['dy'])])

o = f.objs['a']['observed']
v = hepdata.Variable('Observed yield', is_independent=False, is_binned=False)
add_variable(t, v, o['y'])

sub.add_table(t)

####

f = fig005
for subfig in 'abcd':
    t = f.tables[subfig]
    t.location += ' (%s plot)' % {'a': 'upper left', 'b': 'upper right', 'c': 'lower left', 'd': 'lower right'}[subfig]

    add_variable(t, hepdata.Variable('$d_{VV}$', is_independent=True, is_binned=True, units='mm'), f.reps[subfig]['x_edges'])

    if subfig == 'a':
        ntracks_title = r'3-track $\times$ 3-track'
    elif subfig == 'b':
        ntracks_title = r'4-track $\times$ 3-track'
    elif subfig == 'c':
        ntracks_title = r'4-track $\times$ 4-track'
    elif subfig == 'd':
        ntracks_title = r'$\geq$5-track $\times$ $\geq$5-track'

    o = f.objs[subfig]['predicted']
    v = hepdata.Variable('Background template normalized to total observed yield, ' + ntracks_title, is_independent=False, is_binned=False)
    add_variable(t, v, o['y'])

    o = f.objs[subfig]['observed']
    v = hepdata.Variable('Observed yield, ' + ntracks_title, is_independent=False, is_binned=False)
    add_variable(t, v, o['y'])

    sub.add_table(t)

####

f = fig006
for subfig in 'ab':
    o = f.reps[subfig]
    t = f.tables[subfig]
    t.location += ' (%s upper and lower plots, grid of limit values)' % {'a': 'left', 'b': 'right'}[subfig]
    particle = {'a': r'\tilde{\chi}^{0} / \tilde{g}', 'b': r'\tilde{t}'}[subfig]

    add_variable(t, hepdata.Variable(r'$m_{%s}$'     % particle, is_independent=True, is_binned=False, units='GeV'), o['x'])
    add_variable(t, hepdata.Variable(r'$c\tau_{%s}$' % particle, is_independent=True, is_binned=False, units='mm'),  o['y'])

    v = hepdata.Variable(r'Observed 95% C.L. upper limits on $\sigma\mathcal{B}^{2}$', is_independent=False, is_binned=False, units='fb')
    add_variable(t, v, o['z'])

    sub.add_table(t)

####

f = fig006excl
for subfig in 'ab':
    o = f.objs[subfig]
    t = f.tables[subfig]
    t.location += ' (%s upper and lower plots, mass exclusion curves)' % {'a': 'left', 'b': 'right'}[subfig]
    particle = {'a': r'\tilde{\chi}^{0} / \tilde{g}', 'b': r'\tilde{t}'}[subfig]

    assert o['expected']['y'] == o['observed']['y']
    add_variable(t, hepdata.Variable(r'$c\tau_{%s}$' % particle, is_independent=True,  is_binned=False, units='mm'), o['expected']['y'])
    add_variable(t, hepdata.Variable(r'$m_{%s}$ observed lower limit' % particle, is_independent=False, is_binned=False, units='GeV'), o['observed']['x'])
    add_variable(t, hepdata.Variable(r'$m_{%s}$ expected lower limit' % particle, is_independent=False, is_binned=False, units='GeV'), o['expected']['x'])

    sub.add_table(t)

####

for f in fig007, fig008:
    for subfig in 'abcdef':
        o = f.reps[subfig]
        t = f.tables[subfig]
        t.location += ' (%s plot)' % {'a': 'upper left', 'b': 'upper right', 'c': 'middle left', 'd': 'middle right', 'e': 'lower left', 'f': 'lower right'}[subfig]
        n = 'abcdef'.index(subfig)
        particle = {0: r'\tilde{\chi}^{0} / \tilde{g}', 1: r'\tilde{t}'}[n%2]
        umb = n/2

        if f == fig007:
            fixed = r'$c\tau_{%s} = %s~\textrm{mm}$' % (particle, {0: '0.3', 1: '1', 2: '10'}[umb])
            add_variable(t, hepdata.Variable(r'$m_{%s}$'     % particle, is_independent=True, is_binned=False, units='GeV'), o['x'])
        else:
            fixed = r'$m_{%s} = %i~\textrm{GeV}$' % (particle, {0: 800, 1: 1600, 2: 2400}[umb])
            add_variable(t, hepdata.Variable(r'$c\tau_{%s}$' % particle, is_independent=True, is_binned=False, units='mm'),  o['x'])

        v = hepdata.Variable(r'Observed 95% C.L. upper limits on $\sigma\mathcal{B}^{2}$ for fixed ' + fixed, is_independent=False, is_binned=False, units='fb')
        add_variable(t, v, f.objs[subfig]['observed']['y'])

        v = hepdata.Variable(r'Expected 95% C.L. upper limits on $\sigma\mathcal{B}^{2}$ for fixed ' + fixed, is_independent=False, is_binned=False, units='fb')
        u68 = hepdata.Uncertainty('68% expected', is_symmetric=False)
        u95 = hepdata.Uncertainty('95% expected', is_symmetric=False)
        add_variable(t, v, f.objs[subfig]['expect50']['y'], [(u68, f.objs[subfig]['expect50']['dy68']), (u95, f.objs[subfig]['expect50']['dy95'])])

        sub.add_table(t)

####

sub.create_files(submission_path)


'''
hand-edit patch:

diff -r -x '*png' -uN hepdata_tmp_3/figure_4.yaml hepdata_cand4/figure_4.yaml
--- hepdata_tmp_3/figure_4.yaml	2019-01-23 11:26:32.789611179 -0600
+++ hepdata_cand4/figure_4.yaml	2019-01-23 04:07:21.294676562 -0600
@@ -5,7 +5,7 @@
     units: ''
   values:
   - errors:
-    - label: Statistical (~sqrt(n_generated))
+    - label: Exact ($d_{BV}$ > 0.1 mm)
       symerror: 0
     value: 0
   - errors:
@@ -170,7 +170,7 @@
     units: ''
   values:
   - errors:
-    - label: Statistical (~sqrt(n_generated))
+    - label: Exact ($d_{BV}$ > 0.1 mm)
       symerror: 0
     value: 0
   - errors:
@@ -335,7 +335,7 @@
     units: ''
   values:
   - errors:
-    - label: Statistical (~sqrt(n_generated))
+    - label: Exact ($d_{BV}$ > 0.1 mm)
       symerror: 0
     value: 0
   - errors:
diff -r -x '*png' -uN hepdata_tmp_3/submission.yaml hepdata_cand4/submission.yaml
--- hepdata_tmp_3/submission.yaml	2019-01-23 11:26:50.316896681 -0600
+++ hepdata_cand4/submission.yaml	2019-01-23 03:56:35.019005752 -0600
@@ -9,9 +9,9 @@
 - description: DOI
   location: https://doi.org/10.1103/PhysRevD.98.092011
 comment: Results are reported from a search for long-lived particles in proton-proton
-  collisions at $\sqrt{s}=13 TeV$ delivered by the CERN LHC and collected by the CMS
+  collisions at $\sqrt{s}$ = 13 TeV delivered by the CERN LHC and collected by the CMS
   experiment. The data sample, which was recorded during 2015 and 2016, corresponds
-  to an integrated luminosity of 38.5$~\textrm{fb}^{-1}$. This search uses benchmark
+  to an integrated luminosity of $38.5~\textrm{fb}^{-1}$. This search uses benchmark
   signal models in which long-lived particles are pair-produced and each decays into
   two or more quarks, leading to a signal with multiple jets and two displaced vertices
   composed of many tracks. No events with two well-separated high-track-multiplicity
@@ -40,8 +40,8 @@
   location: thumb_Figure_002.png
 data_file: figure_2.yaml
 description: Distribution of the distance between vertices in the $x$-$y$ plane, $d_{VV}$,
-  for simulated multijet signals with $m = 800 GeV$, production cross section 1 fb,
-  and $c\tau = 0.3$, 1.0, and 10 mm, with the background template overlaid. All vertex
+  for simulated multijet signals with $m$ = 800 GeV, production cross section 1 fb,
+  and $c\tau$ = 0.3, 1.0, and 10 mm, with the background template overlaid. All vertex
   and event selection criteria have been applied. The last bin includes the overflow
   events.
 keywords: []
@@ -54,9 +54,9 @@
 - description: Thumbnail image file
   location: thumb_Figure_003-a.png
 data_file: figure_3a.yaml
-description: Signal efficiency as a function of signal mass and lifetime, for the
-  multijet (upper) and dijet (lower) signal samples. All vertex and event selection
-  criteria have been applied, as well as the requirement $$d_{VV}$ > 0.4 mm$.
+description: Signal efficiency as a function of signal mass and lifetime for the
+  multijet signal samples. All vertex and event selection
+  criteria have been applied, as well as the requirement $d_{VV}$ > 0.4 mm.
 keywords: []
 location: Figure 3a (upper plot)
 name: Figure 3a
@@ -67,9 +67,9 @@
 - description: Thumbnail image file
   location: thumb_Figure_003-b.png
 data_file: figure_3b.yaml
-description: Signal efficiency as a function of signal mass and lifetime, for the
-  multijet (upper) and dijet (lower) signal samples. All vertex and event selection
-  criteria have been applied, as well as the requirement $$d_{VV}$ > 0.4 mm$.
+description: Signal efficiency as a function of signal mass and lifetime for the
+  dijet signal samples. All vertex and event selection
+  criteria have been applied, as well as the requirement $d_{VV}$ > 0.4 mm.
 keywords: []
 location: Figure 3b (lower plot)
 name: Figure 3b
@@ -81,8 +81,8 @@
   location: thumb_Figure_004.png
 data_file: figure_4.yaml
 description: Distribution of $d_{BV}$ in $\geq$5-track one-vertex events for data
-  and simulated multijet signals with $m = 800 GeV$, production cross section 1 fb,
-  and $c\tau = 0.3$, 1.0, and 10 mm. Event preselection and vertex selection criteria
+  and simulated multijet signals with $m$ = 800 GeV, production cross section 1 fb,
+  and $c\tau$ = 0.3, 1.0, and 10 mm. Event preselection and vertex selection criteria
   have been applied. The last bin includes the overflow events.
 keywords: []
 location: Figure 4
@@ -95,11 +95,9 @@
   location: thumb_Figure_005-a.png
 data_file: figure_5a.yaml
 description: Distribution of the distance between vertices in the $x$-$y$ plane in
-  two-vertex events. The points show the data ($d_{VV}$), and the solid lines show
-  the background template ($d_{VV}^{C}$) normalized to the data, for events with two
-  3-track vertices (upper left), one 4-track vertex and one 3-track vertex (upper
-  right), two 4-track vertices (lower left), and two $\geq$5-track vertices (lower
-  right). In each plot, the last bin includes the overflow events. The dotted lines
+  events with two 3-track vertices. The points show the data ($d_{VV}$), and the solid lines show
+  the background template ($d_{VV}^{C}$) normalized to the data.
+  The last bin includes the overflow events. The dotted lines
   indicate the boundaries between the three bins used in the fit.
 keywords: []
 location: Figure 5a (upper left plot)
@@ -112,11 +110,9 @@
   location: thumb_Figure_005-b.png
 data_file: figure_5b.yaml
 description: Distribution of the distance between vertices in the $x$-$y$ plane in
-  two-vertex events. The points show the data ($d_{VV}$), and the solid lines show
-  the background template ($d_{VV}^{C}$) normalized to the data, for events with two
-  3-track vertices (upper left), one 4-track vertex and one 3-track vertex (upper
-  right), two 4-track vertices (lower left), and two $\geq$5-track vertices (lower
-  right). In each plot, the last bin includes the overflow events. The dotted lines
+  events with one 4-track vertex and one 3-track vertex. The points show the data ($d_{VV}$), and the solid lines show
+  the background template ($d_{VV}^{C}$) normalized to the data.
+  The last bin includes the overflow events. The dotted lines
   indicate the boundaries between the three bins used in the fit.
 keywords: []
 location: Figure 5b (upper right plot)
@@ -129,11 +125,9 @@
   location: thumb_Figure_005-c.png
 data_file: figure_5c.yaml
 description: Distribution of the distance between vertices in the $x$-$y$ plane in
-  two-vertex events. The points show the data ($d_{VV}$), and the solid lines show
-  the background template ($d_{VV}^{C}$) normalized to the data, for events with two
-  3-track vertices (upper left), one 4-track vertex and one 3-track vertex (upper
-  right), two 4-track vertices (lower left), and two $\geq$5-track vertices (lower
-  right). In each plot, the last bin includes the overflow events. The dotted lines
+  events with two 4-track vertices. The points show the data ($d_{VV}$), and the solid lines show
+  the background template ($d_{VV}^{C}$) normalized to the data.
+  The last bin includes the overflow events. The dotted lines
   indicate the boundaries between the three bins used in the fit.
 keywords: []
 location: Figure 5c (lower left plot)
@@ -146,11 +140,9 @@
   location: thumb_Figure_005-d.png
 data_file: figure_5d.yaml
 description: Distribution of the distance between vertices in the $x$-$y$ plane in
-  two-vertex events. The points show the data ($d_{VV}$), and the solid lines show
-  the background template ($d_{VV}^{C}$) normalized to the data, for events with two
-  3-track vertices (upper left), one 4-track vertex and one 3-track vertex (upper
-  right), two 4-track vertices (lower left), and two $\geq$5-track vertices (lower
-  right). In each plot, the last bin includes the overflow events. The dotted lines
+  events with two $\geq$5-track vertices. The points show the data ($d_{VV}$), and the solid lines show
+  the background template ($d_{VV}^{C}$) normalized to the data.
+  The last bin includes the overflow events. The dotted lines
   indicate the boundaries between the three bins used in the fit.
 keywords: []
 location: Figure 5d (lower right plot)
@@ -163,14 +155,10 @@
   location: thumb_Figure_006-a.png
 data_file: figure_6a.yaml
 description: Observed 95% C.L. upper limits on $\sigma\mathcal{B}^2$ for the multijet
-  (left) and dijet (right) signals as a function of mass and mean proper decay length.
-  The upper plots span $c\tau$ from 1 to 100 mm, and the lower plots span $c\tau$
-  from 0.1 to 1 mm. The overlaid mass exclusion curves assume gluino pair production
-  cross sections for the multijet signals and top squark pair production cross sections
-  for the dijet signals, and 100% branching fraction.
+  signals as a function of mass and mean proper decay length.
 keywords: []
 location: Figure 6a (left upper and lower plots, grid of limit values)
-name: Figure 6a
+name: Figure 6a (grid of limit values)
 ---
 additional_resources:
 - description: Image file
@@ -178,15 +166,11 @@
 - description: Thumbnail image file
   location: thumb_Figure_006-b.png
 data_file: figure_6b.yaml
-description: Observed 95% C.L. upper limits on $\sigma\mathcal{B}^2$ for the multijet
-  (left) and dijet (right) signals as a function of mass and mean proper decay length.
-  The upper plots span $c\tau$ from 1 to 100 mm, and the lower plots span $c\tau$
-  from 0.1 to 1 mm. The overlaid mass exclusion curves assume gluino pair production
-  cross sections for the multijet signals and top squark pair production cross sections
-  for the dijet signals, and 100% branching fraction.
+description: Observed 95% C.L. upper limits on $\sigma\mathcal{B}^2$ for the
+  dijet signals as a function of mass and mean proper decay length.
 keywords: []
 location: Figure 6b (right upper and lower plots, grid of limit values)
-name: Figure 6b
+name: Figure 6b (grid of limit values)
 ---
 additional_resources:
 - description: Image file
@@ -194,15 +178,12 @@
 - description: Thumbnail image file
   location: thumb_Figure_006-a.png
 data_file: figure_6a_excl.yaml
-description: Observed 95% C.L. upper limits on $\sigma\mathcal{B}^2$ for the multijet
-  (left) and dijet (right) signals as a function of mass and mean proper decay length.
-  The upper plots span $c\tau$ from 1 to 100 mm, and the lower plots span $c\tau$
-  from 0.1 to 1 mm. The overlaid mass exclusion curves assume gluino pair production
-  cross sections for the multijet signals and top squark pair production cross sections
-  for the dijet signals, and 100% branching fraction.
+description: Mass exclusion curves for the multijet signals, assuming
+  gluino pair production cross sections
+  and 100% branching fraction.
 keywords: []
 location: Figure 6a (left upper and lower plots, mass exclusion curves)
-name: figure_6a_excl
+name: Figure 6a (mass exclusion curves)
 ---
 additional_resources:
 - description: Image file
@@ -210,15 +191,12 @@
 - description: Thumbnail image file
   location: thumb_Figure_006-b.png
 data_file: figure_6b_excl.yaml
-description: Observed 95% C.L. upper limits on $\sigma\mathcal{B}^2$ for the multijet
-  (left) and dijet (right) signals as a function of mass and mean proper decay length.
-  The upper plots span $c\tau$ from 1 to 100 mm, and the lower plots span $c\tau$
-  from 0.1 to 1 mm. The overlaid mass exclusion curves assume gluino pair production
-  cross sections for the multijet signals and top squark pair production cross sections
-  for the dijet signals, and 100% branching fraction.
+description: Mass exclusion curves for the dijet signals, assuming
+  top squark pair production cross sections
+  and 100% branching fraction.
 keywords: []
 location: Figure 6b (right upper and lower plots, mass exclusion curves)
-name: figure_6b_excl
+name: Figure 6b (mass exclusion curves)
 ---
 additional_resources:
 - description: Image file
@@ -227,11 +205,11 @@
   location: thumb_Figure_007-a.png
 data_file: figure_7a.yaml
 description: Observed and expected 95% C.L. upper limits on $\sigma\mathcal{B}^2$
-  for the multijet (left) and dijet (right) signals, as a function of mass for a fixed
-  $c\tau$ of 0.3 mm (upper), 1.0 mm (middle), and 10 mm (lower). The gluino pair production
-  cross section is overlaid for the multijet signals, and the top squark pair production
-  cross section is overlaid for the dijet signals. The uncertainties in the theoretical
-  cross sections include those due to the renormalization and factorization scales,
+  for the multijet signals as a function of mass for a fixed
+  $c\tau$ of 0.3 mm. The gluino pair production
+  cross section is overlaid.
+  The uncertainties in the theoretical
+  cross section include those due to the renormalization and factorization scales,
   and the parton distribution functions.
 keywords: []
 location: Figure 7a (upper left plot)
@@ -244,11 +222,11 @@
   location: thumb_Figure_007-b.png
 data_file: figure_7b.yaml
 description: Observed and expected 95% C.L. upper limits on $\sigma\mathcal{B}^2$
-  for the multijet (left) and dijet (right) signals, as a function of mass for a fixed
-  $c\tau$ of 0.3 mm (upper), 1.0 mm (middle), and 10 mm (lower). The gluino pair production
-  cross section is overlaid for the multijet signals, and the top squark pair production
-  cross section is overlaid for the dijet signals. The uncertainties in the theoretical
-  cross sections include those due to the renormalization and factorization scales,
+  for the dijet signals as a function of mass for a fixed
+  $c\tau$ of 0.3 mm.
+  The top squark pair production
+  cross section is overlaid. The uncertainties in the theoretical
+  cross section include those due to the renormalization and factorization scales,
   and the parton distribution functions.
 keywords: []
 location: Figure 7b (upper right plot)
@@ -261,11 +239,11 @@
   location: thumb_Figure_007-c.png
 data_file: figure_7c.yaml
 description: Observed and expected 95% C.L. upper limits on $\sigma\mathcal{B}^2$
-  for the multijet (left) and dijet (right) signals, as a function of mass for a fixed
-  $c\tau$ of 0.3 mm (upper), 1.0 mm (middle), and 10 mm (lower). The gluino pair production
-  cross section is overlaid for the multijet signals, and the top squark pair production
-  cross section is overlaid for the dijet signals. The uncertainties in the theoretical
-  cross sections include those due to the renormalization and factorization scales,
+  for the multijet signals as a function of mass for a fixed
+  $c\tau$ of 1.0 mm. The gluino pair production
+  cross section is overlaid.
+  The uncertainties in the theoretical
+  cross section include those due to the renormalization and factorization scales,
   and the parton distribution functions.
 keywords: []
 location: Figure 7c (middle left plot)
@@ -278,11 +256,11 @@
   location: thumb_Figure_007-d.png
 data_file: figure_7d.yaml
 description: Observed and expected 95% C.L. upper limits on $\sigma\mathcal{B}^2$
-  for the multijet (left) and dijet (right) signals, as a function of mass for a fixed
-  $c\tau$ of 0.3 mm (upper), 1.0 mm (middle), and 10 mm (lower). The gluino pair production
-  cross section is overlaid for the multijet signals, and the top squark pair production
-  cross section is overlaid for the dijet signals. The uncertainties in the theoretical
-  cross sections include those due to the renormalization and factorization scales,
+  for the dijet signals as a function of mass for a fixed
+  $c\tau$ of 1.0 mm.
+  The top squark pair production
+  cross section is overlaid. The uncertainties in the theoretical
+  cross section include those due to the renormalization and factorization scales,
   and the parton distribution functions.
 keywords: []
 location: Figure 7d (middle right plot)
@@ -295,11 +273,11 @@
   location: thumb_Figure_007-e.png
 data_file: figure_7e.yaml
 description: Observed and expected 95% C.L. upper limits on $\sigma\mathcal{B}^2$
-  for the multijet (left) and dijet (right) signals, as a function of mass for a fixed
-  $c\tau$ of 0.3 mm (upper), 1.0 mm (middle), and 10 mm (lower). The gluino pair production
-  cross section is overlaid for the multijet signals, and the top squark pair production
-  cross section is overlaid for the dijet signals. The uncertainties in the theoretical
-  cross sections include those due to the renormalization and factorization scales,
+  for the multijet signals as a function of mass for a fixed
+  $c\tau$ of 10 mm. The gluino pair production
+  cross section is overlaid.
+  The uncertainties in the theoretical
+  cross section include those due to the renormalization and factorization scales,
   and the parton distribution functions.
 keywords: []
 location: Figure 7e (lower left plot)
@@ -312,11 +290,11 @@
   location: thumb_Figure_007-f.png
 data_file: figure_7f.yaml
 description: Observed and expected 95% C.L. upper limits on $\sigma\mathcal{B}^2$
-  for the multijet (left) and dijet (right) signals, as a function of mass for a fixed
-  $c\tau$ of 0.3 mm (upper), 1.0 mm (middle), and 10 mm (lower). The gluino pair production
-  cross section is overlaid for the multijet signals, and the top squark pair production
-  cross section is overlaid for the dijet signals. The uncertainties in the theoretical
-  cross sections include those due to the renormalization and factorization scales,
+  for the dijet signals as a function of mass for a fixed
+  $c\tau$ of 10 mm.
+  The top squark pair production
+  cross section is overlaid. The uncertainties in the theoretical
+  cross section include those due to the renormalization and factorization scales,
   and the parton distribution functions.
 keywords: []
 location: Figure 7f (lower right plot)
@@ -329,8 +307,8 @@
   location: thumb_Figure_008-a.png
 data_file: figure_8a.yaml
 description: Observed and expected 95% C.L. upper limits on $\sigma\mathcal{B}^2$
-  for the multijet (left) and dijet (right) signals, as a function of $c\tau$ for
-  a fixed mass of 800 GeV (upper), 1600 GeV (middle), and 2400 GeV (lower).
+  for the multijet signals as a function of $c\tau$ for
+  a fixed mass of 800 GeV.
 keywords: []
 location: Figure 8a (upper left plot)
 name: Figure 8a
@@ -342,8 +320,8 @@
   location: thumb_Figure_008-b.png
 data_file: figure_8b.yaml
 description: Observed and expected 95% C.L. upper limits on $\sigma\mathcal{B}^2$
-  for the multijet (left) and dijet (right) signals, as a function of $c\tau$ for
-  a fixed mass of 800 GeV (upper), 1600 GeV (middle), and 2400 GeV (lower).
+  for the dijet signals as a function of $c\tau$ for
+  a fixed mass of 800 GeV.
 keywords: []
 location: Figure 8b (upper right plot)
 name: Figure 8b
@@ -355,8 +333,8 @@
   location: thumb_Figure_008-c.png
 data_file: figure_8c.yaml
 description: Observed and expected 95% C.L. upper limits on $\sigma\mathcal{B}^2$
-  for the multijet (left) and dijet (right) signals, as a function of $c\tau$ for
-  a fixed mass of 800 GeV (upper), 1600 GeV (middle), and 2400 GeV (lower).
+  for the multijet signals as a function of $c\tau$ for
+  a fixed mass of 1600 GeV.
 keywords: []
 location: Figure 8c (middle left plot)
 name: Figure 8c
@@ -368,8 +346,8 @@
   location: thumb_Figure_008-d.png
 data_file: figure_8d.yaml
 description: Observed and expected 95% C.L. upper limits on $\sigma\mathcal{B}^2$
-  for the multijet (left) and dijet (right) signals, as a function of $c\tau$ for
-  a fixed mass of 800 GeV (upper), 1600 GeV (middle), and 2400 GeV (lower).
+  for the dijet signals as a function of $c\tau$ for
+  a fixed mass of 1600 GeV.
 keywords: []
 location: Figure 8d (middle right plot)
 name: Figure 8d
@@ -381,8 +359,8 @@
   location: thumb_Figure_008-e.png
 data_file: figure_8e.yaml
 description: Observed and expected 95% C.L. upper limits on $\sigma\mathcal{B}^2$
-  for the multijet (left) and dijet (right) signals, as a function of $c\tau$ for
-  a fixed mass of 800 GeV (upper), 1600 GeV (middle), and 2400 GeV (lower).
+  for the multijet signals as a function of $c\tau$ for
+  a fixed mass of 2400 GeV.
 keywords: []
 location: Figure 8e (lower left plot)
 name: Figure 8e
@@ -394,8 +372,8 @@
   location: thumb_Figure_008-f.png
 data_file: figure_8f.yaml
 description: Observed and expected 95% C.L. upper limits on $\sigma\mathcal{B}^2$
-  for the multijet (left) and dijet (right) signals, as a function of $c\tau$ for
-  a fixed mass of 800 GeV (upper), 1600 GeV (middle), and 2400 GeV (lower).
+  for the dijet signals as a function of $c\tau$ for
+  a fixed mass of 2400 GeV.
 keywords: []
 location: Figure 8f (lower right plot)
 name: Figure 8f
'''
