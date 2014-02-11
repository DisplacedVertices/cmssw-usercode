import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.source.fileNames = ['/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/F4E63CCC-8318-E211-8C79-0030487F1A57.root']
process.source.fileNames = ['/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-1000_MFF-20_CTau1p5To150_8TeV-pythia6/AODSIM/DEBUG_PU_S10_START53_V7A-v2/0000/E80ADAD3-EEF0-E111-B106-003048F0E55A.root']
process.TFileService.fileName = 'fit.root'

if 0:
    process.source.fileNames = '''/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/F4E63CCC-8318-E211-8C79-0030487F1A57.root
/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/E6193B70-8018-E211-8C2C-003048C69404.root
/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/D65AF29A-8618-E211-BE62-0030487F1309.root
/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/D20535AF-8318-E211-8DD4-0030487F1A3F.root
/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/AE4F435F-7C18-E211-8278-0030487F1C57.root
/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/8685F844-8818-E211-902F-0030487F1F23.root
/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/80A0705C-7518-E211-A17D-0030487E4D11.root
/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/7E17F3D4-8218-E211-82AF-003048C69404.root
/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/7C46A3E8-5F18-E211-B872-0030487E4D11.root
/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/72C3D631-7A18-E211-BD88-0030487D8661.root
/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/6C5E2583-7718-E211-A85E-0030487E4D11.root
/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/4E2DECAF-8C18-E211-B118-0030487D858B.root
/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/409BEF3F-7B18-E211-8F47-0030487F1A4F.root
/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/3EDEF6AB-8A18-E211-9F02-0030487D5E4B.root
/store/mc/Summer12_DR53X/HTo2LongLivedTo4F_MH-400_MFF-50_CTau8To800_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/3EC3CCE5-8118-E211-84DF-003048C69404.root'''.split('\n')

process.a = cms.EDProducer('MFVDispJetsPlay')

process.p = cms.Path(process.a)

idses = '''1113 1113
1113 1114
1114 1114
2113 2113
2113 2114
2114 2114
3113 3113
3113 3114
3114 3114
1 0
2 0
3 0'''.split('\n')

for ids in idses:
    ids = ids.strip().split()
    a = int(ids[0])
    b = int(ids[1])
    filt = cms.EDFilter('MFVDispJetsFilter', a = cms.int32(a), b = cms.int32(b))
    ana = cms.EDProducer('MFVDispJetsPlay')
    path = cms.Path(filt * ana)
    setattr(process, 'filt%i%i' % (a,b), filt)
    setattr(process, 'anal%i%i' % (a,b), ana)
    setattr(process, 'path%i%i' % (a,b), path)

process.options.wantSummary = True

debug = 'debug' in sys.argv
if debug:
    process.a.debug = cms.untracked.bool(True)
    process.load('JMTucker.Tools.ParticleListDrawer_cff')
    process.p.insert(0, process.ParticleListDrawer)
