from sys import argv
from collections import defaultdict
from datetime import datetime
from DVCode.Tools import DBS, colors, Samples

at_sites = ['T3_US_FNALLPC', 'T1_US_FNAL_Disk', 'T2_DE_DESY', 'T2_US_MIT', 'T2_US_Florida', 'T2_US_Nebraska', 'T2_US_Purdue', 'T2_US_Wisconsin'] # ordered by priority
at = { x:defaultdict(list) for x in at_sites }

if 'main' in argv:
    dses = ['main']
else:
    dses = ['miniaod']

for ds in dses:
    print colors.bold(ds)
    for sample in Samples.registry.all():
        equally_good = []

        if not sample.has_dataset(ds):
            continue

        sample.set_curr_dataset(ds)
        if '/None/' in sample.dataset or getattr(sample, 'is_private', False):
            continue

        try:
            sites = DBS.sites_for_dataset(sample.dataset, instance=sample.dbs_inst, json=True)
        except (RuntimeError, ValueError):
            print colors.yellow('%s %s DBS problem' % (sample.name, sample.dataset))
            continue

        if not sites:
            continue

        print sample.name,
        sites.sort(key=lambda site: DBS.site_completions(site, True))
        max_site_completion = DBS.site_completions(sites[-1], True)
        found = False
        for site in sites:
            if DBS.site_is_tape(site):
                continue

            is_complete = DBS.complete_at_site(site)
            is_good_as_possible = DBS.site_completions(site) >= max_site_completion
            if is_complete:
                color = colors.green
            elif is_good_as_possible:
                color = colors.yellow
            else:
                color = colors.red
            print color(DBS.site_completions_string(site)),

            if is_good_as_possible:
                for at_site in at_sites:
                    if site['name'] == at_site:
                        equally_good.append(at_site)

        for at_site in at_sites : 
            if at_site in equally_good :
                at[at_site][ds].append(sample.name)
                break
        print

print '# %s' % datetime.now()
print 'condorable = {'
for k,v in at.iteritems():
    print '    "%s": {' % k
    for k2,v2 in v.iteritems():
        print '        "%s": [%s],' % (k2, ', '.join(v2))
    print '},'
print '}'
