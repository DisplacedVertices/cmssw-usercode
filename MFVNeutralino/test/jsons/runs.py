import json, sys
print ' '.join(sorted(json.load(open(sys.argv[1])).iterkeys()))

