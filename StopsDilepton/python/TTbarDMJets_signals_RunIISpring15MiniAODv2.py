import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

### ----------------------------- 25 ns ----------------------------------------
# TTbar cross section: NNLO, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO (172.5)

TTbarDMJets_pseudoscalar_Mchi1_Mphi10       = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi1_Mphi10", "/TTbarDMJets_pseudoscalar_Mchi-1_Mphi-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM", "CMS", ".*root", 0.4517)
TTbarDMJets_pseudoscalar_Mchi1_Mphi20       = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi1_Mphi20", "/TTbarDMJets_pseudoscalar_Mchi-1_Mphi-20_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 4.117e-01)
TTbarDMJets_pseudoscalar_Mchi1_Mphi50       = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi1_Mphi50", "/TTbarDMJets_pseudoscalar_Mchi-1_Mphi-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 3.080e-01)
TTbarDMJets_pseudoscalar_Mchi1_Mphi100      = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi1_Mphi100", "/TTbarDMJets_pseudoscalar_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 0.1932)
TTbarDMJets_pseudoscalar_Mchi1_Mphi200      = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi1_Mphi200", "/TTbarDMJets_pseudoscalar_Mchi-1_Mphi-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 8.786e-02)
TTbarDMJets_pseudoscalar_Mchi1_Mphi300      = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi1_Mphi300", "/TTbarDMJets_pseudoscalar_Mchi-1_Mphi-300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 3.950e-02)
TTbarDMJets_pseudoscalar_Mchi1_Mphi500      = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi1_Mphi500", "/TTbarDMJets_pseudoscalar_Mchi-1_Mphi-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 5.163e-03)
TTbarDMJets_pseudoscalar_Mchi10_Mphi10      = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi10_Mphi10", "/TTbarDMJets_pseudoscalar_Mchi-10_Mphi-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 0.01522)
TTbarDMJets_pseudoscalar_Mchi10_Mphi50      = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi10_Mphi50", "/TTbarDMJets_pseudoscalar_Mchi-10_Mphi-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM", "CMS", ".*root", 3.091e-01)
TTbarDMJets_pseudoscalar_Mchi10_Mphi100     = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi10_Mphi100", "/TTbarDMJets_pseudoscalar_Mchi-10_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 0.1976)
TTbarDMJets_pseudoscalar_Mchi50_Mphi50      = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi50_Mphi50", "/TTbarDMJets_pseudoscalar_Mchi-50_Mphi-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 2.928e-03)
TTbarDMJets_pseudoscalar_Mchi50_Mphi200     = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi50_Mphi200", "/TTbarDMJets_pseudoscalar_Mchi-50_Mphi-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 0.08476)
TTbarDMJets_pseudoscalar_Mchi50_Mphi300     = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi50_Mphi300", "/TTbarDMJets_pseudoscalar_Mchi-50_Mphi-300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 3.845e-02)
TTbarDMJets_pseudoscalar_Mchi150_Mphi200    = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi150_Mphi200", "/TTbarDMJets_pseudoscalar_Mchi-150_Mphi-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root",  3.955e-04)
TTbarDMJets_pseudoscalar_Mchi150_Mphi500    = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi150_Mphi500", "/TTbarDMJets_pseudoscalar_Mchi-150_Mphi-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 4.400e-03)
TTbarDMJets_pseudoscalar_Mchi150_Mphi1000   = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi150_Mphi1000", "/TTbarDMJets_pseudoscalar_Mchi-150_Mphi-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 0.0003392)
TTbarDMJets_pseudoscalar_Mchi500_Mphi500    = kreator.makeMCComponent("TTbarDMJets_pseudoscalar_Mchi500_Mphi500", "/TTbarDMJets_pseudoscalar_Mchi-500_Mphi-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM", "CMS", ".*root", 2.904e-06)
TTbarDMJets_scalar_Mchi1_Mphi10             = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi1_Mphi10", "/TTbarDMJets_scalar_Mchi-1_Mphi-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 21.36)
TTbarDMJets_scalar_Mchi1_Mphi20             = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi1_Mphi20", "/TTbarDMJets_scalar_Mchi-1_Mphi-20_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 1.095e+01)
TTbarDMJets_scalar_Mchi1_Mphi50             = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi1_Mphi50", "/TTbarDMJets_scalar_Mchi-1_Mphi-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 3.088e+00)
TTbarDMJets_scalar_Mchi1_Mphi100            = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi1_Mphi100", "/TTbarDMJets_scalar_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 7.205e-01)
TTbarDMJets_scalar_Mchi1_Mphi200            = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi1_Mphi200", "/TTbarDMJets_scalar_Mchi-1_Mphi-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 1.016e-01)
TTbarDMJets_scalar_Mchi1_Mphi300            = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi1_Mphi300", "/TTbarDMJets_scalar_Mchi-1_Mphi-300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 0.03045)
TTbarDMJets_scalar_Mchi1_Mphi500            = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi1_Mphi500", "/TTbarDMJets_scalar_Mchi-1_Mphi-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 4.947e-03)
TTbarDMJets_scalar_Mchi1_Mphi1000           = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi1_Mphi1000", "/TTbarDMJets_scalar_Mchi-1_Mphi-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 3.265e-04)
TTbarDMJets_scalar_Mchi10_Mphi10            = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi10_Mphi10", "/TTbarDMJets_scalar_Mchi-10_Mphi-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM", "CMS", ".*root", 1.011e-01)
TTbarDMJets_scalar_Mchi10_Mphi50            = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi10_Mphi50", "/TTbarDMJets_scalar_Mchi-10_Mphi-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 3.097e+00)
TTbarDMJets_scalar_Mchi10_Mphi100           = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi10_Mphi100", "/TTbarDMJets_scalar_Mchi-10_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 7.417e-01)
TTbarDMJets_scalar_Mchi50_Mphi200           = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi50_Mphi200", "/TTbarDMJets_scalar_Mchi-50_Mphi-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 1.003e-01)
TTbarDMJets_scalar_Mchi50_Mphi300           = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi50_Mphi300", "/TTbarDMJets_scalar_Mchi-50_Mphi-300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 3.046e-02)
TTbarDMJets_scalar_Mchi50_Mphi50            = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi50_Mphi50", "/TTbarDMJets_scalar_Mchi-50_Mphi-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 0.0027578)
TTbarDMJets_scalar_Mchi150_Mphi200          = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi150_Mphi200", "/TTbarDMJets_scalar_Mchi-150_Mphi-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 0.0001313)
TTbarDMJets_scalar_Mchi500_Mphi500          = kreator.makeMCComponent("TTbarDMJets_scalar_Mchi500_Mphi500", "/TTbarDMJets_scalar_Mchi-500_Mphi-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", "CMS", ".*root", 8.888e-07)

