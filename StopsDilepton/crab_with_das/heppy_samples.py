#-------- SAMPLES AND TRIGGERS -----------
#from CMGTools.TTHAnalysis.samples.samples_13TeV_PHYS14 import *
from CMGTools.StopsDilepton.samples import *
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import *
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *
#from CMGTools.RootTools.samples.TTbarDMJets_signals_RunIISpring15MiniAODv2 import *
#from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *
#from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *
#from CMGTools.RootTools.samples.triggers_13TeV_Spring15_1l import *
#from CMGTools.RootTools.samples.samples_13TeV_signals import *
##applying the correct json files to PrompReco and July17 samples

for sample in dataSamples_Run2016_v2:
    sample.json="$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_271036-275125_13TeV_PromptReco_Collisions16_JSON.txt"
