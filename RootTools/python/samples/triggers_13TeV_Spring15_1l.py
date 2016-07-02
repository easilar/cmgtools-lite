##################
## Triggers for HLT_MC_SPRING15 and Run II
## Based on HLT_MC_SPRING15 and /frozen/2015/25ns14e33/v2.1/HLT/V1 and /frozen/2015/50ns_5e33/v2.1/HLT/V5

### ----> for the 1L dPhi analysis

## single lepton
triggers_1mu = ["HLT_IsoMu27_v*"]
triggers_1mu20 = ["HLT_IsoMu20_v*"]
triggers_1el = ["HLT_Ele32_eta2p1_WP75_Gsf_v*",'HLT_Ele32_eta2p1_WPLoose_Gsf_v*','HLT_Ele32_eta2p1_WPTight_Gsf_v*']
triggers_1el23 = ["HLT_Ele23_WPLoose_Gsf_v*"]
triggers_1el22 = ["HLT_Ele22_eta2p1_WPLoose_Gsf_v*","HLT_Ele22_eta2p1_WPTight_Gsf_v*"]


### non-iso single lepton
trigger_1mu_noiso_r = ['HLT_Mu45_eta2p1_v*']
trigger_1mu_noiso_w = ['HLT_Mu50_v*']
trigger_1el_noiso = ['HLT_Ele105_CaloIdVT_GsfTrkIdT_v*']
#trigger_1el = ['HLT_Ele25_eta2p1_WPTight_Gsf_v*']

## muons
triggers_mu_ht600 = ["HLT_Mu15_IsoVVVL_PFHT600_v*"]
triggers_mu_ht400_met70 = ["HLT_Mu15_IsoVVVL_PFHT400_PFMET70_v*"]
triggers_mu_ht350_met70 = ["HLT_Mu15_IsoVVVL_PFHT350_PFMET70_v*"]
triggers_mu_ht350_met50 = ["HLT_Mu15_IsoVVVL_PFHT350_PFMET50_v*"]
triggers_mu_ht350 = ["HLT_Mu15_IsoVVVL_PFHT350_v*"]
triggers_mu_met120 = ["HLT_PFMET120_NoiseCleaned_Mu5_v*"]
triggers_mu_ht400_btag = ["HLT_Mu15_IsoVVVL_BTagCSV07_PFHT400_v*"]

## electrons
triggers_el_ht600 = ["HLT_Ele15_IsoVVVL_PFHT600_v*"]
triggers_el_ht400_met70 = ["HLT_Ele15_IsoVVVL_PFHT400_PFMET70_v*"]
triggers_el_ht350_met70 = ["HLT_Ele15_IsoVVVL_PFHT350_PFMET70_v*"]
triggers_el_ht350_met50 = ["HLT_Ele15_IsoVVVL_PFHT350_PFMET50_v*"]
triggers_el_ht350 = ["HLT_Ele15_IsoVVVL_PFHT350_v*"]
triggers_el_ht200 = ["HLT_Ele27_eta2p1_WP85_Gsf_HT200_v*"]
triggers_el_ht400_btag = ["HLT_Ele15_IsoVVVL_BTagtop8CSV07_PFHT400_v*"]

## hadronic
triggers_HT350 = ["HLT_PFHT350_v*"] # prescaled!
triggers_HT600 = ["HLT_PFHT600_v*"] # prescaled!
triggers_HT800 = ["HLT_PFHT800_v*"]
triggers_HT900 = ["HLT_PFHT900_v*"]
triggers_MET170 = ["HLT_PFMET170_NoiseCleaned_v*"]
triggers_HTMET = ["HLT_PFHT350_PFMET120_*"] # include all noise cleaning options!
triggers_HT350MET120 = ["HLT_PFHT350_PFMET120_*"] # include all noise cleaning options!
triggers_HT350MET100 = ["HLT_PFHT350_PFMET100_*"] # include all noise cleaning options!

#### Combined paths

triggers_muhad = triggers_mu_ht600 + triggers_mu_ht400_met70 + triggers_mu_met120 + triggers_mu_ht400_btag
triggers_elhad = triggers_el_ht600 + triggers_el_ht400_met70 + triggers_el_ht200  + triggers_el_ht400_btag
triggers_had = triggers_HT900 + triggers_MET170 + triggers_HTMET

#### DegenerateStop
triggers_MET170_pres = ["HLT_PFMET170_v*"] #(prescaled by 10)
triggers_MET250      = ["HLT_MET250_v*"]  
triggers_MET90nc           =["HLT_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v*"]
triggers_MET120nc          =["HLT_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v*"]
triggers_MET90MHT90        =["HLT_PFMET90_PFMHT90_IDTight_v*"]
triggers_MET120MHT120      =["HLT_PFMET120_PFMHT120_IDTight_v*"]
triggers_PhysRate          =["HLT_IsoMu17_eta2p1_v*", "HLT_IsoMu20_v*", "HLT_Mu27_v*", "HLT_IsoTkMu20_v*"]
triggers_Mu3erHT140MET125  =["HLT_Mu3er_PFHT140_PFMET125_v*"]
 
