##########################################################
##       CONFIGURATION FOR SUSY SingleLep TREES         ##
## skim condition: >= 1 loose leptons, no pt cuts or id ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

#Load all analyzers
from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *

####### Leptons  #####
# lep collection
lepAna.packedCandidates = 'packedPFCandidates'

## ELECTRONS
lepAna.loose_electron_pt  = 5
eleID = "MVAID"

if eleID == "CBID":
  lepAna.loose_electron_id  = "POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto_full5x5"
  lepAna.loose_electron_lostHits = 999. # no cut
  lepAna.loose_electron_dxy    = 999.
  lepAna.loose_electron_dz     = 999.

  lepAna.inclusive_electron_id  = ""#"POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto_full5x5"
  lepAna.inclusive_electron_lostHits = 999. # no cut since embedded in ID
  lepAna.inclusive_electron_dxy    = 999. # no cut since embedded in ID
  lepAna.inclusive_electron_dz     = 999. # no cut since embedded in ID

elif eleID == "MVAID":
  inclusive_electron_id  = "" # same as in susyCore

  #lepAna.loose_electron_id = "POG_MVA_ID_Phys14_NonTrig_VLoose" # Phys14 era
  lepAna.loose_electron_id = "POG_MVA_ID_Spring15_NonTrig_VLoose" # Spring15 25ns era

elif eleID == "Incl": # as inclusive as possible
  lepAna.loose_electron_id  = ""
  lepAna.loose_electron_lostHits = 999. # no cut
  lepAna.loose_electron_dxy    = 999.
  lepAna.loose_electron_dz     = 999.

  lepAna.inclusive_electron_id  = ""
  lepAna.inclusive_electron_lostHits = 999.  # no cut
  lepAna.inclusive_electron_dxy    = 999. # no cut since embedded in ID
  lepAna.inclusive_electron_dz     = 999. # no cut since embedded in ID

## MUONS
lepAna.loose_muon_pt  = 5

# Isolation
isolation = "miniIso"

if isolation == "miniIso":
  # do miniIso
  lepAna.doMiniIsolation = True
  lepAna.miniIsolationPUCorr = 'rhoArea'
  lepAna.miniIsolationVetoLeptons = None
  lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4
  lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4
elif isolation == "relIso03":
  # normal relIso03
  lepAna.ele_isoCorr = "rhoArea"
  lepAna.mu_isoCorr = "rhoArea"

  lepAna.loose_electron_relIso = 0.5
  lepAna.loose_muon_relIso = 0.5


# --- LEPTON SKIMMING ---
ttHLepSkim.minLeptons = 0
ttHLepSkim.maxLeptons = 999
#LepSkim.idCut  = ""
#LepSkim.ptCuts = []

# --- JET-LEPTON CLEANING ---
jetAna.minLepPt = 10
jetAna.applyL2L3Residual = 'Data' 
jetAna.jetPt = 0
jetAna.jetEta = 5.2
jetAna.addJECShifts = True
jetAna.doQG = False
jetAna.smearJets = False #should be false in susycore, already

jetAna.recalibrateJets =  True #For data #FIXME
jetAna.calculateSeparateCorrections = True #should be true if recalibrate, otherwise L1 inconsistent

jetAna.calculateType1METCorrection = False
jetAna.dataGT   = "Fall15_25nsV2_DATA"
jetAna.mcGT   = "Fall15_25nsV2_MC"

metAna.recalibrate = False 

isoTrackAna.setOff=False
genAna.allGenTaus = True

from CMGTools.TTHAnalysis.analyzers.ttHLepEventAnalyzer import ttHLepEventAnalyzer
ttHEventAna = cfg.Analyzer(
    ttHLepEventAnalyzer, name="ttHLepEventAnalyzer",
    minJets25 = 0,
    )

## Insert the FatJet, SV, HeavyFlavour analyzers in the sequence
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
                        ttHFatJetAna)
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
                        ttHSVAna)

from PhysicsTools.Heppy.analyzers.gen.LHEAnalyzer import LHEAnalyzer 
LHEAna = LHEAnalyzer.defaultConfig


