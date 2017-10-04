from limits_input import *

kinds = 'mfv_neu', 'mfv_ddbar'
taus = [100, 400, 1000, 10000, 31000]
masses = [300,400,500,600, 800, 1200, 1800, 3000]

f = ROOT.TFile('limits_input.root')
names =  ['%s_tau%05ium_M%04i' % (k,t,m) for k in kinds for t in taus for m in masses]
isamples = [name2isample(f, name) for name in names]

class sample:
    pass
samples = []
for name, isample in zip(names, isamples):
    s = sample()
    s.name = name
    s.isample = isample
    s.tau = name2tau(name)
    s.mass = name2mass(name)
    samples.append(s)

__all__ = [
    'names'
    'isamples',
    'samples',
    ]
