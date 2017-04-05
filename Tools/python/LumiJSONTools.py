#! /usr/bin/env python

import ast
from FWCore.PythonUtilities.XML2Python import xml2obj
from FWCore.PythonUtilities.LumiList import LumiList

def fjr2ll(fjr_fn):
    '''Ripped off from fjr2json.py that comes with CMSSW.'''

    runsLumisDict = {}
    obj = xml2obj(filename=fjr_fn)
    for inputFile in obj.InputFile:
        if not inputFile.Runs:
            assert inputFile.Runs == ''
        else:
            try: # Regular XML version, assume only one of these
                runObjects = inputFile.Runs.Run
                for run in runObjects:
                    runNumber = int(run.ID)
                    runList = runsLumisDict.setdefault(runNumber, [])
                    for lumiPiece in run.LumiSection:
                        lumi = int(lumiPiece.ID)
                        runList.append(lumi)
            except:
                if isinstance(inputFile.Runs, basestring):
                    runObjects = [inputFile.Runs]
                else:
                    runObjects = inputFile.Runs

                for runObject in runObjects:
                    try:
                        runs = ast.literal_eval(runObject)
                        for run, lumis in runs.iteritems():
                            runList = runsLumisDict.setdefault(int(run), [])
                            runList.extend(lumis)
                    except ValueError: # Old style handled above
                        pass

    return LumiList(runsAndLumis=runsLumisDict)
