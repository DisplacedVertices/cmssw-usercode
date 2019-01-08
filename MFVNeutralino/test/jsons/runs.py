import json, sys
rng = 'range' in sys.argv
if rng:
    sys.argv.remove('range')
l = json.load(open(sys.argv[1])).keys()
if rng:
    l = [int(x) for x in l]
    print min(l), max(l)
else:
    print ' '.join(sorted(l))

