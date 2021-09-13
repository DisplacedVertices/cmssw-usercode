#!/usr/bin/env python

from JMTucker.MFVNeutralino.UtilitiesBase import *

####

_leptonpresel = bool_from_argv('leptonpresel')
_metpresel = bool_from_argv('metpresel')
_presel_s = '_leptonpresel' if _leptonpresel else '_metpresel' if _metpresel else ''

####

def cmd_hadd_vertexer_histos():
    ntuple = sys.argv[2]
    print(ntuple)
    samples = Samples.registry.from_argv(
            Samples.qcd_samples_2017 + Samples.met_samples_2017 + Samples.Zvv_samples_2017 + Samples.mfv_splitSUSY_samples_M2000_2017
            #Samples.data_samples_2015 + \
            #Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015 + \
            #Samples.data_samples + \
            #Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext
    )
    for s in samples:
        s.set_curr_dataset(ntuple)
        hadd(s.name + '.root', ['root://cmseos.fnal.gov/' + fn.replace('ntuple', 'vertex_histos') for fn in s.filenames])

def cmd_report_data():
    for ds, ex in ('SingleMuon', '_mu'), ('JetHT', ''), ('SingleElectron', '_ele'):
        maod = 'miniaod' if 'miniaod' in sys.argv else ''
        pc = ''
        if '10pc' in sys.argv:
            pc = '10pc'
            ex += '_10pc'
        elif '1pc' in sys.argv:
            pc = '1pc'
            ex += '_1pc'

        for year in 2017, 2018:
            if not glob('*%s%i*' % (ds, year)):
                continue

            os.system('mreport c*_%s%i* %s %s' % (ds, year, pc, maod))
            json_fn = 'processedLumis.json'
            if not os.path.isfile(json_fn):
                raise IOError('something went wrong with mreport?')

            print 'jsondiff'
            avail_fn = json_path('ana_avail_%i%s.json' % (year, ex))
            ok = False
            if not os.path.isfile(avail_fn):
                if raw_input('no file %s, enter y to create it: ' % avail_fn)[0] == 'y':
                    shutil.copy(json_fn, avail_fn)
                    ok = True
            else:
                os.system('compareJSON.py --diff %s %s' % (json_fn, avail_fn))
                if raw_input('enter y if ok: ') == 'y':
                    ok = True
            if ok:
                os.rename('processedLumis.json', 'dataok_%i.json' % year)
            else:
                bad_fn = '%s.bad.%i' % (json_fn, int(time()))
                print 'saving %s as %s' % (json_fn, bad_fn)
                os.rename(json_fn, bad_fn)

def cmd_hadd_data():
    permissive = bool_from_argv('permissive')
    for ds in 'SingleMuon', 'JetHT', 'ZeroBias', 'SingleElectron':
        print ds
        files = set(glob(ds + '*.root'))
        if not files:
            print 'no files for this ds'
            continue

        have = []
        year_eras = [
            ('2017', 'BCDEF'),
            ('2018', 'ABCD'),
            ]

        for year, eras in year_eras:
            files = [f for x in eras for f in glob('%s%s%s.root' % (ds, year, x))]
            ok = len(files) == len(eras)
            if not ok:
                print 'some files missing for %s %s: only have %r' % (ds, year, files)
            if ok or permissive:
                hadd_or_merge('%s%s.root' % (ds, year), files)
                have.append(year)

        if '2017' in have and '2018' in have:
            hadd_or_merge(ds + '2017p8.root', ['%s%s.root' % (ds, year) for year in '2017', '2018'])

cmd_merge_data = cmd_hadd_data

def _mc_parts():
  for year in [2017,2018]:
    if year == 2017:
        #for base in 'dyjetstollM50', 'wjetstolnu':
        base = 'qcdht0500'
    elif year == 2018:
        base == 'qcdht0200'
    a = '%s_%s.root' % (base, year)
    b = '%sext_%s.root' % (base, year)
    c = '%ssum_%s.root' % (base, year)
    yield (year,base), (a,b,c)

def cmd_hadd_mc_sums():
    for (year,base), (a,b,c) in _mc_parts():
        if not os.path.isfile(a) or not os.path.isfile(b):
            print 'skipping', year, base, 'because at least one input file missing'
        elif os.path.isfile(c):
            print 'skipping', year, base, 'because', c, 'already exists'
        else:
            hadd_or_merge(c, [a, b])

cmd_merge_mc_sums = cmd_hadd_mc_sums

