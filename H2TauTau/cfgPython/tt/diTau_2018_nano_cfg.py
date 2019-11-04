import os
import re

import ROOT

import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption


import logging
logging.shutdown()
# reload(logging)
logging.basicConfig(level=logging.INFO)

from PhysicsTools.HeppyCore.framework.event import Event
Event.print_patterns = ['*taus*', '*muons*', '*electrons*', 'veto_*', 
                        '*dileptons_*', '*jets*']


###############
# Components
###############

sync = cfg.MCComponent(
    'sync',
    ['test.root']
    )

selectedComponents = [sync]


from CMGTools.H2TauTau.heppy.analyzers.colin.Printer import Printer
printer = cfg.Analyzer(
    Printer
)


from CMGTools.H2TauTau.heppy.analyzers.ece.Reader import Reader
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

###############
# Analyzers 
###############

from CMGTools.H2TauTau.heppy.analyzers.Selector import Selector

#This is to select the taus with a certain requirement.
def select_tau(tau):
    #print("tau before selection: ", tau.pt()  )
    #print("compare dz", tau.leadChargedHadrCand().dz() , tau.dz()  )
    #print("tau decayModeFinding",  tau.tauID('decayModeFinding')  )
    #print("tau byVVLooseIsolationMVArun2017v2DBoldDMwLT2017",  tau.tauID('byVVLooseIsolationMVArun2017v2DBoldDMwLT2017')  )
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

#This is to require an event with at least 2 tau in it.
two_tau = cfg.Analyzer(
    EventFilter,
    'two_tau',
    src = 'sel_taus',
    filter_func = lambda x : len(x)>1
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



from CMGTools.H2TauTau.heppy.ntuple.tools import Block , EventContent , Variable , to_leg
v = Variable


nano_tau_vars = Block(
    	'tau', lambda x: x.sel_taus[0],
	tau_pt = v(lambda x: x.pt()),
	tau_eta = v(lambda x: x.eta()),
	tau_phi = v(lambda x: x.phi()),
	tau_m = v(lambda x: x.mass()),
	tau_q = v(lambda x: x.charge()),
	tau_dz =  v(lambda x: x.dz()),
	tau_idDecayMode = v(lambda x: x.idDecayMode()),
	tau_idMVAoldDM2017v2 = v(lambda x: x.idMVAoldDM2017v2())
    	)

nano_tautau = EventContent(
    [
    nano_tau_vars,
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


sequence = cfg.Sequence(
[
jet_reader,
tau_reader,
]
)
sequence.extend( sequence_dilepton )
#sequence.append(tauidweighter_general)
#sequence.append(tauidweighter)
sequence.append(printer)
sequence.append(ntuple)

from PhysicsTools.HeppyCore.framework.chain import Chain as Events
Events.tree_name = 'Events'
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                    )
#import pdb;pdb.set_trace()
print(config)

