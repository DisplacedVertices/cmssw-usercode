from JMTucker.MFVNeutralino.MiniTreeBase import *

fn = sys.argv[1]
f, t = get_f_t(fn)

kind = None
def setkind(x):
    global kind
    if kind is not None and x != kind:
        raise ValueError('kind unequal to previous')
    kind = x

for jentry in ttree_iterator(t):
    lsp0 = p4(t.gen_lsp_pt[0], t.gen_lsp_eta[0], t.gen_lsp_phi[0], t.gen_lsp_mass[0])
    lsp1 = p4(t.gen_lsp_pt[1], t.gen_lsp_eta[1], t.gen_lsp_phi[1], t.gen_lsp_mass[1])

    n = len(t.gen_daughters)
    assert len(t.gen_daughter_id) == n and n % 2 == 0

    ids = list(t.gen_daughter_id)
    aids = [abs(x) for x in ids]

    #print n, ids

    if n == 14 and aids[0:3] == [3,5,6] and aids[7:10] == [3,5,6] and aids[3] in [1,3,5] and aids[10] in [1,3,5] and aids[4] == 24 and aids[11] == 24:
        setkind('mfv')
    elif n == 4 and ids == [1,-1,1,-1]:
        setkind('ddbar')
    else:
        raise ValueError('unrecognized daughters')

    stride = n/2
    alldaus = t.gen_daughters[:stride], t.gen_daughters[stride:]
    alldauids = t.gen_daughter_id[:stride], t.gen_daughter_id[stride:]

    if kind == 'ddbar':
        visdaus = list(alldaus[0]), list(alldaus[1])
        d0, dbar0 = alldaus[0]
        d1, dbar1 = alldaus[1]
    elif kind == 'mfv':
        s0, b0, t0, bfromt0, W0, a0, b0 = alldaus[0]
        s1, b1, t1, bfromt1, W1, a1, b1 = alldaus[1]
        visdaus = [[],[]]
        for i in 0,1:
            for v,x in zip(alldaus[i], alldauids[i]):
                if abs(x) in [1,2,3,4,5,11,13,15]:
                    visdaus[i].append(v)

    sumpt = sum(v.Pt() for v in visdaus[0] + visdaus[1])
    print sumpt
