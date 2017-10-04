import re
from JMTucker.Tools import Samples
from limits_input import ROOT, name2isample

num2name = {}
name2num = {}

_re = re.compile(r'samples.push_back\(\{(-\d+), "(mfv_.*00)", 0, 0\}\);')
for line in open('signals.h'):
    mo = _re.search(line)
    if mo:
        num, name = mo.groups()
        num = int(num)
        #print num, name
        num2name[num] = name
        name2num[name] = num

kinds = 'mfv_neu', 'mfv_ddbar'
taus = [100, 400, 1000, 10000, 31000]
masses = [300,400,500,600, 800, 1200, 1800, 3000]

kinds = ['mfv_neu']
taus = [1000]
masses = [800]

f = ROOT.TFile('limits_input.root')
sample_nums = [name2isample(f, name) for name in ['%s_tau%05ium_M%04i' % (k,t,m) for k in kinds for t in taus for m in masses]]

#samples = []
#for i in sample_nums:
#    s = getattr(Samples, num2name[i])
#    s.sample_num = i
#    samples.append(s)

__all__ = [
    'num2name',
    'name2num',
    'sample_nums'
#    'samples',
    'Samples'
    ]
