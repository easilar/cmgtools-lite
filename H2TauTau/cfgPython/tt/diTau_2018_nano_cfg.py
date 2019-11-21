import os
import re

import ROOT

import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

from CMGTools.H2TauTau.heppy.analyzers.Selector import Selector
from CMGTools.H2TauTau.heppy.analyzers.Cleaner import Cleaner

import logging
logging.shutdown()
# reload(logging)
logging.basicConfig(level=logging.INFO)

from PhysicsTools.HeppyCore.framework.event import Event
Event.print_patterns = ['*taus*', '*muons*', '*electrons*', 'veto_*', 
                        '*dileptons_*', '*jets*']

events_to_pick  = [84575,\
84574,\
84580,\
84579,\
84593,\
84603,\
84605,\
84607,\
84606,\
84610,\
84616,\
84617,\
84636,\
84633,\
84634,\
84653,\
84655,\
84628,\
1403781,\
1403789,\
1403795,\
1403798,\
1403805,\
1403811,\
1403818,\
1403823,\
1403828,\
1403837,\
1403838,\
1403841,\
1403852,\
1403853,\
1403862,\
1403863,\
1403873,\
1403860,\
1403878,\
1403872,\
1403881,\
1403880,\
1403876,\
1403870]



events_to_pick = []


###############
# Components
###############

from CMGTools.RootTools.yellowreport.YRParser import yrparser13TeV
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
creator = ComponentCreator()
#ComponentCreator.useLyonAAA = True
ComponentCreator.useAAA = True

#HiggsVBF125_nano = creator.makeMCComponent('HiggsVBF125_nano', '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', 'CMS', '.*root', 1.0)

HiggsVBF125_nano = creator.makeMCComponent('HiggsVBF125_nano', '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM', 'CMS', '.*root', 1.0)
sync = cfg.MCComponent(
    'sync',
    ['AE1D1509-EE2D-3F49-8109-9595D4963A92.root','90DCD1FC-D0FD-C04D-ACAE-926D2D153A3B.root','08393EF3-F3C3-2745-973E-A6B0E179CCC5.root']
    )

#selectedComponents = [HiggsVBF125_nano]
selectedComponents = [sync]


from CMGTools.H2TauTau.heppy.sequence.common import samples_lists
from CMGTools.RootTools.utils.splitFactor import splitFactor

n_events_per_job = 1e6

for sample in selectedComponents:
    sample.splitFactor = splitFactor(sample, n_events_per_job)





from CMGTools.H2TauTau.heppy.analyzers.colin.Printer import Printer
printer = cfg.Analyzer(
    Printer
)


from CMGTools.H2TauTau.heppy.analyzers.ece.Reader import Reader , EventInfoReader


from CMGTools.H2TauTau.heppy.objects.event import Event
eventInfoReader = cfg.Analyzer(
    EventInfoReader,
    desired_infos = ['run','luminosityBlock','event'],
    src_class = Event 
)

from CMGTools.H2TauTau.heppy.objects.jet import Jet
jet_reader = cfg.Analyzer(
    Reader, 
   collection_name = 'Jet',
   output = 'jets',
   src_class = Jet
)

from CMGTools.H2TauTau.heppy.objects.tau import Tau
tau_reader = cfg.Analyzer(
    Reader, 
   collection_name = 'Tau',
   output = 'taus',
   src_class = Tau
)

from CMGTools.H2TauTau.heppy.objects.muon import Muon
muon_reader = cfg.Analyzer(
    Reader,
   collection_name = 'Muon',
   output = 'muons',
   src_class = Muon
)

from CMGTools.H2TauTau.heppy.objects.electron import Electron
electron_reader = cfg.Analyzer(
    Reader,
   collection_name = 'Electron',
   output = 'electrons',
   src_class = Electron
)

from CMGTools.H2TauTau.heppy.objects.met import MET
met_reader = cfg.Analyzer(
   EventInfoReader,
   desired_infos = ['MET_pt','MET_phi','MET_sumEt']
)

from CMGTools.H2TauTau.heppy.objects.genparticle import GenParticle
genparticle_reader = cfg.Analyzer(
    Reader,
   collection_name = 'GenPart',
   output = 'GenParticles',
   src_class = GenParticle
)

