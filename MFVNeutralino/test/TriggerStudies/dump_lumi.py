from DVCode.Tools.LumiLines import *
lls = LumiLines('/uscms/home/tucker/mfvrecipe/lumi.gzpickle')
f = open('fafa', 'wt')
s = 0.
for ll in lls.lls:
    f.write('%i %i %f\n' % (ll.run, ll.ls, ll.recorded))
    s += ll.recorded
f.close()
print len(lls.lls)
print s

