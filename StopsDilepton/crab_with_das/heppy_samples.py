#-------- SAMPLES AND TRIGGERS -----------
#from CMGTools.TTHAnalysis.samples.samples_13TeV_PHYS14 import *
from CMGTools.StopsDilepton.samples import *
from CMGTools.RootTools.samples.samples_13TeV_RunIIFall15MiniAODv2 import *
#from CMGTools.RootTools.samples.TTbarDMJets_signals_RunIISpring15MiniAODv2 import *
#from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *
#from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *
#from CMGTools.RootTools.samples.triggers_13TeV_Spring15_1l import *
#from CMGTools.RootTools.samples.samples_13TeV_signals import *
##applying the correct json files to PrompReco and July17 samples

for sample in samples_data_private:
  sample.json = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_Silver_v2.txt"
