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

n_events_per_job = 1e6

for sample in selectedComponents:
    sample.splitFactor = splitFactor(sample, n_events_per_job)
       
events_to_pick  = [84619,
84659,
84710,
84762,
84794,
84838,
84879,
84915,
84944,
84966,
85006,
85054,
85104,
85132,
85176,
85206,
85226,
85224,
85228,
85292,
85367,
85369,
85399,
85424,
85411,
85419,
85446,
85464,
85469,
85510,
85511,
85535,
85541,
85560,
85566,
85625,
47464,
47488,
47493,
47544,
47576,
47610,
47626,
47636,
47642,
47705,
47724,
47732,
47748,
47773] 

events_to_pick  = []


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
        tau2_associatedVert_z = v(lambda x: x.associatedVertex.z()),
        )


muon_vars = Block(
        'muo', lambda x: x.sel_muons_third_lepton_veto[0],
    muo_weight_tracking = v(lambda x: getattr(x, 'weight_tracking', 1. )),
    muo_pt = v(lambda x: x.pt()), 
    muo_eta = v(lambda x: x.eta()),
    muo_phi = v(lambda x: x.phi()),  
    muo_iso = v(lambda x: x.iso_htt()), 
    muo_d0 = v(lambda x: x.dxy()),
    muo_dz = v(lambda x: x.dz()),  
    muo_weight_trig_m = v(lambda x: getattr(x, 'weight_trigger_m', 1.)),
    muo_weight_trig_mt = v(lambda x: getattr(x, 'weight_trigger_mt', 1.)),
)

event_vars = Block(
    'event', lambda x: x,
    run = v(lambda x: x.run, int),
    lumi = v(lambda x: x.lumi, int),
    event = v(lambda x: x.eventId, int, 'l'),
    rho = v(lambda x: x.rho),
    n_pv = v(lambda x: len(x.vertices), int)
    )



tautau = EventContent(
    [
#    metvars,
    event_vars,
#    tau1_vars,
#    tau2_vars,
#    electron_vars,
    muon_vars
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
#        taus,
#        sel_taus,
#	two_tau,
#	at_least_one_tau
        muons,
	sel_muons_third_lepton_veto,
	at_least_one_muo,
#        electrons,
#        genmatcher,
#        tauenergyscale,
])

sequence = sequence_beforedil
#sequence.extend( sequence_dilepton )
#sequence.extend( sequence_afterdil )
#sequence.append(tauidweighter_general)
#sequence.append(tauidweighter)
#sequence.append(triggerweighter)
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
