import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

### Signals, 25 ns

#ZprimeToTT_M2000_W200 = kreator.makeMCComponent("ZprimeToTT_M2000_W200", "/ZprimeToTT_M-2000_W-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM", "CMS", ".*root", 1.0, useAAA=True)
#SMS_T2bb_2J_mStop600_mLSP580 = kreator.makeMyPrivateMCComponent("SMS_T2bb_2J_mStop600_mLSP580", "/SMS-T2bb_2J_mStop-600_mLSP-580_Tune4C_13TeV-madgraph-tauola/namin-step3-fb89f44b0d6970d718ed21d513cd1c9d/USER", "PRIVATE", ".*root", "phys03", 0.174599, useAAA=True)

### ----------------------------- summary ----------------------------------------

samples_stopsDilepton = []

JetHT_260431_M2_5_500 = kreator.makeMyPrivateMCComponent("JetHT_260431_M2_5_500", "/JetHT/schoef-crab_JetHT_Run2015D_M2_5_500_lumiBased_reduced-8e13882dc7c4566a38618e8b59bae173/USER", "PRIVATE", ".*root", "phys03", 1, useAAA=True)
JetHT_260431          = kreator.makeMyPrivateMCComponent("JetHT_260431", "/JetHT/schoef-crab_JetHT_Run2015D_lumiBased_reduced-4fff70efe810c67b5c65aa7d4a7cd41d/USER", "PRIVATE", ".*root", "phys03", 1, useAAA=True)

samples_data_private = [
JetHT_260431_M2_5_500,
JetHT_260431,
]


QCD_Pt_15to3000 = kreator.makeMyPrivateMCComponent("QCD_Pt_15to3000", "/QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8/schoef-crab_QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8-5dafd396af9e4f54f380247389303774/USER", "PRIVATE", ".*root", "phys03", 1, useAAA=True)
QCD_Pt_15to3000_M2_5_500 = kreator.makeMyPrivateMCComponent("QCD_Pt_15to3000_M2_5_500", "/QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8/schoef-crab_QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8_M2_5_500-5dafd396af9e4f54f380247389303774/USER", "PRIVATE", ".*root", "phys03", 1, useAAA=True)

QCD_Pt_15to3000_M0   = kreator.makeMyPrivateMCComponent("QCD_Pt_15to3000_M0", "/QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8/schoef-crab_QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8_M0-5dafd396af9e4f54f380247389303774/USER", "PRIVATE", ".*root", "phys03", 1, useAAA=True)
QCD_Pt_15to3000_M21p = kreator.makeMyPrivateMCComponent("QCD_Pt_15to3000_M21p", "/QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8/schoef-crab_QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8_M21p-5dafd396af9e4f54f380247389303774/USER", "PRIVATE", ".*root", "phys03", 1, useAAA=True)
QCD_Pt_15to3000_M23p = kreator.makeMyPrivateMCComponent("QCD_Pt_15to3000_M23p", "/QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8/schoef-crab_QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8_M23p-5dafd396af9e4f54f380247389303774/USER", "PRIVATE", ".*root", "phys03", 1, useAAA=True)


samples_mc_private = [
QCD_Pt_15to3000,
QCD_Pt_15to3000_M2_5_500,
#QCD_Pt_15to3000_M2_0_500,
#QCD_Pt_15to3000_M2_5_100,
QCD_Pt_15to3000_M0,
QCD_Pt_15to3000_M21p,
QCD_Pt_15to3000_M23p,
]

samples = samples_stopsDilepton + samples_data_private + samples_mc_private

for sample in samples_mc_private:
    sample.isMC = True 
    sample.isData = False

for sample in samples_data_private:
    sample.isMC = False
    sample.isData = True

### ---------------------------------------------------------------------

from CMGTools.TTHAnalysis.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"

#Define splitting
for comp in samples:
    comp.splitFactor = 250 
    comp.puFileMC=dataDir+"/puProfile_Summer12_53X.root"
    comp.puFileData=dataDir+"/puProfile_Data12.root"
    comp.efficiency = eff2012