samples = [TTbarDMJets_pseudoscalar_Mchi1_Mphi10, TTbarDMJets_pseudoscalar_Mchi1_Mphi20, TTbarDMJets_pseudoscalar_Mchi1_Mphi50, TTbarDMJets_pseudoscalar_Mchi1_Mphi100, TTbarDMJets_pseudoscalar_Mchi1_Mphi200, TTbarDMJets_pseudoscalar_Mchi1_Mphi300, TTbarDMJets_pseudoscalar_Mchi1_Mphi500, TTbarDMJets_pseudoscalar_Mchi10_Mphi10, TTbarDMJets_pseudoscalar_Mchi10_Mphi50, TTbarDMJets_pseudoscalar_Mchi10_Mphi100, TTbarDMJets_pseudoscalar_Mchi50_Mphi50, TTbarDMJets_pseudoscalar_Mchi50_Mphi200, TTbarDMJets_pseudoscalar_Mchi50_Mphi300, TTbarDMJets_pseudoscalar_Mchi150_Mphi200, TTbarDMJets_pseudoscalar_Mchi150_Mphi500, TTbarDMJets_pseudoscalar_Mchi150_Mphi1000, TTbarDMJets_pseudoscalar_Mchi500_Mphi500, TTbarDMJets_scalar_Mchi1_Mphi10, TTbarDMJets_scalar_Mchi1_Mphi20, TTbarDMJets_scalar_Mchi1_Mphi50, TTbarDMJets_scalar_Mchi1_Mphi100, TTbarDMJets_scalar_Mchi1_Mphi200, TTbarDMJets_scalar_Mchi1_Mphi300, TTbarDMJets_scalar_Mchi1_Mphi500, TTbarDMJets_scalar_Mchi1_Mphi1000, TTbarDMJets_scalar_Mchi10_Mphi10, TTbarDMJets_scalar_Mchi10_Mphi50, TTbarDMJets_scalar_Mchi10_Mphi100, TTbarDMJets_scalar_Mchi50_Mphi200, TTbarDMJets_scalar_Mchi50_Mphi300, TTbarDMJets_scalar_Mchi50_Mphi50, TTbarDMJets_scalar_Mchi150_Mphi200, TTbarDMJets_scalar_Mchi500_Mphi500] 

### ---------------------------------------------------------------------

from CMGTools.TTHAnalysis.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"

#Define splitting
for comp in samples:
    comp.isMC = True
    comp.isData = False
    comp.splitFactor = 250 #  if comp.name in [ "WJets", "DY3JetsM50", "DY4JetsM50","W1Jets","W2Jets","W3Jets","W4Jets","TTJetsHad" ] else 100
    comp.puFileMC=dataDir+"/puProfile_Summer12_53X.root"
    comp.puFileData=dataDir+"/puProfile_Data12.root"
    comp.efficiency = eff2012

if __name__ == "__main__":
   import sys
   if "test" in sys.argv:
       from CMGTools.RootTools.samples.ComponentCreator import testSamples
       testSamples(samples)
