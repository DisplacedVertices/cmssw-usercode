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

    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2017; nom'
    f2_val_3trk = print_f2(3, fb(0.146, 0.658, 0.044), fb(0.420, 0.755, 0.101), 0.587, 0.546, 1)
    f2_val_4trk = print_f2(4, fb(0.146, 0.658, 0.044), fb(0.441, 0.763, 0.108), 0.563, 0.521, 1)
    f2_val_5trk = print_f2(5, fb(0.146, 0.658, 0.044), fb(0.484, 0.737, 0.107), 0.540, 0.491, 1)
    f2_val_7trk = print_f2(7, fb(0.146, 0.658, 0.044), fb(0.421, 0.755, 0.101), 0.576, 0.534, 1)
    print

    print '###########################'
    print "For utilities.py:"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2018; nom'
    f2_val_3trk = print_f2(3, fb(0.127, 0.663, 0.029), fb(0.432, 0.781, 0.078), 0.530, 0.487, 1)
    f2_val_4trk = print_f2(4, fb(0.127, 0.663, 0.029), fb(0.470, 0.785, 0.078), 0.503, 0.480, 1)
    f2_val_5trk = print_f2(5, fb(0.127, 0.663, 0.029), fb(0.580, 0.792, 0.109), 0.541, 0.476, 1)
    f2_val_7trk = print_f2(7, fb(0.127, 0.663, 0.029), fb(0.435, 0.781, 0.078), 0.517, 0.484, 1)
    print

    print '###########################'
    print "For utilities.py:"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2017p8; nom'
    f2_val_3trk = print_f2(3, fb(0.134, 0.662, 0.037), fb(0.426, 0.769, 0.089), 0.559, 0.516, 1)
    f2_val_4trk = print_f2(4, fb(0.134, 0.662, 0.037), fb(0.457, 0.775, 0.092), 0.533, 0.501, 1)
    f2_val_5trk = print_f2(5, fb(0.134, 0.662, 0.037), fb(0.531, 0.767, 0.108), 0.545, 0.480, 1)
    f2_val_7trk = print_f2(7, fb(0.134, 0.662, 0.037), fb(0.429, 0.769, 0.089), 0.547, 0.508, 1)
    print

    print '###########################'
    print "For utilities.py:"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print

    ######################################
    #             ~ Data ~               #
    ######################################

    print '2017 Data: f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2017'
    f2_val_3trk_data = print_f2(3, fb(0.146, 0.658, 0.044), fb(0.420, 0.755, 0.101), 0.677, 0.630, 1)
    f2_val_4trk_data = print_f2(4, fb(0.146, 0.658, 0.044), fb(0.441, 0.763, 0.108), 0.662, 0.599, 1)
    print

    print '###########################'
    print "For utilities.py:"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f')" % (f2_val_3trk_data, 1-f2_val_3trk_data, f2_val_4trk_data, 1-f2_val_4trk_data)
    print '###########################'
    print

    print '2018 Data: f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2018'
    f2_val_3trk_data = print_f2(3, fb(0.127, 0.663, 0.029), fb(0.432, 0.781, 0.078), 0.600, 0.550, 1)
    f2_val_4trk_data = print_f2(4, fb(0.127, 0.663, 0.029), fb(0.470, 0.785, 0.078), 0.579, 0.532, 1)
    print

    print '###########################'
    print "For utilities.py:"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f')" % (f2_val_3trk_data, 1-f2_val_3trk_data, f2_val_4trk_data, 1-f2_val_4trk_data)
    print '###########################'
    print

    print '2017p8 Data: f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2017p8'
    f2_val_3trk_data = print_f2(3, fb(0.134, 0.662, 0.037), fb(0.426, 0.769, 0.089), 0.641, 0.592, 1)
    f2_val_4trk_data = print_f2(4, fb(0.134, 0.662, 0.037), fb(0.457, 0.775, 0.092), 0.621, 0.565, 1)
    print

    print '###########################'
    print "For utilities.py:"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f')" % (f2_val_3trk_data, 1-f2_val_3trk_data, f2_val_4trk_data, 1-f2_val_4trk_data)
    print '###########################'
    print


    ######################################
    # Systematics based on SF variations #
    ######################################

    # vary bcjet SFs up
    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2017; bcjet_up'
    f2_val_3trk = print_f2(3, fb(0.146, 0.688, 0.048), fb(0.420, 0.784, 0.113), 0.587, 0.546, 1)
    f2_val_4trk = print_f2(4, fb(0.146, 0.688, 0.048), fb(0.441, 0.791, 0.122), 0.563, 0.521, 1)
    f2_val_5trk = print_f2(5, fb(0.146, 0.688, 0.048), fb(0.484, 0.765, 0.120), 0.540, 0.491, 1)
    f2_val_7trk = print_f2(7, fb(0.146, 0.688, 0.048), fb(0.421, 0.784, 0.113), 0.576, 0.534, 1)
    print

    print '###########################'
    print "For utilities.py: (2017; bcjet SFs up)"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2018; bcjet_up'
    f2_val_3trk = print_f2(3, fb(0.127, 0.692, 0.033), fb(0.432, 0.808, 0.090), 0.530, 0.487, 1)
    f2_val_4trk = print_f2(4, fb(0.127, 0.692, 0.033), fb(0.470, 0.812, 0.090), 0.503, 0.480, 1)
    f2_val_5trk = print_f2(5, fb(0.127, 0.692, 0.033), fb(0.580, 0.818, 0.125), 0.541, 0.476, 1)
    f2_val_7trk = print_f2(7, fb(0.127, 0.692, 0.033), fb(0.435, 0.808, 0.089), 0.517, 0.484, 1)
    print

    print '###########################'
    print "For utilities.py: (2018; bcjet SFs up)"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2017p8; bcjet_up'
    f2_val_3trk = print_f2(3, fb(0.134, 0.691, 0.041), fb(0.426, 0.797, 0.101), 0.559, 0.516, 1)
    f2_val_4trk = print_f2(4, fb(0.134, 0.691, 0.041), fb(0.457, 0.803, 0.105), 0.533, 0.501, 1)
    f2_val_5trk = print_f2(5, fb(0.134, 0.691, 0.041), fb(0.531, 0.794, 0.122), 0.545, 0.480, 1)
    f2_val_7trk = print_f2(7, fb(0.134, 0.691, 0.041), fb(0.429, 0.797, 0.101), 0.547, 0.508, 1)
    print

    print '###########################'
    print "For utilities.py: (2017p8; bcjet SFs up)"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print


    # vary bcjet SFs down
    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2017; bcjet_down'
    f2_val_3trk = print_f2(3, fb(0.146, 0.628, 0.041), fb(0.420, 0.724, 0.088), 0.587, 0.546, 1)
    f2_val_4trk = print_f2(4, fb(0.146, 0.628, 0.041), fb(0.441, 0.732, 0.094), 0.563, 0.521, 1)
    f2_val_5trk = print_f2(5, fb(0.146, 0.628, 0.041), fb(0.484, 0.707, 0.094), 0.540, 0.491, 1)
    f2_val_7trk = print_f2(7, fb(0.146, 0.628, 0.041), fb(0.421, 0.724, 0.088), 0.576, 0.534, 1)
    print

    print '###########################'
    print "For utilities.py: (2017; bcjet SFs down)"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2018; bcjet_down'
    f2_val_3trk = print_f2(3, fb(0.127, 0.634, 0.026), fb(0.432, 0.752, 0.066), 0.530, 0.487, 1)
    f2_val_4trk = print_f2(4, fb(0.127, 0.634, 0.026), fb(0.470, 0.755, 0.065), 0.503, 0.480, 1)
    f2_val_5trk = print_f2(5, fb(0.127, 0.634, 0.026), fb(0.580, 0.764, 0.092), 0.541, 0.476, 1)
    f2_val_7trk = print_f2(7, fb(0.127, 0.634, 0.026), fb(0.435, 0.752, 0.066), 0.517, 0.484, 1)
    print

    print '###########################'
    print "For utilities.py: (2018; bcjet SFs down)"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2017p8; bcjet_down'
    f2_val_3trk = print_f2(3, fb(0.134, 0.633, 0.034), fb(0.426, 0.739, 0.077), 0.559, 0.516, 1)
    f2_val_4trk = print_f2(4, fb(0.134, 0.633, 0.034), fb(0.457, 0.746, 0.079), 0.533, 0.501, 1)
    f2_val_5trk = print_f2(5, fb(0.134, 0.633, 0.034), fb(0.531, 0.738, 0.093), 0.545, 0.480, 1)
    f2_val_7trk = print_f2(7, fb(0.134, 0.633, 0.034), fb(0.429, 0.739, 0.077), 0.547, 0.508, 1)
    print

    print '###########################'
    print "For utilities.py: (2017p8; bcjet SFs down)"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print

    # vary ljet SFs up
    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2017; ljet_up'
    f2_val_3trk = print_f2(3, fb(0.146, 0.661, 0.051), fb(0.420, 0.757, 0.111), 0.587, 0.546, 1)
    f2_val_4trk = print_f2(4, fb(0.146, 0.661, 0.051), fb(0.441, 0.765, 0.118), 0.563, 0.521, 1)
    f2_val_5trk = print_f2(5, fb(0.146, 0.661, 0.051), fb(0.484, 0.740, 0.118), 0.540, 0.491, 1)
    f2_val_7trk = print_f2(7, fb(0.146, 0.661, 0.051), fb(0.421, 0.757, 0.111), 0.576, 0.534, 1)
    print

    print '###########################'
    print "For utilities.py: (2017; ljet SFs up)"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2018; ljet_up'
    f2_val_3trk = print_f2(3, fb(0.127, 0.664, 0.033), fb(0.432, 0.782, 0.082), 0.530, 0.487, 1)
    f2_val_4trk = print_f2(4, fb(0.127, 0.664, 0.033), fb(0.470, 0.785, 0.081), 0.503, 0.480, 1)
    f2_val_5trk = print_f2(5, fb(0.127, 0.664, 0.033), fb(0.580, 0.793, 0.114), 0.541, 0.476, 1)
    f2_val_7trk = print_f2(7, fb(0.127, 0.664, 0.033), fb(0.435, 0.782, 0.082), 0.517, 0.484, 1)
    print

    print '###########################'
    print "For utilities.py: (2018; ljet SFs up)"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2017p8; ljet_up'
    f2_val_3trk = print_f2(3, fb(0.134, 0.664, 0.042), fb(0.426, 0.770, 0.096), 0.559, 0.516, 1)
    f2_val_4trk = print_f2(4, fb(0.134, 0.664, 0.042), fb(0.457, 0.777, 0.099), 0.533, 0.501, 1)
    f2_val_5trk = print_f2(5, fb(0.134, 0.664, 0.042), fb(0.531, 0.769, 0.115), 0.545, 0.480, 1)
    f2_val_7trk = print_f2(7, fb(0.134, 0.664, 0.042), fb(0.429, 0.771, 0.096), 0.547, 0.508, 1)
    print

    print '###########################'
    print "For utilities.py: (2017p8; ljet SFs up)"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print
    
    # vary ljet SFs down
    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2017; ljet_down'
    f2_val_3trk = print_f2(3, fb(0.146, 0.656, 0.037), fb(0.420, 0.752, 0.090), 0.587, 0.546, 1)
    f2_val_4trk = print_f2(4, fb(0.146, 0.656, 0.037), fb(0.441, 0.760, 0.099), 0.563, 0.521, 1)
    f2_val_5trk = print_f2(5, fb(0.146, 0.656, 0.037), fb(0.484, 0.734, 0.097), 0.540, 0.491, 1)
    f2_val_7trk = print_f2(7, fb(0.146, 0.656, 0.037), fb(0.421, 0.752, 0.091), 0.576, 0.534, 1)
    print

    print '###########################'
    print "For utilities.py: (2017; ljet SFs down)"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2018; ljet_down'
    f2_val_3trk = print_f2(3, fb(0.127, 0.662, 0.026), fb(0.432, 0.780, 0.074), 0.530, 0.487, 1)
    f2_val_4trk = print_f2(4, fb(0.127, 0.662, 0.026), fb(0.470, 0.784, 0.074), 0.503, 0.480, 1)
    f2_val_5trk = print_f2(5, fb(0.127, 0.662, 0.026), fb(0.580, 0.791, 0.103), 0.541, 0.476, 1)
    f2_val_7trk = print_f2(7, fb(0.127, 0.662, 0.026), fb(0.435, 0.780, 0.074), 0.517, 0.484, 1)
    print

    print '###########################'
    print "For utilities.py: (2018; ljet SFs down)"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print

    print 'f0,f1,cb,cbbar from sorting events by at least 1 tight btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1); 2017p8; ljet_down'
    f2_val_3trk = print_f2(3, fb(0.134, 0.661, 0.032), fb(0.426, 0.767, 0.082), 0.559, 0.516, 1)
    f2_val_4trk = print_f2(4, fb(0.134, 0.661, 0.032), fb(0.457, 0.774, 0.086), 0.533, 0.501, 1)
    f2_val_5trk = print_f2(5, fb(0.134, 0.661, 0.032), fb(0.531, 0.765, 0.099), 0.545, 0.480, 1)
    f2_val_7trk = print_f2(7, fb(0.134, 0.661, 0.032), fb(0.429, 0.767, 0.082), 0.547, 0.508, 1)
    print

    print '###########################'
    print "For utilities.py: (2017p8; ljet SFs down)"
    print "(3,'%.3f,%.3f'), (4,'%.3f,%.3f'), (5,'%.3f,%.3f'), (7,'%.3f,%.3f')" % (f2_val_3trk, 1-f2_val_3trk, f2_val_4trk, 1-f2_val_4trk, f2_val_5trk, 1-f2_val_5trk, f2_val_7trk, 1-f2_val_7trk)
    print '###########################'
    print

    ##################################
    # old stuff from the old btagger #
    ##################################

    #print 'f0,f1,cb,cbbar from sorting events by at least 1 medium btag; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1)'
    #print_f2(3, 0.199, 0.522, 0.580, 0.547, 1)
    #print_f2(7, 0.199, 0.525, 0.568, 0.535, 1)
    #print_f2(4, 0.199, 0.557, 0.555, 0.521, 1)
    #print_f2(5, 0.199, 0.536, 0.534, 0.494, 1)
    #print

    #print 'f0,f1,cb,cbbar from sorting events by at least 1 medium btag and unfolding; assume the probability of finding two vertices is the one-vertex efficiency squared (s=1)'
    #f2_val_3trk = print_f2(3, fb(0.199,0.685,0.109), fb(0.522,0.804,0.247), 0.580, 0.547, 1)
    #f2_val_7trk = print_f2(7, fb(0.199,0.685,0.109), fb(0.525,0.804,0.250), 0.568, 0.535, 1)
    #f2_val_4trk = print_f2(4, fb(0.199,0.685,0.109), fb(0.557,0.811,0.284), 0.555, 0.521, 1)
    #f2_val_5trk = print_f2(5, fb(0.199,0.685,0.109), fb(0.536,0.778,0.227), 0.534, 0.494, 1)
    #print

    #print 'f0,f1,cb,cbbar from sorting events by b quarks; assume all vertices in events with b quarks are reconstructed from b quarks (s=2)'
    #print_f2(3, 0.176, 0.461, 0.584, 0.547, 2)
    #print_f2(7, 0.176, 0.463, 0.574, 0.532, 2)
    #print_f2(4, 0.176, 0.487, 0.563, 0.516, 2)
    #print_f2(5, 0.176, 0.549, 0.535, 0.493, 2)
    #print

    #print 'f0,f1,cb,cbbar from sorting events by at least 1 medium btag; assume all vertices in events with b quarks are reconstructed from b quarks (s=2)'
    #print_f2(3, 0.199, 0.522, 0.580, 0.547, 2)
    #print_f2(7, 0.199, 0.525, 0.568, 0.535, 2)
    #print_f2(4, 0.199, 0.557, 0.555, 0.521, 2)
    #print_f2(5, 0.199, 0.536, 0.534, 0.494, 2)
    #print

    #print 'f0,f1,cb,cbbar from sorting events by at least 1 medium btag and unfolding; assume all vertices in events with b quarks are reconstructed from b quarks (s=2)'
    #print_f2(3, fb(0.199,0.685,0.109), fb(0.522,0.804,0.247), 0.580, 0.547, 2)
    #print_f2(7, fb(0.199,0.685,0.109), fb(0.525,0.804,0.250), 0.568, 0.535, 2)
    #print_f2(4, fb(0.199,0.685,0.109), fb(0.557,0.811,0.284), 0.555, 0.521, 2)
    #print_f2(5, fb(0.199,0.685,0.109), fb(0.536,0.778,0.227), 0.534, 0.494, 2)
    #print
