import sys

count = 0
while 1:
    line = sys.stdin.readline()
    if count:
        count -= 1
        continue
    if line == ' NEW MINIMUM FOUND.  GO BACK TO MINIMIZATION STEP.\n':
        count = 9
        continue
    print line,
