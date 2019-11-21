import ROOT
from nano_object import NanoObject

class Muon(NanoObject):


	def __getattr__(self, attr):
		if attr in ['weight_trigger_mt','weight_tracking', 'weight_trigger_m']:
			return 1.0
		if attr == 'iso_htt':
			return self.pfRelIso04_all()
                else:
                        return super(Muon,self).__getattr__(attr)

	def isMediumMuon(self):
		return	self.mediumId()
