from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

import sys
import pprint
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection

class Reader(Analyzer):
	'''Read only the desired collections from the nanoAOD collections'''

	def process(self, event):
		collection = Collection(event.input, self.cfg_ana.collection_name) 
		objects = []
		for tmp_obj in collection:
			curr_obj = self.cfg_ana.src_class(tmp_obj)
			objects.append(curr_obj)
		setattr(event, self.cfg_ana.output, objects)

class EventInfoReader(Analyzer):
        '''Read only the desired information from event'''

        def process(self, event):
		desired_infos = self.cfg_ana.desired_infos
		for desired_info in desired_infos:
			res = getattr(event.input, desired_info)
                	setattr(event, desired_info, res)

