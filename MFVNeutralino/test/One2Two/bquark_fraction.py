#!/usr/bin/env python

#f0 = the fraction of preselected events with b quarks
#nb    = the number of preselected events with b quarks
#nbbar = the number of preselected events without b quarks
#nb/nbbar = n(f0)
def n(f0):
    return f0/(1-f0)

#f1 = the fraction of one-vertex events with b quarks
#effb    = the efficiency to reconstruct a vertex in an event with b quarks
#effbbar = the efficiency to reconstruct a vertex in an event without b quarks
#effb/effbbar = e(f0,f1)
def e(f0,f1):
    return f1/(1-f1) * 1/n(f0)

#f2 = the fraction of two-vertex events with b quarks
#cb    = the integrated efficiency correction for dVVC constructed from one-vertex events with b quarks
#cbbar = the integrated efficiency correction for dVVC constructed from one-vertex events without b quarks
#cb/cbbar = c(cb,cbbar)
def c(cb,cbbar):
    return cb/cbbar
def a(f0,f1,cb,cbbar,s):
    return e(f0,f1)**2 * c(cb,cbbar) * n(f0) * 1./s**2
def f2(f0,f1,cb,cbbar,s):
    return a(f0,f1,cb,cbbar,s)/(1+a(f0,f1,cb,cbbar,s))


def print_f2(ntk,f0,f1,cb,cbbar,s):
    f2_val = f2(f0,f1,cb,cbbar,s)
    print 'ntk = %d: f0 = %.3f, f1 = %.3f, cb/cbbar = %.3f/%.3f = %.2f, nb/nbbar = %.2f, effb/effbbar = %.1f, f2 = %.2f' % (ntk, f0, f1, cb, cbbar, c(cb,cbbar), n(f0), e(f0,f1), f2_val)
    return f2_val


def fb(ft,efft,frt):
    return (ft-frt)/(efft-frt)

if __name__ == '__main__':
    print 'f0,f1,cb,cbbar from sorting events by b quarks; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1)'
    print_f2(3, 0.176, 0.461, 0.584, 0.547, 1)
    print_f2(7, 0.176, 0.463, 0.574, 0.532, 1)
    print_f2(4, 0.176, 0.487, 0.563, 0.516, 1)
    print_f2(5, 0.176, 0.549, 0.535, 0.493, 1)
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 medium btag; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1)'
    print_f2(3, 0.199, 0.522, 0.580, 0.547, 1)
    print_f2(7, 0.199, 0.525, 0.568, 0.535, 1)
    print_f2(4, 0.199, 0.557, 0.555, 0.521, 1)
    print_f2(5, 0.199, 0.536, 0.534, 0.494, 1)
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 medium btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1)'
    f2_val_3trk = print_f2(3, fb(0.199,0.685,0.109), fb(0.522,0.804,0.247), 0.580, 0.547, 1)
    f2_val_7trk = print_f2(7, fb(0.199,0.685,0.109), fb(0.525,0.804,0.250), 0.568, 0.535, 1)
    f2_val_4trk = print_f2(4, fb(0.199,0.685,0.109), fb(0.557,0.811,0.284), 0.555, 0.521, 1)
    f2_val_5trk = print_f2(5, fb(0.199,0.685,0.109), fb(0.536,0.778,0.227), 0.534, 0.494, 1)
    print

    print '###########################'
    print "For utilities.py:"
    print "(3,'%.2f,%.2f'), (4,'%.2f,%.2f'), (5,'%.2f,%.2f'), (7,'%.2f,%.2f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print


    print 'f0,f1,cb,cbbar from sorting events by b quarks; assume all vertices in events with b quarks are reconstructed from b quarks (s=2)'
    print_f2(3, 0.176, 0.461, 0.584, 0.547, 2)
    print_f2(7, 0.176, 0.463, 0.574, 0.532, 2)
    print_f2(4, 0.176, 0.487, 0.563, 0.516, 2)
    print_f2(5, 0.176, 0.549, 0.535, 0.493, 2)
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 medium btag; assume all vertices in events with b quarks are reconstructed from b quarks (s=2)'
    print_f2(3, 0.199, 0.522, 0.580, 0.547, 2)
    print_f2(7, 0.199, 0.525, 0.568, 0.535, 2)
    print_f2(4, 0.199, 0.557, 0.555, 0.521, 2)
    print_f2(5, 0.199, 0.536, 0.534, 0.494, 2)
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 medium btag and unfolding; assume all vertices in events with b quarks are reconstructed from b quarks (s=2)'
    print_f2(3, fb(0.199,0.685,0.109), fb(0.522,0.804,0.247), 0.580, 0.547, 2)
    print_f2(7, fb(0.199,0.685,0.109), fb(0.525,0.804,0.250), 0.568, 0.535, 2)
    print_f2(4, fb(0.199,0.685,0.109), fb(0.557,0.811,0.284), 0.555, 0.521, 2)
    print_f2(5, fb(0.199,0.685,0.109), fb(0.536,0.778,0.227), 0.534, 0.494, 2)
    print
