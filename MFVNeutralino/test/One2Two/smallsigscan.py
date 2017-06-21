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

sample_nums = [-39,-46,-53,-60]
samples = []
for i in sample_nums:
    s = getattr(Samples, num2name[i])
    s.sample_num = i
    samples.append(s)

__all__ = [
    'num2name',
    'name2num',
    'samples',
    'Samples'
    ]