def cmd_rm_mc_parts():
    for (year,base), (a,b,c) in _mc_parts():
        if os.path.isfile(c):
            for y in a,b:
                if os.path.isfile(y):
                    print y
                    os.remove(y)

def _background_samples(trigeff=False, year=2017):
    if _leptonpresel or trigeff:
        #x = ['ttbar', 'wjetstolnu', 'dyjetstollM10', 'dyjetstollM50', 'qcdmupt15']
        x = ['ttbar', 'wjetstolnu', 'dyjetstollM10', 'dyjetstollM50']
        if not trigeff:
            x += ['qcdempt%03i' % x for x in [15,20,30,50,80,120,170,300]]
            x += ['qcdbctoept%03i' % x for x in [15,20,30,80,170,250]]
    elif _metpresel:
        x = ['ttbar', 'wjetstolnu']
        x += ['qcdht%04i' % x for x in [200, 300, 500, 700, 1000, 1500, 2000]]
        x += ['zjetstonunuht%04i' % x for x in [100, 200, 400, 600, 800, 1200, 2500]]
        if year==2017:
          x += ['qcdht0200', 'qcdht0500sum']
        elif year==2018:
          x += ['qcdht0200sum', 'qcdht0500']
    else:
        x = ['qcdht%04i' % x for x in [700, 1000, 1500, 2000]]
        x += ['ttbarht%04i' % x for x in [600, 800, 1200, 2500]]
    return x

def cmd_merge_background(permissive=bool_from_argv('permissive'), year_to_use=2017):
    cwd = os.getcwd()
    ok = True
    if year_to_use==-1:
      for year_s, scale in [('_2017', -AnalysisConstants.int_lumi_2017 * AnalysisConstants.scale_factor_2017),
                            ('_2018', -AnalysisConstants.int_lumi_2018 * AnalysisConstants.scale_factor_2018)]:
  
          year = int(year_s[1:])
          print 'scaling to', year, scale
  
          files = _background_samples(year=year)
          files = ['%s%s.root' % (x, year_s) for x in files]
          files2 = []
          for fn in files:
              if not os.path.isfile(fn):
                  msg = '%s not found' % fn
                  if permissive:
                      print msg
                  else:
                      raise RuntimeError(msg)
              else:
                  files2.append(fn)
          if files2:
              cmd = 'samples merge %f background%s%s.root ' % (scale, _presel_s, year_s)
              cmd += ' '.join(files2)
              print cmd
              if os.system(cmd) != 0:
                  ok = False
      if ok:
          cmd = 'hadd.py background_2017p8.root background_2017.root background_2018.root'
          print cmd
          os.system(cmd)

    else:
        if year_to_use==2017:
            year_s = '_2017'
            scale = -AnalysisConstants.int_lumi_2017 * AnalysisConstants.scale_factor_2017
        elif year_to_use==2018:
            year_s = '_2018'
            scale = -AnalysisConstants.int_lumi_2018 * AnalysisConstants.scale_factor_2018
        else:
            raise RuntimeError("Year {0} not available!".format(year_to_use))
  
        year = int(year_s[1:])
        print 'scaling to', year, scale
  
        files = _background_samples(year=year)
        files = ['%s%s.root' % (x, year_s) for x in files]
        files2 = []
        for fn in files:
            if not os.path.isfile(fn):
                msg = '%s not found' % fn
                if permissive:
                    print msg
                else:
                    raise RuntimeError(msg)
            else:
                files2.append(fn)
        if files2:
            cmd = 'samples merge %f background%s%s.root ' % (scale, _presel_s, year_s)
            cmd += ' '.join(files2)
            print cmd
            if os.system(cmd) != 0:
                ok = False
        if ok:
            print ("{0} background merged!".format(year))

    #only work for 2017 data now
    #if ok:
    #    cmd = 'hadd.py background%s_2017p8.root background%s_2017.root background%s_2018.root' % (_presel_s, _presel_s, _presel_s)
    #    print cmd
    #    os.system(cmd)

