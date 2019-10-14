from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

import sys
import pprint
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection

class Printer(Analyzer):

    def beginLoop(self, setup):
        super(Printer, self).beginLoop(setup)
        self.counters.addCounter('Counter')
        self.count = self.counters.counter('Counter')
        self.count.register('All Events')
        self.count.register('>= 2 jets')
        

    def process(self, event):
        self.count.inc('All Events')
        jets = Collection(event.input, 'Jet')
        taus = Collection(event.input, 'Tau')
        njets = 0
        for i,jet in enumerate(jets): 
            if jet.pt<50: 
                njets = i
        if njets >= 2: 
            self.count.inc('>= 2 jets')

