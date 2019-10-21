from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

import sys
import pprint
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection

class Reader(Analyzer):
	'''Read only the desired collections from the nanoAOD collections'''

	def process(self, event):
		collection = Collection(event.input, self.cfg_ana.collection_name) 
		test_obj = self.cfg_ana.src_class(collection[0])
		print(test_obj.pt())
		setattr(event, self.cfg_ana.output, collection)
