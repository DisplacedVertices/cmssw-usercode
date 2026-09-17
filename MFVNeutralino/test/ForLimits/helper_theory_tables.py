from __future__ import print_function
import csv as _csv

import nuisance_configs as ns_conf


def load_fac_scale_VH_table(csv_path):
    """Parse fac_scale_shape_bins.csv into {(mass_gev, ctau_um, year): ([kup_b0..b3], [kdn_b0..b3])}.
    Kappas are the ZH/W+H/W-H yield-weighted average; low_bin-flagged bins are forced to 1.0."""
    NBINS_CSV = 4
    NBINS_ALL = 4

    raw = {}
    with open(csv_path) as f:
        for r in _csv.DictReader(f):
            key = (int(r['mass_gev']), int(r['ctau_um']), r['year'])
            entry = {}
            for b in range(NBINS_CSV):
                if r['flags_bin%d' % b] == 'ok':
                    entry[b] = (float(r['kappa_up_bin%d' % b]),
                                float(r['kappa_dn_bin%d' % b]),
                                int(r['n_bin%d' % b]))
                else:
                    entry[b] = (1.0, 1.0, 0)
            raw.setdefault(key, {})[r['stype']] = entry

    table = {}
    for key, stypes_d in raw.items():
        kup, kdn = [], []
        for b in range(NBINS_ALL):
            if b >= NBINS_CSV:
                kup.append(1.0)
                kdn.append(1.0)
                continue
            total_n = sum_ku = sum_kd = 0.0
            for st in ('ZH', 'WplusH', 'WminusH'):
                ku, kd, n = stypes_d.get(st, {}).get(b, (1.0, 1.0, 0))
                sum_ku += ku * n
                sum_kd += kd * n
                total_n += n
            if total_n > 0:
                kup.append(sum_ku / total_n)
                kdn.append(sum_kd / total_n)
            else:
                kup.append(1.0)
                kdn.append(1.0)
        table[key] = (kup, kdn)
    return table


_fac_scale_VH_table = None


def get_fac_scale_VH_table():
    global _fac_scale_VH_table
    if _fac_scale_VH_table is None:
        _fac_scale_VH_table = load_fac_scale_VH_table(ns_conf.fac_scale_VH_csv_path)
    return _fac_scale_VH_table
