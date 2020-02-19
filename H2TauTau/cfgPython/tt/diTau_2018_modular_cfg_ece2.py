import os
import re

import ROOT

import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

from CMGTools.RootTools.yellowreport.YRParser import yrparser13TeV
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator


creator = ComponentCreator()
#ComponentCreator.useLyonAAA = True
ComponentCreator.useAAA = True

#HiggsVBF125 = creator.makeMCComponent('HiggsVBF125', '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 'CMS', '.*root', 1.0)
HiggsVBF125 = creator.makeMCComponent('HiggsVBF125', '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 'CMS', '.*root', 1.0)

mc_higgs = [
    HiggsVBF125,
]

samples_lists = {'sm_higgs': mc_higgs}
print("sample lists:" , samples_lists)


import logging
logging.shutdown()
# reload(logging)
logging.basicConfig(level=logging.WARNING)

from PhysicsTools.HeppyCore.framework.event import Event
Event.print_patterns = ['*taus*', '*muons*', '*electrons*', 'veto_*', 
                        '*dileptons_*', '*jets*']

###############
# Options
###############

# Get all heppy options; set via "-o production" or "-o production=True"

samples_name = 'sm_higgs'


###############
# Components
###############

from CMGTools.RootTools.utils.splitFactor import splitFactor

selectedComponents = samples_lists[samples_name]

n_events_per_job = 3e5
#n_events_per_job = 3e6

for sample in selectedComponents:
    sample.splitFactor = splitFactor(sample, n_events_per_job)
       

events_to_pick  = []


from CMGTools.H2TauTau.heppy.sequence.common import debugger
debugger.condition = None  #lambda event : True # lambda event : len(event.sel_taus)>2
#debugger.condition = lambda event : True # lambda event : len(event.sel_taus)>2

###############
# Analyzers 
###############
from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer import JSONAnalyzer
from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount import SkimAnalyzerCount

json = cfg.Analyzer(
    JSONAnalyzer,
    name='JSONAnalyzer',
)

skim = cfg.Analyzer(
    SkimAnalyzerCount,
    name='SkimAnalyzerCount'
)

from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
vertex = cfg.Analyzer(
    VertexAnalyzer,
    name='VertexAnalyzer',
    fixedWeight=1,
    keepFailingEvents=True,
    verbose=False
)


from CMGTools.H2TauTau.heppy.analyzers.TauAnalyzer import TauAnalyzer
taus = cfg.Analyzer(
    TauAnalyzer,
    name = 'TauAnalyzer',
    output = 'taus',
    taus = 'slimmedTaus'
)


from CMGTools.H2TauTau.heppy.analyzers.MuonAnalyzer import MuonAnalyzer
muons = cfg.Analyzer(
    MuonAnalyzer,
    name = 'MuonAnalyzer',
    output = 'muons',
    muons = 'slimmedMuons',
)

from PhysicsTools.Heppy.physicsobjects.Muon import Muon
Muon.iso_htt = lambda x: x.relIso(0.4, 'dbeta', dbeta_factor=0.5,
                                  all_charged=False)

from CMGTools.H2TauTau.heppy.analyzers.ElectronAnalyzer import ElectronAnalyzer
electrons = cfg.Analyzer(
    ElectronAnalyzer,
    output = 'electrons',
    electrons = 'slimmedElectrons',
)

# setting up an alias for our isolation, now use iso_htt everywhere
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.Heppy.physicsutils.EffectiveAreas import areas

Electron.EffectiveArea03 = areas['Fall17']['electron']

Electron.iso_htt = lambda x: x.relIso(0.3, "EA",
                                      all_charged=False)

from CMGTools.H2TauTau.heppy.analyzers.EventFilter import EventFilter

#This is to require an event with at least 2 tau in it.
at_least_one_tau = cfg.Analyzer(
    EventFilter,
    'tau',
    src = 'taus',
    filter_func = lambda x : len(x)>0
)


at_least_one_muo = cfg.Analyzer(
    EventFilter,
    'muo',
    src = 'sel_muons_third_lepton_veto',
    filter_func = lambda x : len(x)>0
)

at_least_one_ele = cfg.Analyzer(
    EventFilter,
    'ele',
    src = 'sel_electrons_third_lepton_veto',
    filter_func = lambda x : len(x)>0
)



from CMGTools.H2TauTau.heppy.analyzers.Selector import Selector
def select_tau(tau):
    return tau.pt()    > 40  and \
        abs(tau.eta()) < 2.1 and \
        abs(tau.leadChargedHadrCand().dz()) < 0.2 and \
        tau.tauID('decayModeFinding') > 0.5 and \
        abs(tau.charge()) == 1. and \
        tau.tauID('byVVLooseIsolationMVArun2017v2DBoldDMwLT2017')

sel_taus = cfg.Analyzer(
    Selector,
    'sel_taus',
    output = 'sel_taus',
    src = 'taus',
    filter_func = select_tau  
)

from CMGTools.H2TauTau.heppy.analyzers.EventFilter import EventFilter
two_tau = cfg.Analyzer(
    EventFilter, 
    'two_tau',
    src = 'sel_taus',
    filter_func = lambda x : len(x)>1
)

def select_leptons(event):
    leptons = []
    leptons.extend(event.taus)
    leptons.extend(event.muons)
    leptons.extend(event.electrons)
    return leptons

from CMGTools.H2TauTau.heppy.analyzers.GenMatcherAnalyzer import GenMatcherAnalyzer
genmatcher = cfg.Analyzer(
    GenMatcherAnalyzer, 
    'genmatcher',
    jetCol='slimmedJets',
    genPtCut=8.,
    genmatching = True,
    filter_func = select_leptons
)

from CMGTools.H2TauTau.heppy.analyzers.TauP4Scaler import TauP4Scaler
tauenergyscale = cfg.Analyzer(
    TauP4Scaler,
    'tauenergyscale',
    src = 'taus',
    systematics = False
)


def select_muon_third_lepton_veto(muon):
    return muon.pt() > 10             and \
        abs(muon.eta()) < 2.4         and \
        muon.isMediumMuon()  and \
        abs(muon.dxy()) < 0.045       and \
        abs(muon.dz())  < 0.2         and \
        muon.iso_htt() < 0.3
sel_muons_third_lepton_veto = cfg.Analyzer(
    Selector,
    '3lepv_muons',
    output = 'sel_muons_third_lepton_veto',
    src = 'muons',
    filter_func = select_muon_third_lepton_veto
)


def select_electron_third_lepton_veto(electron):
    return electron.pt() > 10             and \
        abs(electron.eta()) < 2.5         and \
        electron.id_passes("mvaEleID-Fall17-noIso-V2", "wp90") and \
        abs(electron.dxy()) < 0.045       and \
        abs(electron.dz())  < 0.2         and \
        electron.passConversionVeto()     and \
        electron.gsfTrack().hitPattern().numberOfLostHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1 and \
        electron.iso_htt() < 0.3
sel_electrons_third_lepton_veto = cfg.Analyzer(
    Selector,
    '3lepv_electrons',
    output = 'sel_electrons_third_lepton_veto',
    src = 'electrons',
    filter_func = select_electron_third_lepton_veto
)


# ditau pair ================================================================

from CMGTools.H2TauTau.heppy.analyzers.DiLeptonAnalyzer import DiLeptonAnalyzer

dilepton = cfg.Analyzer(
    DiLeptonAnalyzer,
    output = 'dileptons',
    l1 = 'sel_taus',
    l2 = 'sel_taus',
    dr_min = 0.5
)

def sorting_metric(dilepton):
    leg1_iso = dilepton.leg1().tauID('byIsolationMVArun2017v2DBoldDMwLTraw2017')
    leg2_iso = dilepton.leg2().tauID('byIsolationMVArun2017v2DBoldDMwLTraw2017')
    if leg1_iso > leg2_iso:
        most_isolated_tau_isolation = leg1_iso
        most_isolated_tau_pt = dilepton.leg1().pt()
        least_isolated_tau_isolation = leg2_iso
        least_isolated_tau_pt = dilepton.leg2().pt()
    else:
        most_isolated_tau_isolation = leg2_iso
        most_isolated_tau_pt = dilepton.leg2().pt()
        least_isolated_tau_isolation = leg1_iso
        least_isolated_tau_pt = dilepton.leg1().pt()
    return (-most_isolated_tau_isolation,
             -most_isolated_tau_pt,
             -least_isolated_tau_isolation,
             -least_isolated_tau_pt)

from CMGTools.H2TauTau.heppy.analyzers.Sorter import Sorter
dilepton_sorted = cfg.Analyzer(
    Sorter,
    output = 'dileptons_sorted',
    src = 'dileptons',
    metric = sorting_metric,
    reverse = False
    )



sequence_dilepton = cfg.Sequence([
        sel_taus,
        two_tau,
        dilepton,
        dilepton_sorted,
        ])
# Jet sequence ==========================================================
gt_mc = 'Fall17_17Nov2017_V32_MC'

def select_good_jets_FixEE2017(jet):
        return jet.correctedJet("Uncorrected").pt() >50. or \
        abs(jet.eta()) < 2.65 or \
        abs(jet.eta()) > 3.139

from CMGTools.H2TauTau.heppy.analyzers.JetAnalyzer import JetAnalyzer
jets = cfg.Analyzer(
    JetAnalyzer,
    output = 'jets',
    jets = 'slimmedJets',
    do_jec = True,
    gt_mc = gt_mc,
    selection = select_good_jets_FixEE2017
)

from CMGTools.H2TauTau.heppy.analyzers.Sorter import Sorter
jet_sorter = cfg.Analyzer(
    Sorter,
    output = 'jets_sorted',
    src = 'jets',
    metric = lambda jet: (jet.pt()),
    reverse = True
    )

jets_20_unclean = cfg.Analyzer(
    Selector,
    'jets_20_unclean',
    output = 'jets_20_unclean',
    src = 'jets_sorted',
    filter_func = lambda x : x.pt()>20 and abs(x.eta())<4.7 and x.jetID("POG_PFID_Tight" )
)


from CMGTools.H2TauTau.heppy.analyzers.JetCleaner import JetCleaner
jet_20 = cfg.Analyzer(
    JetCleaner,
    output = 'jets_20',
    dileptons = 'dileptons_sorted',
    jets = 'jets_20_unclean',
    drmin = 0.5
)

jets_30 = cfg.Analyzer(
    Selector,
    'jets_30',
    output = 'jets_30',
    src = 'jets_20',
    filter_func = lambda x : x.pt()>30 
)

# Trigger  ===============================================================
from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerAnalyzer

trigger = cfg.Analyzer(
    TriggerAnalyzer,
    name='TriggerAnalyzer',
    addTriggerObjects=True,
    requireTrigger=False,
    usePrescaled=False
)


from CMGTools.H2TauTau.heppy.analyzers.TrigMatcher import TrigMatcher    
trigger_match = cfg.Analyzer(
    TrigMatcher,
    src='dileptons_sorted',
    require_all_matched = True
)



# weights ================================================================

# id weights
from CMGTools.H2TauTau.heppy.analyzers.TauIDWeighter import TauIDWeighter
tauidweighter_general = cfg.Analyzer(
    TauIDWeighter,
    'TauIDWeighter_general',
    taus = lambda event: [event.dileptons_sorted[0].leg1(),event.dileptons_sorted[0].leg2()]
)

tauidweighter = cfg.Analyzer(
    TauIDWeighter,
    'TauIDWeighter',
    taus = lambda event: [event.dileptons_sorted[0].leg1(),event.dileptons_sorted[0].leg2()],
    WPs = {'JetToTau':'Tight', # dummy, no weights for jet fakes
           'TauID':'Tight',
           'MuToTaufake':'Loose',
           'EToTaufake':'VLoose'}
)


# trigger weights
ws_tau_vars_dict = {'t_pt':lambda tau:tau.pt(),
                    't_eta':lambda tau:tau.eta(),
                    't_phi':lambda tau:tau.phi()}
ws_tau_func_dict = {'tt':'t_trg_tight_tt_ratio'}
from CMGTools.H2TauTau.heppy.analyzers.TriggerWeighter import TriggerWeighter
triggerweighter = cfg.Analyzer(
    TriggerWeighter,
    'TriggerWeighter',
    workspace_path = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_2017_v2.root',
    legs = lambda event: [event.dileptons_sorted[0].leg1(),event.dileptons_sorted[0].leg2()],
    leg1_vars_dict = ws_tau_vars_dict,
    leg2_vars_dict = ws_tau_vars_dict,
    leg1_func_dict = ws_tau_func_dict,
    leg2_func_dict = ws_tau_func_dict
)


# from CMGTools.H2TauTau.heppy.analyzers.FakeFactorAnalyzer import FakeFactorAnalyzer
# fakefactor = cfg.Analyzer(
#     FakeFactorAnalyzer,
#     'FakeFactorAnalyzer',
#     channel = 'tt',
#     filepath = '$CMSSW_BASE/src/HTTutilities/Jet2TauFakes/data/MSSM2016/20170628_medium/{}/{}/fakeFactors_20170628_medium.root',
#     met = 'pfmet'
# )




from CMGTools.H2TauTau.heppy.ntuple.tools import Block , EventContent , Variable , to_leg
v = Variable
default = v.default

tau1_vars = Block(
        'tau1', lambda x: x.sel_taus[0],
    	tau1_decayMode = v(lambda x: x.decayMode()),
    	tau1_idDecayMode = v(lambda x: x.tauID('decayModeFinding')),
	tau1_idDecayModeNewDMs = v(lambda x: x.tauID('decayModeFindingNewDMs')),
    	tau1_d0 = v(lambda x: x.leadChargedHadrCand().dxy()),
        tau1_dz =  v(lambda x: x.leadChargedHadrCand().dz()),
	tau1_idMVAoldDM2017v2 = v(lambda x: x.tauID('byVVLooseIsolationMVArun2017v2DBoldDMwLT2017')),
        tau1_pt = v(lambda x: x.pt()),
        tau1_eta = v(lambda x: x.eta()),
        tau1_phi = v(lambda x: x.phi()),
        tau1_m = v(lambda x: x.mass()),
        tau1_q = v(lambda x: x.charge()),
        tau1_gen_match = v(lambda x: x.gen_match),
        tau1_energyScale = v(lambda x: x.energyScale),
        tau1_associatedVert_z = v(lambda x: x.associatedVertex.z()),
        )

tau2_vars = Block(
        'tau2', lambda x: x.sel_taus[1],
    	tau2_decayMode = v(lambda x: x.decayMode()),
    	tau2_idDecayMode = v(lambda x: x.tauID('decayModeFinding')),
	tau2_idDecayModeNewDMs = v(lambda x: x.tauID('decayModeFindingNewDMs')),
    	tau2_d0 = v(lambda x: x.leadChargedHadrCand().dxy()),
        tau2_dz =  v(lambda x: x.leadChargedHadrCand().dz()),
	tau2_idMVAoldDM2017v2 = v(lambda x: x.tauID('byVVLooseIsolationMVArun2017v2DBoldDMwLT2017')),
        tau2_pt = v(lambda x: x.pt()),
        tau2_eta = v(lambda x: x.eta()),
        tau2_phi = v(lambda x: x.phi()),
        tau2_m = v(lambda x: x.mass()),
        tau2_q = v(lambda x: x.charge()),
        tau2_gen_match = v(lambda x: x.gen_match),
        tau2_energyScale = v(lambda x: x.energyScale),
        tau2_associatedVert_z = v(lambda x: x.associatedVertex.z()),
        )


muon_vars = Block(
        'muo', lambda x: x.sel_muons_third_lepton_veto[0],
    muo_weight_tracking = v(lambda x: getattr(x, 'weight_tracking', 1. )),
    muo_pt = v(lambda x: x.pt()), 
    muo_eta = v(lambda x: x.eta()),
    muo_phi = v(lambda x: x.phi()),  
    muo_iso = v(lambda x: x.iso_htt()), 
    muo_dxy = v(lambda x: x.dxy()),
    muo_dz = v(lambda x: x.dz()),  
    muo_weight_trig_m = v(lambda x: getattr(x, 'weight_trigger_m', 1.)),
    muo_weight_trig_mt = v(lambda x: getattr(x, 'weight_trigger_mt', 1.)),
)

electron_vars = Block(
        'ele', lambda x: x.sel_electrons_third_lepton_veto[0],
    ele_id_e_mva_nt_loose = v(lambda x: x.physObj.userFloat("ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values")),
    ele_weight_tracking = v(lambda x: getattr(x, 'weight_trk', 1. )),
    ele_pt = v(lambda x: x.pt()),
    ele_eta = v(lambda x: x.eta()),
    ele_phi = v(lambda x: x.phi()),
    ele_iso = v(lambda x: x.iso_htt()),
    ele_d0 = v(lambda x: x.dxy()),
    ele_dz = v(lambda x: x.dz()),
    ele_weight_trig_e = v(lambda x: getattr(x, 'weight_trigger_e', 1.)),
    ele_weight_trig_et = v(lambda x: getattr(x, 'weight_trigger_et', 1.)),
)

event_vars = Block(
    'event', lambda x: x,
    run = v(lambda x: x.run, int),
    lumi = v(lambda x: x.lumi, int),
    event = v(lambda x: x.eventId, int, 'l'),
    rho = v(lambda x: x.rho),
    n_pv = v(lambda x: len(x.vertices), int)
    )

jets20 = Block(
    'jets20', lambda x: x.jets_20,
    n_jets_pt20 = v(lambda x: len(x), int),
    j1_pt = v(lambda x: x[0].pt() if len(x)>0 else default),
    j1_eta = v(lambda x: x[0].eta() if len(x)>0 else default),
    j1_phi = v(lambda x: x[0].phi() if len(x)>0 else default),
    # j1_bcsv = v(lambda x: x.bcsv()),
    j1_pumva = v(lambda x: x[0].puMva('pileupJetId:fullDiscriminant') if len(x)>0 else default),
#    j1_puid = v(lambda x: x[0].pileUpJetId_htt() if len(x)>0 else default),
    j1_flavour_parton = v(lambda x: x[0].partonFlavour() if len(x)>0 else default),
    j1_flavour_hadron = v(lambda x: x[0].hadronFlavour() if len(x)>0 else default),
    j1_rawf = v(lambda x: x[0].rawFactor() if len(x)>0 else default),
    j2_pt = v(lambda x: x[1].pt() if len(x)>1 else default),
    j2_eta = v(lambda x: x[1].eta() if len(x)>1 else default),
    j2_phi = v(lambda x: x[1].phi() if len(x)>1 else default),
    j2_pumva = v(lambda x: x[1].puMva('pileupJetId:fullDiscriminant') if len(x)>1 else default ),
#    j2_puid = v(lambda x: x[1].pileUpJetId_htt() if len(x)>1 else default ),
    j2_flavour_parton = v(lambda x: x[1].partonFlavour() if len(x)>1 else default),
    j2_flavour_hadron = v(lambda x: x[1].hadronFlavour() if len(x)>1 else default),
    j2_rawf = v(lambda x: x[1].rawFactor() if len(x)>1 else default),
    dijet_m = v(lambda x: (x[0].p4()+x[1].p4()).M() if len(x)>1 else default),
)

triggers = Block(
    'triggers', lambda x: [getattr(x.dileptons_sorted[0], 'matchedPaths', []),x.dileptons_sorted[0]],
    trg_singletau1 = v(lambda x : any('MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v' in name for name in x[0]) and x[1].leg1().pt()>45. and abs(x[1].leg1().eta())<2.1),
    trg_singletau2 = v(lambda x : any('MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v' in name for name in x[0]) and x[1].leg2().pt()>45. and abs(x[1].leg2().eta())<2.1),
    trg_singletau  = v(lambda x : any('MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v' in name for name in x[0]) and any([tau.pt()>45. and abs(tau.eta()<2.1) for tau in [x[1].leg1(), x[1].leg2()]])),
    trg_singlemuon_24 = v(lambda x : any('IsoMu24_v' in name for name in x[0]) and x[1].leg1().pt()>25. and abs(x[1].leg1().eta())<2.1),
    trg_singlemuon_27 = v(lambda x : any('IsoMu27_v' in name for name in x[0]) and x[1].leg1().pt()>28. and abs(x[1].leg1().eta())<2.1),
    trg_singleelectron_27 = v(lambda x : any('Ele27_WPTight_Gsf_v' in name for name in x[0]) and x[1].leg1().pt()>28. and abs(x[1].leg1().eta())<2.1),
    trg_singleelectron_32 = v(lambda x : any('Ele32_WPTight_Gsf_v' in name for name in x[0]) and x[1].leg1().pt()>33. and abs(x[1].leg1().eta())<2.1),
    trg_singleelectron_35 = v(lambda x : any('Ele35_WPTight_Gsf_v' in name for name in x[0]) and x[1].leg1().pt()>36. and abs(x[1].leg1().eta())<2.1),
    trg_doubletau_35_mediso = v(lambda x : any('DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v' in name for name in x[0]) and all([tau.pt()>40. and abs(tau.eta()<2.1) for tau in [x[1].leg1(), x[1].leg2()]])),
    trg_doubletau_35_tightiso_tightid = v(lambda x : any('DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v' in name for name in x[0]) and all([tau.pt()>40. and abs(tau.eta()<2.1) for tau in [x[1].leg1(), x[1].leg2()]])),
    trg_doubletau_40_mediso_tightid = v(lambda x : any('DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v' in name for name in x[0]) and all([tau.pt()>45. and abs(tau.eta()<2.1) for tau in [x[1].leg1(), x[1].leg2()]])),
    trg_doubletau_40_tightiso = v(lambda x : any('DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v' in name for name in x[0]) and all([tau.pt()>45. and abs(tau.eta()<2.1) for tau in [x[1].leg1(), x[1].leg2()]])),
    trg_crossmuon_mu24tau20 = v(lambda x : any('IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1_v' in name for name in x[0]) and x[1].leg1().pt()>25. and abs(x[1].leg1().eta())<2.1 and x[1].leg2().pt()>21. and abs(x[1].leg2().eta())<2.1),
    trg_crossmuon_mu20tau27 = v(lambda x : any('IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v' in name for name in x[0]) and x[1].leg1().pt()>21. and abs(x[1].leg1().eta())<2.1 and x[1].leg2().pt()>32. and abs(x[1].leg2().eta())<2.1),
    trg_crossele_ele24tau30 = v(lambda x : any('Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v' in name for name in x[0]) and x[1].leg1().pt()>25. and abs(x[1].leg1().eta())<2.1 and x[1].leg2().pt()>35. and abs(x[1].leg2().eta())<2.1),
    trg_muonelectron_mu8ele23 = v(lambda x : any('Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v' in name for name in x[0]) and x[1].leg1().pt()>24. and abs(x[1].leg1().eta())<2.5 and x[1].leg2().pt()>9. and abs(x[1].leg2().eta())<2.4),
    trg_muonelectron_mu12ele23 = v(lambda x : any('Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v' in name for name in x[0]) and x[1].leg1().pt()>24.  and abs(x[1].leg1().eta())<2.5 and x[1].leg2().pt()>13.and abs(x[1].leg2().eta())<2.4),
    trg_muonelectron_mu23ele12 = v(lambda x : any('Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v' in name for name in x[0]) and x[1].leg1().pt()>13.  and abs(x[1].leg1().eta())<2.5 and x[1].leg2().pt()>24.and abs(x[1].leg2().eta())<2.4)
)

triggers_matched = Block(
    'triggers_matched', lambda x: [getattr(x.dileptons_sorted[0], 'matchedPaths', []),x.dileptons_sorted[0]],
    trg_singletau_matched  = v(lambda x : any('MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v' in name for name in x[0])),
    trg_singlemuon_24_matched = v(lambda x : any('IsoMu24_v' in name for name in x[0])),
    trg_singlemuon_27_matched = v(lambda x : any('IsoMu27_v' in name for name in x[0])),
    trg_singleelectron_27_matched = v(lambda x : any('Ele27_WPTight_Gsf_v' in name for name in x[0])),
    trg_singleelectron_32_matched = v(lambda x : any('Ele32_WPTight_Gsf_v' in name for name in x[0])),
    trg_singleelectron_35_matched = v(lambda x : any('Ele35_WPTight_Gsf_v' in name for name in x[0])),
    trg_doubletau_35_mediso_matched = v(lambda x : any('DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v' in name for name in x[0])),
    trg_doubletau_35_tightiso_tightid_matched = v(lambda x : any('DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v' in name for name in x[0])),
    trg_doubletau_40_mediso_tightid_matched = v(lambda x : any('DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v' in name for name in x[0])),
    trg_doubletau_40_tightiso_matched = v(lambda x : any('DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v' in name for name in x[0])),
    trg_crossmuon_mu24tau20_matched = v(lambda x : any('IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1_v' in name for name in x[0])),
    trg_crossmuon_mu20tau27_matched = v(lambda x : any('IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v' in name for name in x[0])),
    trg_crossele_ele24tau30_matched = v(lambda x : any('Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v' in name for name in x[0])),
    trg_muonelectron_mu8ele23_matched = v(lambda x : any('Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v' in name for name in x[0])),
    trg_muonelectron_mu12ele23_matched = v(lambda x : any('Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v' in name for name in x[0])),
    trg_muonelectron_mu23ele12_matched = v(lambda x : any('Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v' in name for name in x[0]))
)


tautau = EventContent(
    [
#    metvars,
    event_vars,
#    tau1_vars,
#    tau2_vars,
    jets20
#    triggers,
#    triggers_matched
#    electron_vars,
#    muon_vars
#    dilepton_vars
     ]
)




# ntuple ================================================================

skim_func = lambda x: True

from CMGTools.H2TauTau.heppy.analyzers.NtupleProducer import NtupleProducer
#from CMGTools.H2TauTau.heppy.ntuple.ntuple_variables import tautau as event_content_tautau
ntuple = cfg.Analyzer(
    NtupleProducer,
    name = 'NtupleProducer',
    treename = 'events',
    event_content = tautau,
    skim_func = skim_func
)

sequence_beforedil = cfg.Sequence([
#        mcweighter,
        json,
        skim,
        vertex,
        taus,
#	at_least_one_tau
#        muons,
#	sel_muons_third_lepton_veto,
#	at_least_one_muo,
#        electrons,
#	sel_electrons_third_lepton_veto,
#	at_least_one_ele
#        genmatcher,
#        tauenergyscale,
#        sel_taus,
#	two_tau,
])

sequence_jets = cfg.Sequence([
        jets,
       jet_sorter,
       jets_20_unclean,
       jet_20,
#       jets_30
#       btagger,
#       bjets_20
])

sequence_afterdil = cfg.Sequence([
#       trigger, 
#       trigger_match,
#       met_filters,
#       lheweight,
#       httgenana,
#       pileup, 
#       njets_ana
]) 

sequence = sequence_beforedil
sequence.extend( sequence_dilepton )
#sequence.extend( sequence_afterdil )
sequence.extend(sequence_jets)
#sequence.append(tauidweighter_general)
#sequence.append(tauidweighter)
#sequence.append(triggerweighter)
sequence.append(debugger)
sequence.append(ntuple)


if events_to_pick:
    from CMGTools.H2TauTau.htt_ntuple_base_cff import eventSelector
    eventSelector.toSelect = events_to_pick
    sequence.insert(0, eventSelector)

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                    )

printComps(config.components, True)

print config
