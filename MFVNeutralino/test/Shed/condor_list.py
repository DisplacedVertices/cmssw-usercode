from collections import defaultdict
from datetime import datetime
from JMTucker.Tools import DBS, colors, Samples

at_sites = ['T3_US_FNALLPC', 'T1_US_FNAL_Disk', 'T2_DE_DESY'] # ordered by priority
at = { x:defaultdict(list) for x in at_sites }

for ds in 'main', 'miniaod':
    print colors.bold(ds)
    for sample in Samples.registry.all():
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
                        at[site['name']][ds].append(sample.name)
                        found = True
            if found:
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
