import ROOT
from nano_object import NanoObject

def calc_p4(obj):
        p4 = ROOT.TLorentzVector()
        p4.SetPtEtaPhiM(obj.pt(),obj.eta(),obj.phi(),obj.mass())
        return p4

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

	def p4(self):
                return calc_p4(self)



