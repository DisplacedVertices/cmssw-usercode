import csv
from pprint import pprint
from itertools import izip
from collections import defaultdict
from DVCode.Tools.LumiJSONTools import LumiList

name, csv_fn, json_fn, hlt_path_base, l1_path_base, l1_thresholds_possible = 'PFHT800_2015', 'PFHT800_2015.txt', '../2015.json', 'HLT_PFHT800_v', 'L1_HTT', lambda x: x == [100, 125, 150, 175] or x == [150, 175]
name, csv_fn, json_fn, hlt_path_base, l1_path_base, l1_thresholds_possible = 'PFHT800_2016', 'PFHT800_2016.txt', '../2016.json', 'HLT_PFHT800_v', 'L1_HTT', lambda x: x == [160, 200, 220, 240, 255, 270, 280, 300, 320]
name, csv_fn, json_fn, hlt_path_base, l1_path_base, l1_thresholds_possible = 'PFJet450_2015', 'PFJet450_2015.txt', '../2015.json', 'HLT_PFJet450_v', 'L1_SingleJet', lambda x: x == [128, 200] or x == [200]
name, csv_fn, json_fn, hlt_path_base, l1_path_base, l1_thresholds_possible = 'PFJet450_2016', 'PFJet450_2016.txt', '../2016.json', 'HLT_PFJet450_v', 'L1_SingleJet', lambda x: x == [170, 180, 200] or x == [170]
name, csv_fn, json_fn, hlt_path_base, l1_path_base, l1_thresholds_possible = 'AK8PFJet450', 'AK8PFJet450.txt', '../2016.json', 'HLT_AK8PFJet450_v', 'L1_SingleJet', lambda x: x == [170, 180, 200] or x == [170]
name, csv_fn, json_fn, hlt_path_base, l1_path_base, l1_thresholds_possible = 'PFHT900', 'PFHT900.txt', '../2016.json', 'HLT_PFHT900_v', 'L1_HTT', lambda x: x == [160, 200, 220, 240, 255, 270, 280, 300, 320]

json = LumiList(json_fn)
minls, maxls = defaultdict(lambda: 999999), defaultdict(int)
for run, ls in json.getLumis():
    if ls > maxls[run]:
        maxls[run] = ls
    if ls < minls[run]:
        minls[run] = ls

with open(csv_fn, 'rb') as f:
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
    hlt_version = int(hlt_path.split(hlt_path_base)[1])
    assert hlt_prescale == 1
    assert logic == 'OR' or logic == 'ONE'
    l1_prescales = []
    lowest_l1_threshold = 999
    for l1_path_prescale in l1_paths_prescale.split():
        l1_path, l1_prescale = l1_path_prescale.split('/')
        l1_prescale = int(l1_prescale)
        l1_threshold = int(l1_path.split(l1_path_base)[1])
        if l1_prescale == 1 and l1_threshold < lowest_l1_threshold:
            lowest_l1_threshold = l1_threshold
        l1_prescales.append((l1_threshold, l1_prescale))
    l1_prescales.sort()
    #print row, '\n\t', lowest_l1_threshold
    assert l1_thresholds_possible([t for t,p in l1_prescales])
    changes[run][ls] = (lowest_l1_threshold, l1_prescales)

ll_by_lowest_thresh = defaultdict(LumiList)
ll_by_unprescaled_thresh = defaultdict(LumiList)

for run in sorted(changes.keys()):
    ls_thresh = sorted(changes[run].items())
    assert ls_thresh[0][0] <= minls[run]
    nchanges = len(ls_thresh)
    for i, (ls, (lowest_thresh, prescales)) in enumerate(ls_thresh):
        if i == nchanges - 1:
            end_ls = maxls[run]
        else:
            end_ls = ls_thresh[i+1][0] - 1
        ll_by_lowest_thresh[lowest_thresh] += LumiList(compactList={run: [[ls, end_ls]]})
        for thresh, prescale in prescales:
            if prescale == 1:
                ll_by_unprescaled_thresh[thresh] += LumiList(compactList={run: [[ls, end_ls]]})

for thresh, ll in ll_by_lowest_thresh.iteritems():
    (json & ll).writeJSON('%s_lowestL1%i.json' % (name, thresh))

for thresh, ll in ll_by_unprescaled_thresh.iteritems():
    if ll == json:
        print thresh, 'is a winner'
    (json & ll).writeJSON('%s_unprescaledL1%i.json' % (name, thresh))
