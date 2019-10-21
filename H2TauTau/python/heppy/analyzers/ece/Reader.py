from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

import sys
import pprint
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection

class Reader(Analyzer):
	'''Read only the desired collections from the nanoAOD collections'''

	def process(self, event):
		collection = Collection(event.input, self.cfg_ana.collection_name) 
		if len(collection) > 0 :
			test_obj = self.cfg_ana.src_class(collection[0])
			print('collection name:' , self.cfg_ana.collection_name)
			print('leading obj pt:' , test_obj.pt())
		else:
			print("size of the collection is 0")
		setattr(event, self.cfg_ana.output, collection)