from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *
from CMGTools.RootTools.samples.triggers_13TeV_Spring15_1l import *
triggerFlagsAna.triggerBits = {
        ## hadronic
        'HT350' : triggers_HT350,
        'HT600' : triggers_HT600,
        'HT800' : triggers_HT800,
        'MET170' : triggers_MET170,
        'HT350MET120' : triggers_HT350MET120,
        'HT350MET100' : triggers_HT350MET100,
        'HTMET' : triggers_HT350MET100 + triggers_HT350MET120,
        ## muon
        'SingleMu' : triggers_1mu,
        'IsoMu27' : triggers_1mu,
        'IsoMu20' : triggers_1mu20,
        'Mu45eta2p1' : trigger_1mu_noiso_r,
        'Mu50' : trigger_1mu_noiso_w,
        'MuHT600' : triggers_mu_ht600,
        'MuHT400MET70' : triggers_mu_ht400_met70,
        'MuHT350MET70' : triggers_mu_ht350_met70,
        'MuHT350MET50' : triggers_mu_ht350_met50,
        'MuHT350' : triggers_mu_ht350,
        'MuHTMET' : triggers_mu_ht350_met70 + triggers_mu_ht400_met70,
        'MuMET120' : triggers_mu_met120,
        'MuHT400B': triggers_mu_ht400_btag,
        ## electrons
        'IsoEle32' : triggers_1el,
        'IsoEle23' : triggers_1el23,
        'IsoEle22' : triggers_1el22,
        'Ele105' : trigger_1el_noiso,
        'EleHT600' : triggers_el_ht600,
        'EleHT400MET70' : triggers_el_ht400_met70,
        'EleHT350MET70' : triggers_el_ht350_met70,
        'EleHT350MET50' : triggers_el_ht350_met50,
        'EleHT350' : triggers_el_ht350,
        'EleHTMET' : triggers_el_ht350_met70 + triggers_el_ht400_met70,
        'EleHT200' :triggers_el_ht200,
        'EleHT400B': triggers_el_ht400_btag,

#mumu
        'mumuIso' : triggers_mumu_iso,
        'mumuNoniso_50ns' : triggers_mumu_noniso_50ns,
        'mumuNoiso' : triggers_mumu_noniso,
        'mumuSS' : triggers_mumu_ss,
        'mumuHT' : triggers_mumu_ht,
# ee
        'ee_DZ': triggers_ee, 
#mue
        'mue':triggers_mue,
#dilepton+HT
        'ee_ht':triggers_ee_ht,
        'mue_ht':triggers_mue_ht,
#multi-lepton
        '3e':triggers_3e,
        '3mu':triggers_3mu,
        '3mu_alt':triggers_3mu_alt,
        '2mu1e':triggers_2mu1e,
        '2e1mu':triggers_2e1mu,
#fake rate
        'FR_1mu_iso':triggers_FR_1mu_iso,
        'FR_1mu_noiso':triggers_FR_1mu_noiso,
        'FR_1e_noiso':triggers_FR_1e_noiso,
        'FR_1e_iso':triggers_FR_1e_iso,
        'FR_1e_b2g':triggers_FR_1e_b2g,
#MET
        'Jet80MET90'       :triggers_Jet80MET90      ,
        'Jet80MET120'      :triggers_Jet80MET120     ,
        'MET120Mu5'        :triggers_MET120Mu5       ,

        'MET170_pres'      :triggers_MET170_pres     , 
        'MET250'           :triggers_MET250          ,
        'MET90nc'          :triggers_MET90nc         ,
        'MET120nc'         :triggers_MET120nc        ,
        'MET90'            :triggers_MET90MHT90      ,
        'MET120'           :triggers_MET120MHT120    ,
        'PhysRates'        :triggers_PhysRate        ,
        'Mu3erHT140MET125' :triggers_Mu3erHT140MET125,
        'DiPFJetAve100_HFJEC': ["HLT_DiPFJetAve100_HFJEC_v*"],
        'DiPFJetAve140': ["HLT_DiPFJetAve140_v*"],
        'DiPFJetAve160_HFJEC': ["HLT_DiPFJetAve160_HFJEC_v*"],
        'DiPFJetAve200': ["HLT_DiPFJetAve200_v*"],
        'DiPFJetAve220_HFJEC': ["HLT_DiPFJetAve220_HFJEC_v*"],
        'DiPFJetAve260': ["HLT_DiPFJetAve260_v*"],
        'DiPFJetAve300_HFJEC': ["HLT_DiPFJetAve300_HFJEC_v*"],
        'DiPFJetAve320': ["HLT_DiPFJetAve320_v*"],
        'DiPFJetAve40': ["HLT_DiPFJetAve40_v*"],
        'DiPFJetAve400': ["HLT_DiPFJetAve400_v*"],
        'DiPFJetAve500': ["HLT_DiPFJetAve500_v*"],
        'DiPFJetAve60_HFJEC': ["HLT_DiPFJetAve60_HFJEC_v*"],
        'DiPFJetAve60': ["HLT_DiPFJetAve60_v*"],
        'DiPFJetAve80_HFJEC': ["HLT_DiPFJetAve80_HFJEC_v*"],
        'DiPFJetAve80': ["HLT_DiPFJetAve80_v*"],
        }

# Tree Producer
from CMGTools.StopsDilepton.treeProducerStopsDilepton import *
## Tree Producer
treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerSusySingleLepton',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
     PDFWeights = PDFWeights,
     globalVariables = susySingleLepton_globalVariables,
     globalObjects = susySingleLepton_globalObjects,
     collections = susySingleLepton_collections,
)

#!# #-------- SAMPLES AND SEQUENCE -----------

selectedComponents = [
        ]

sequence = cfg.Sequence(
  susyCoreSequence+
      [ LHEAna,
        ttHEventAna,
        treeProducer,
        ])

#if True or getHeppyOption("loadSamples"):
if getHeppyOption("loadSamples"):
    from CMGTools.RootTools.samples.samples_13TeV_RunIIFall15MiniAODv2 import *
    from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *
    for sample in dataSamples_Run2015D_16Dec:
        sample.json="$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_Silver_v2.txt"
    from CMGTools.StopsDilepton.samples import *

    selectedComponents = [TTJets, DoubleMuon_Run2015D_16Dec]
    for comp in selectedComponents:
            comp.files = comp.files[:1]
            comp.splitFactor = 1

from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
event_class = Events
if getHeppyOption("fetch"):
  event_class = EOSEventsWithDownload

print "Components"
print selectedComponents
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [],
#                     preprocessor=preprocessor, # comment if pre-processor non needed
                     events_class = event_class)