def cmd_effsprint(year_to_use=2017):
    if year_to_use==-1:
        for year in 2017, 2018:
            background_fns = ' '.join('%s_%s.root' % (x, year) for x in _background_samples(year=year))
            todo = [('background', background_fns), ('signals', 'mfv*%s.root' % year)]
            def do(cmd, outfn):
                cmd = 'python %s %s %s' % (cmssw_base('src/JMTucker/MFVNeutralino/test/effsprint.py'), cmd, year)
                print cmd
                os.system('%s | tee %s' % (cmd, outfn))
                print
            for which, which_files in todo:
                for ntk in 3,4,'3or4',5:
                    for vtx in 1,2:
                        cmd = 'ntk%s' % ntk
                        if which == 'background':
                            cmd += ' sum'
                        if vtx == 1:
                            cmd += ' one'
                        cmd += ' ' + which_files
                        outfn = 'effsprint_%s%s_%s_ntk%s_%iv' % (which, _presel_s, year, ntk, vtx)
                        do(cmd, outfn)
            do('presel sum ' + background_fns, 'effsprint_presel_%s' % year)
            do('nocuts sum ' + background_fns, 'effsprint_nocuts_%s' % year)
    else:
        if year_to_use!=2017 and year_to_use!=2018:
            raise RuntimeError("Year {0} not available!".format(year_to_use))
        year = year_to_use
        background_fns = ' '.join('%s_%s.root' % (x, year) for x in _background_samples(year=year))
        todo = [('background', background_fns), ('signals', 'mfv*%s.root' % year)]
        def do(cmd, outfn):
            cmd = 'python %s %s %s' % (cmssw_base('src/JMTucker/MFVNeutralino/test/effsprint.py'), cmd, year)
            print cmd
            os.system('%s | tee %s' % (cmd, outfn))
            print
        for which, which_files in todo:
            for ntk in 3,4,'3or4',5:
                for vtx in 1,2:
                    cmd = 'ntk%s' % ntk
                    if which == 'background':
                        cmd += ' sum'
                    if vtx == 1:
                        cmd += ' one'
                    cmd += ' ' + which_files
                    outfn = 'effsprint_%s%s_%s_ntk%s_%iv' % (which, _presel_s, year, ntk, vtx)
                    do(cmd, outfn)
            # A B C D region effsprint
            for reg in ['A', 'B', 'C', 'D']:
                cmd = 'ntk5 '
                cmd += reg
                if which == 'background':
                    cmd += ' sum'
                cmd += ' ' + which_files
                outfn = 'effsprint_%s%s_%s_region%s' % (which, _presel_s, year, reg)
                do(cmd, outfn)
                
        do('presel sum ' + background_fns, 'effsprint_presel_%s' % year)
        do('nocuts sum ' + background_fns, 'effsprint_nocuts_%s' % year)


def cmd_histos():
    cmd_report_data()
    cmd_hadd_data()
    cmd_merge_background()
    cmd_effsprint()

def cmd_presel():
    cmd_report_data()
    cmd_hadd_data()
    cmd_merge_background()

def cmd_vpeffs():
    cmd_report_data()
    cmd_hadd_data()
    cmd_merge_background()

def cmd_minitree():
    cmd_report_data()
    cmd_hadd_data()

def cmd_trackmover():
    cmd_report_data()
    cmd_hadd_data()

def cmd_trackmoverhists():
    cmd_hadd_data()
    cmd_merge_background()

def cmd_k0hists():
    cmd_hadd_data()
    cmd_merge_background(True)

def cmd_trigeff():
    cmd_hadd_mc_sums()
    if glob('*SingleMuon*') or glob('*SingleElectron*'):
        cmd_report_data()
        cmd_hadd_data()
    cmd_trigeff_merge()

def cmd_trigeff_merge():
    permissive = bool_from_argv('permissive')
    print colors.yellow('using *_2017* for 2018')
    for year_s, scale in ('_2017', -AnalysisConstants.int_lumi_2017), ('_2018', -AnalysisConstants.int_lumi_2018):
        for wqcd_s in '', '_wqcd':
            files = _background_samples(trigeff=True)
            #if not wqcd_s:
            #    files.remove('qcdmupt15')
            files = ['%s%s.root' % (x, '_2017') for x in files]
            files2 = []
            for fn in files:
                if not os.path.isfile(fn):
                    msg = '%s not found' % fn
                    if permissive:
                        print msg
                    else:
                        raise RuntimeError(msg)
                else:
                    files2.append(fn)

            if files2:
                out_fn = 'background%s%s.root' % (wqcd_s, year_s)
                if os.path.exists(out_fn):
                    print colors.yellow('skipping %s because it exists' % out_fn)
                else:
                    cmd = 'samples merge %f %s %s' % (scale, out_fn, ' '.join(files2))
                    print cmd
                    os.system(cmd)

####

if __name__ == '__main__':
    main(locals())

