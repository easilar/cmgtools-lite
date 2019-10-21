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

#TODO 
#Select two taus among 
#Write the Taus you selected to the ntuple


#skim_func = lambda x: True
#
#from CMGTools.H2TauTau.heppy.analyzers.NtupleProducer import NtupleProducer
#from CMGTools.H2TauTau.heppy.ntuple.ntuple_variables import  nano_tautau as event_content_nanotautau
#
#ntuple = cfg.Analyzer(
#    NtupleProducer,
#    name = 'NtupleProducer',
#    treename = 'events',
#    event_content = event_content_nanotautau,
#    skim_func = skim_func
#)


sequence = cfg.Sequence(
[
jet_reader,
tau_reader,
printer,
#ntuple
]
)

from PhysicsTools.HeppyCore.framework.chain import Chain as Events
Events.tree_name = 'Events'
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                    )
#import pdb;pdb.set_trace()
print(config)

