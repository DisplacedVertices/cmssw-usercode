import csv
from itertools import izip
from collections import defaultdict
from LumiList import LumiList

golden = LumiList('2016.json')
maxls = defaultdict(int)
for run, ls in golden.getLumis():
    if ls > maxls[run]:
        maxls[run] = ls

with open('pathinfo/PFHT900.all', 'rb') as f:
    reader = csv.reader(f)
    rows = [r for r in reader]

assert set(len(r) for r in rows) == set([7])
header = rows.pop(0)
assert header == ['# run', 'cmsls', 'prescidx', 'totprescval', 'hltpath/prescval', 'logic', 'l1bit/prescval']

changes = defaultdict(lambda: defaultdict(list))

for row in rows:
    run, ls, prescale_index, total_prescale, hlt_path_prescale, logic, l1_paths_prescale = row
    run, ls, prescale_index, total_prescale = int(run), int(ls), int(prescale_index), int(total_prescale)
    assert total_prescale <= 1
    if total_prescale != 1:
        print row
    hlt_path, hlt_prescale = hlt_path_prescale.split('/')
    hlt_prescale = int(hlt_prescale)
    hlt_version = int(hlt_path.split('HLT_PFHT900_v')[1])
    assert hlt_prescale == 1
    assert logic == 'OR'
    l1_prescales = []
    lowest_l1_threshold = 999
    for l1_path_prescale in l1_paths_prescale.split():
        l1_path, l1_prescale = l1_path_prescale.split('/')
        l1_prescale = int(l1_prescale)
        l1_threshold = int(l1_path.split('L1_HTT')[1])
        if l1_prescale == 1 and l1_threshold < lowest_l1_threshold:
            lowest_l1_threshold = l1_threshold
        l1_prescales.append((l1_threshold, l1_prescale))
    l1_prescales.sort()
    assert [t for t,p in l1_prescales] == [160, 200, 220, 240, 255, 270, 280, 300, 320]
    changes[run][ls] = lowest_l1_threshold

ll_by_thresh = defaultdict(LumiList)

for run in sorted(changes.keys()):
    assert changes[run].has_key(1)
    ls_thresh = sorted(changes[run].items())
    nchanges = len(ls_thresh)
    for i, (ls, thresh) in enumerate(ls_thresh):
        if i == nchanges - 1:
            end_ls = maxls[run]
        else:
            end_ls = ls_thresh[i+1][0] - 1
        ll_by_thresh[thresh] += LumiList(compactList={run: [[ls, end_ls]]})

for thresh, ll in ll_by_thresh.iteritems():
    (golden & ll).writeJSON('PFHT900_L1%i.json' % thresh)