from CMGTools.H2TauTau.heppy.objects.primaryvertex import PrimaryVertex
primaryvertex_reader = cfg.Analyzer(
   EventInfoReader,
   desired_infos = ['PV_npvsGood','PV_npvs','PV_ndof','PV_x','PV_y','PV_z']
)


###############
# Analyzers 
###############

########### For before dilepton



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
    jetCol='jets',
    genPtCut=8.,
    genmatching = True,
    filter_func = select_leptons
)

from CMGTools.H2TauTau.heppy.analyzers.TauP4Scaler import TauP4Scaler
tauenergyscale = cfg.Analyzer(
    TauP4Scaler,
    'tauenergyscale',
    src = 'taus',
    systematics = False #Later make it True
)


########### For after dilepton



#This is to select the taus with a certain requirement.
def select_tau(tau):
    #print("tau before selection: ", tau.pt()  )
    #print("compare dz", tau.leadChargedHadrCand().dz() , tau.dz()  )
    #print("tau decayModeFinding",  tau.tauID('decayModeFinding')  )
    #print("tau byVVLooseIsolationMVArun2017v2DBoldDMwLT2017",  tau.tauID('byVVLooseIsolationMVArun2017v2DBoldDMwLT2017')  )
    #print("gen_match" , tau.gen_match)
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

def select_muon_third_lepton_veto(muon):
    return muon.pt() > 10             and \
        abs(muon.eta()) < 2.4         and \
        muon.isMediumMuon()  and \
        abs(muon.dxy()) < 0.045       and \
        abs(muon.dz())  < 0.2         and \
        muon.iso_htt < 0.3

sel_muons_third_lepton_veto = cfg.Analyzer(
    Selector,
    '3lepv_muons',
    output = 'sel_muons_third_lepton_veto',
    src = 'muons',
    filter_func = select_muon_third_lepton_veto
)


from CMGTools.H2TauTau.heppy.analyzers.EventFilter import EventFilter

#This is to require an event with at least 2 tau in it.
two_tau = cfg.Analyzer(
    EventFilter,
    'two_tau',
    src = 'sel_taus',
    filter_func = lambda x : len(x)>1
)

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
    print("I am in the sorting metric")
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
    return (-most_isolated_tau_isolation, -most_isolated_tau_pt,-least_isolated_tau_isolation,-least_isolated_tau_pt)

from CMGTools.H2TauTau.heppy.analyzers.Sorter import Sorter
dilepton_sorted = cfg.Analyzer(
    Sorter,
    output = 'dileptons_sorted',
    src = 'dileptons',
    metric = sorting_metric,
    reverse = False
    )

'''
sequence_dilepton = cfg.Sequence([
        sel_taus,
        two_tau,
        dilepton,
        dilepton_sorted,
        ])
'''

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
           'EToTaufake':'VLoose',
           'Unknown':'Unknown'}
)



from CMGTools.H2TauTau.heppy.ntuple.tools import Block , EventContent , Variable , to_leg
v = Variable


nano_tau1_vars = Block(
    	'tau1', lambda x: x.sel_taus[0],
	tau1_pt = v(lambda x: x.pt()),
	tau1_eta = v(lambda x: x.eta()),
	tau1_phi = v(lambda x: x.phi()),
	tau1_m = v(lambda x: x.mass()),
	tau1_q = v(lambda x: x.charge()),
	tau1_dz =  v(lambda x: x.dz()),
        tau1_decayMode = v(lambda x: x.decayMode()),
        tau1_idDecayMode = v(lambda x: x.tauID('decayModeFinding')),
        tau1_idDecayModeNewDMs = v(lambda x: x.tauID('decayModeFindingNewDMs')),
	tau1_idMVAoldDM2017v2 = v(lambda x: x.tauID('byVVLooseIsolationMVArun2017v2DBoldDMwLT2017')),
	tau1_gen_match = v(lambda x: x.gen_match)
    	)


nano_tau2_vars = Block(
    	'tau2', lambda x: x.sel_taus[1],
	tau2_pt = v(lambda x: x.pt()),
	tau2_eta = v(lambda x: x.eta()),
	tau2_phi = v(lambda x: x.phi()),
	tau2_m = v(lambda x: x.mass()),
	tau2_q = v(lambda x: x.charge()),
	tau2_dz =  v(lambda x: x.dz()),
        tau2_decayMode = v(lambda x: x.decayMode()),
        tau2_idDecayMode = v(lambda x: x.tauID('decayModeFinding')),
        tau2_idDecayModeNewDMs = v(lambda x: x.tauID('decayModeFindingNewDMs')),
	tau2_idMVAoldDM2017v2 = v(lambda x: x.tauID('byVVLooseIsolationMVArun2017v2DBoldDMwLT2017')),
	tau2_gen_match = v(lambda x: x.gen_match)
    	)



