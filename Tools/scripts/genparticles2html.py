#!/usr/bin/env python

import re, sys

#pythia8_re = re.compile('(?P<index>\d+) +(?P<pdgid>\d+) +(?P<name>.*) +(?P<status>-{0,1}\d+) +(?P<mother1>\d+) +(?P<mother2>\d+) +(?P<daughter1>\d+) +(?P<daughter2>\d+) +(?P<color1>\d+) +(?P<color2>\d+)')
pld_re = re.compile(r'(?P<index>\d+) \| +(?P<pdgid>-{0,1}\d+) - +(?P<name>.*) \| +(?P<status>-{0,1}\d+) \| +(?P<mother1>-{0,1}\d+) +(?P<mother2>-{0,1}\d+) +(?P<daughter1>-{0,1}\d+) +(?P<daughter2>-{0,1}\d+)(?P<rest>.*)')
#mo = pld_re.search('    0 |  2212 -         p+ |  4 |   -1   -1  213  278 |  0  3 |   0.000  26756.000  0.000 |      0.000      0.000   4000.000    0.938 |      0.000      0.000      0.000 |')
#d = mo.groupdict()
#raise 1

format = None
for x in ['pythia8', 'pld']:
    if x in sys.argv:
        if format is None:
            format = eval(x + '_re')
        sys.argv.remove(x)
if format is None:
    print 'usage: genparticles2html.py pythia8|pld listing.txt'
    sys.exit(1)

fn = sys.argv[1]

def linkto(text, index, anchor=False):
    if index == '-1':
        return text
    s = '<a '
    if anchor:
        s += 'name="index%s" ' % index
    s += 'href="#index%s">' % index
    s += text + '</a>'
    return s

def srep(s, a, b, n):
    return s[:a] + n + s[b:]

html = open(fn + '.html', 'wt')
html.write('<html><body><pre>\n')
seen = []
for line in open(fn):
    line.replace('\n', '<br>\n')

    mo = format.search(line)
    if mo is None:
        html.write(line)
        continue

    d = mo.groupdict()
    index = d['index']
    seen.append(int(index))

    # sorry
    i0,i1 = mo.span('index')
    p0,p1 = mo.span('pdgid')
    m10, m11 = mo.span('mother1')
    m20, m21 = mo.span('mother2')
    d10, d11 = mo.span('daughter1')
    d20, d21 = mo.span('daughter2')
    m1 = d['mother1']
    m2 = d['mother2']
    d1 = d['daughter1']
    d2 = d['daughter2']

    l = line
    hline = l[:i0] + linkto(index, index, True) + l[i1:m10] + linkto(m1,m1) + l[m11:m20] + linkto(m2,m2) + l[m21:d10] + linkto(d1,d1) + l[d11:d20] + linkto(d2,d2) + l[d21:]
    html.write(hline)

html.write('</pre></body></html>\n')
html.close()

check = range(min(seen), max(seen)+1)
assert seen == check
