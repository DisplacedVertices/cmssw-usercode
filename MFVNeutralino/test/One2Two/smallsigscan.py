import re
from JMTucker.Tools import Samples

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

sample_nums = [-11,-30,-49,-68,-87,-39,-42,-46,-52,-55] + [-105,-124,-134,-137,-140,-143,-146,-149,-152,-162,-181]
sample_nums.sort(reverse=True)

samples = []
for i in sample_nums:
    s = getattr(Samples, num2name[i])
    s.sample_num = i
    samples.append(s)

__all__ = [
    'num2name',
    'name2num',
    'sample_nums'
    'samples',
    'Samples'
    ]
