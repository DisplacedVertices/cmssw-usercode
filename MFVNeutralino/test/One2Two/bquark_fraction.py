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
def a(f0,f1,cb,cbbar):
    return e(f0,f1)**2 * c(cb,cbbar) * n(f0)
def f2(f0,f1,cb,cbbar):
    return a(f0,f1,cb,cbbar)/(1+a(f0,f1,cb,cbbar))


def print_f2(ntk,f0,f1,cb,cbbar):
    print 'ntk = %d: f0 = %.3f, f1 = %.3f, cb/cbbar = %.3f/%.3f = %.2f, nb/nbbar = %.2f, effb/effbbar = %.1f, f2 = %.2f' % (ntk, f0, f1, cb, cbbar, c(cb,cbbar), n(f0), e(f0,f1), f2(f0,f1,cb,cbbar))

if __name__ == '__main__':
    print 'f0,f1,cb,cbbar from sorting events by b quarks'
    print_f2(3, 0.176, 0.461, 0.584, 0.547)
    print_f2(7, 0.176, 0.463, 0.574, 0.532)
    print_f2(4, 0.176, 0.487, 0.563, 0.516)
    print_f2(5, 0.176, 0.549, 0.535, 0.493)
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 medium btag'
    print_f2(3, 0.199, 0.522, 0.580, 0.547)
    print_f2(7, 0.199, 0.525, 0.568, 0.535)
    print_f2(4, 0.199, 0.557, 0.555, 0.521)
    print_f2(5, 0.199, 0.536, 0.534, 0.494)
    print
