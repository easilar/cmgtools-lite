from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

import sys
import pprint
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from CMGTools.H2TauTau.heppy.objects.nano_object import NanoObject
from CMGTools.H2TauTau.heppy.objects.jet import Jet

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
        #jet = Jet(jets[0])
        #jet.bar()
        #jet.pt()
        njets = 0
        for i,jet in enumerate(jets): 
            if jet.pt<50: 
                njets = i
        if njets >= 2: 
            self.count.inc('>= 2 jets')

    def __str__(self):
        return pprint.pformat(Jet.not_implemented)
        
