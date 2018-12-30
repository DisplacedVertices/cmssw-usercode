#!/usr/bin/env python

# need to install hepdata_lib with pip
#   pip install --user hepdata_lib
# pip doesn't come with SLC6 or CMSSW <= 8 but it does with >= 9

tdr_path = '/uscms_data/d2/tucker/tdr'
submission_path = '/uscms_data/d2/tucker/hepdata_tmp'

paper_code = 'EXO-17-018'
nfigures_expected = [2, 1, 2, 1, 4, 4, 6, 6]
arxiv = '1808.03078'
cds = '2633728'
inspire = '1685992'
doi = '10.1103/PhysRevD.98.09201'

####

from JMTucker.Tools.ROOTTools import ROOT
import os, string, hepdata_lib as hepdata
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
        self.roots = {}
        self.pdfs = {}

    def ok(self, nfiles_expected):
        if not all((self.name,
                    self.label,
                    self.caption,
                    type(self.caption) == str,
                    len(self.files) == nfiles_expected,
                    )):
            return False

        for fn in self.files:
            if not os.path.isfile(fn):
                print 'no file', fn
                return False
            root_fn = fn.replace('.pdf', '.root')
            if not os.path.isfile(root_fn):
                print 'no file', root_fn
                root_fn = None
            
            subfig = fn[fn.index('.pdf')-1]
            if subfig not in string.ascii_lowercase:
                assert len(self.files) == 1
                subfig = 'a'

            self.pdfs [subfig] = fn
            self.roots[subfig] = hepdata.RootFileReader(root_fn) if root_fn else root_fn

        return True

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
                
print 'parsed abstract:'
print repr(abstract)
print
print 'parsed figures:'
for figure in figures:
    print figure.name, figure.label
    print repr(figure.caption)
    for fn in figure.files:
        print '   ', fn
print

assert abstract
assert len(figures) == len(nfigures_expected) and all(figure.ok(nexp) for figure, nexp in zip(figures, nfigures_expected))

for figure in figures:
    exec '%s = figure' % figure.name

####

sub = hepdata.Submission()

sub.comment = abstract

sub.add_link('CMS-Results', 'https://cms-results.web.cern.ch/cms-results/public-results/publications/%s/' % paper_code)
sub.add_link('arXiv', 'https://arxiv.org/abs/%s' % arxiv)
sub.add_link('CDS', 'https://cds.cern.ch/record/%s' % cds)
sub.add_link('DOI', 'http://doi.org/%s' % doi)
sub.add_record_id(inspire, 'inspire')

fig004.sig00p3mm = fig004.roots['a'].read_hist_1d('c0/h_signal_-46_dbv_mm')
fig004.sig01p0mm = fig004.roots['a'].read_hist_1d('c0/h_signal_-53_dbv_mm')
fig004.sig10p0mm = fig004.roots['a'].read_hist_1d('c0/h_signal_-60_dbv_mm')

#f = ROOT.TFile(fig004.files[0].replace('pdf','root'))
#h = f.Get('c0').FindObject("h_signal_-46_dbv_mm")
#fig004.sig0p3mm = hepdata.(fig004.files[0].replace('pdf','root')).read_hist_1d('c0/h_signal_-46_dbv_mm')
#fig004.sig0p3mm = hepdata.RootFileReader(fig004.files[0].replace('pdf','root')).read_hist_1d('
#sub.create_files(submission_path)