event_vars = Block(
    'event', lambda x: x,
    run = v(lambda x: x.run, int),
    lumi = v(lambda x: x.luminosityBlock, int),
    event = v(lambda x: x.event, int, 'l'),
    pv = v(lambda x:x.PV_z),
    #n_up = v(lambda x: getattr(x, 'NUP', default), int),
    #n_pu = v(lambda x: getattr(x, 'nPU', default) if getattr(x, 'nPU', default) is not None else default, int),# to handle data and embedded samples
    #n_pv = v(lambda x: len(x.vertices), int),
    #rho = v(lambda x: x.rho),
    #is_data = v(lambda x: x.input.eventAuxiliary().isRealData(), int),
    )



electron_vars = Block(
    'ele' , lambda x: x.electrons[0],
    ele_pt = v(lambda x: x.pt()),
    #id_e_mva_nt_loose = v(lambda x: x.physObj.userFloat("ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values")),
    #weight_tracking = v(lambda x: getattr(x, 'weight_trk', 1. )),
    #iso = v(lambda x: x.iso_htt()),
    ele_d0 = v(lambda x: x.dxy()),
    ele_dz = v(lambda x: x.dz()),
    #weight_trig_e = v(lambda x: getattr(x, 'weight_trigger_e', 1.)),
    #weight_trig_et = v(lambda x: getattr(x, 'weight_trigger_et', 1.)),
)


muon_vars = Block(
    'muo' , lambda x: x.sel_muons_third_lepton_veto[0],
    muo_weight_tracking = v(lambda x: getattr(x, 'weight_tracking', 1. )),
    muo_iso = v(lambda x: x.iso_htt),
    muo_pt = v(lambda x: x.pt()),
    muo_phi = v(lambda x: x.phi()),
    muo_eta = v(lambda x: x.eta()),
    muo_d0 = v(lambda x: x.dxy()),
    muo_dz = v(lambda x: x.dz()),
    muo_weight_trig_m = v(lambda x: getattr(x, 'weight_trigger_m', 1.)),
    muo_weight_trig_mt = v(lambda x: getattr(x, 'weight_trigger_mt', 1.)),
)



metvars = Block(
    'metvars', lambda x: x,
    met = v(lambda x: x.MET_pt),
    metphi = v(lambda x: x.MET_phi),
)


nano_tautau = EventContent(
    [
#    metvars,
    event_vars,
#    nano_tau1_vars,
#    nano_tau2_vars,
#    electron_vars,
    muon_vars
#    dilepton_vars
     ]
)


skim_func = lambda x: True

from CMGTools.H2TauTau.heppy.analyzers.NtupleProducer import NtupleProducer

ntuple = cfg.Analyzer(
    NtupleProducer,
    name = 'NtupleProducer',
    treename = 'events',
    event_content = nano_tautau,
    skim_func = skim_func
)


sequence_beforedil = cfg.Sequence([
        eventInfoReader,
#	genparticle_reader,
#	jet_reader,
        primaryvertex_reader,
#	tau_reader,
#        sel_taus,
#	two_tau,
#	at_least_one_tau
	muon_reader,
	sel_muons_third_lepton_veto,
	at_least_one_muo
#	electron_reader,
#       mcweighter,
#       json,
#       skim,
#       vertex,
#        taus,
#       muons,
#       electrons,
#        genmatcher
#	tauenergyscale,
#	met_reader,
#	sel_muons_third_lepton_veto,
#	sel_muons_third_lepton_veto_cleaned
])



sequence = sequence_beforedil
#sequence.extend( sequence_dilepton )
#sequence.append(tauidweighter_general)
#sequence.append(tauidweighter)
sequence.append(printer)
sequence.append(ntuple)


if events_to_pick:
    from CMGTools.H2TauTau.htt_ntuple_base_cff import eventSelector
    eventSelector.toSelect = events_to_pick
    sequence.insert(0, eventSelector)


from PhysicsTools.HeppyCore.framework.chain import Chain as Events
Events.tree_name = 'Events'
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                    )
#import pdb;pdb.set_trace()
print(config)

