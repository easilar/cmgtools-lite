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



# from CMGTools.H2TauTau.heppy.analyzers.colin.Reader import Reader
# from CMGTools.H2TauTau.heppy.objects.jet import Jet
# jet_reader = cfg.Analyzer(
#     Reader, 
#    collection_name = 'Jet',
#    class_object = Jet,
#)

sequence = cfg.Sequence(
[printer]
)

from PhysicsTools.HeppyCore.framework.chain import Chain as Events
Events.tree_name = 'Events'
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                    )
print(config)

