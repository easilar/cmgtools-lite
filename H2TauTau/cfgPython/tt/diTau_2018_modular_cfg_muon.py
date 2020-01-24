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

n_events_per_job = 3e6

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

at_least_one_muo = cfg.Analyzer(
    EventFilter,
    'muo',
    src = 'muons',
    filter_func = lambda x : len(x)>0
)




from CMGTools.H2TauTau.heppy.ntuple.tools import Block , EventContent , Variable , to_leg
v = Variable
default = v.default


muon_vars = Block(
        'muo', lambda x: x.muons[0],
    muo_pt = v(lambda x: x.pt()), 
    muo_eta = v(lambda x: x.eta()),
    muo_phi = v(lambda x: x.phi()),  
    muo_dxy = v(lambda x: x.dxy()),
    muo_dz = v(lambda x: x.dz()),  
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
    event_vars,
    muon_vars
     ]
)




# ntuple ================================================================

skim_func = lambda x: True

from CMGTools.H2TauTau.heppy.analyzers.NtupleProducer import NtupleProducer
ntuple = cfg.Analyzer(
    NtupleProducer,
    name = 'NtupleProducer',
    treename = 'events',
    event_content = tautau,
    skim_func = skim_func
)

sequence_beforedil = cfg.Sequence([
        json,
        skim,
        vertex,
        muons,
	at_least_one_muo,
])
sequence = sequence_beforedil
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
