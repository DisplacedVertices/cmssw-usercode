import os, sys, glob

def stats(fn, l, header='sigma_sig_limit'):
    f = open(fn, 'wt')
    l.sort()
    n = len(l)
    if n % 2 == 0:
        median = (l[n/2] + l[n/2-1])/2.
    else:
        median = l[n/2]
    lo68 = l[int(n/2 - 0.34*n)]
    hi68 = l[int(n/2 + 0.34*n)]
    lo95 = l[int(n/2 - 0.475*n)]
    hi95 = l[int(n/2 + 0.475*n)]
    f.write(header + ':Expected  2.5%: r < ' + '%f\n' % lo95)
    f.write(header + ':Expected 16.0%: r < ' + '%f\n' % lo68)
    f.write(header + ':Expected 50.0%: r < ' + '%f\n' % median)
    f.write(header + ':Expected 84.0%: r < ' + '%f\n' % hi68)
    f.write(header + ':Expected 97.5%: r < ' + '%f\n' % hi95)
    f.write(header + ':Observed Limit: r < ' + '%f\n' % median)
    f.close()
    return median, lo68, hi68, lo95, hi95

signals = [x for x in '''
mfv_neutralino_tau0100um_M0200
mfv_neutralino_tau0100um_M0300
mfv_neutralino_tau0100um_M0400
mfv_neutralino_tau0100um_M0600
mfv_neutralino_tau0100um_M0800
mfv_neutralino_tau0100um_M1000
mfv_neutralino_tau0300um_M0200
mfv_neutralino_tau0300um_M0300
mfv_neutralino_tau0300um_M0400
mfv_neutralino_tau0300um_M0600
mfv_neutralino_tau0300um_M0800
mfv_neutralino_tau0300um_M1000
mfv_neutralino_tau1000um_M0200
mfv_neutralino_tau1000um_M0300
mfv_neutralino_tau1000um_M0400
mfv_neutralino_tau1000um_M0600
mfv_neutralino_tau1000um_M0800
mfv_neutralino_tau1000um_M1000
mfv_neutralino_tau9900um_M0200
mfv_neutralino_tau9900um_M0300
mfv_neutralino_tau9900um_M0400
mfv_neutralino_tau9900um_M0600
mfv_neutralino_tau9900um_M0800
mfv_neutralino_tau9900um_M1000
'''.split('\n') if x]

try:
    signal = signals[int(sys.argv[1])]
    signals = [signal]
except IndexError:
    pass

def get_l(path):
    fns = glob.glob('/uscms_data/d1/tucker/combine/' + path + '/*stdout')
    l = []
    for fn in fns:
        lim = None
        for line in open(fn):
            if 'Limit:' in line:
                lim = float(line.split()[3])
        if lim is not None:
            l.append(lim)
    return l

for isig, signal in enumerate(signals):
    isignal = -1 - isig

    jobs = get_l('jobs_' + signal)
    toys = get_l('jobs_toys_' + signal)
    print signal, len(jobs), len(toys)
    if len(jobs) == 0:
        continue
    stats('combine_n%ix-1.out' % isignal, jobs)
    stats('combine_n%ix-2.out' % isignal, toys)

