from JMTucker.MFVNeutralino.MiniTreeBase import *

path = 'crab/MiniTreeV20'

r = []

for s in Samples.mfv_signal_samples:
    w = s.partial_weight * ac.int_lumi * ac.scale_factor
    f, t = get_f_t(os.path.join(path, s.name + '.root'))
    n = t.Draw('nvtx', 'nvtx == 2')
    nn = n*w
    print s.name, n, w, nn
    r.append('%.4f' % nn)

print '[' + ', '.join(r) + ']'




    

    
