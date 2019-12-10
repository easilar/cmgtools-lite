import ROOT
from nano_object import NanoObject


class Tau(NanoObject):


	def __init__(self, *args, **kwargs):
		super(Tau, self).__init__(*args, **kwargs)
		self.rawp4 = ROOT.math.PtEtaPhiMLorentzVector(self.pt(),self.eta(),self.phi(),self.mass())
		self.lv = self.rawp4

	def leadChargedHadrCand(self):
		return self #FIXME

	def tauID(self, mode):
		tauID_dict = {
		"decayModeFinding":self.idDecayMode(),
		"decayModeFindingNewDMs":self.idDecayModeNewDMs(),
		"byVVLooseIsolationMVArun2017v2DBoldDMwLT2017":self.idMVAoldDM2017v2()>=1 , 
		"byIsolationMVArun2017v2DBoldDMwLTraw2017":self.rawMVAoldDM2017v2()
		}
		return tauID_dict[mode]

	def pdgId(self):
		return 15*self.charge()

	def p4(self):
		return self.lv

	def rawpt(self):
		return self.pt()

	def __getattr__(self, attr):
		if attr == 'gen_match':
			if self.genPartFlav() == 0:
				return 6
			else:
				return self.genPartFlav()
		else:
			return super(Tau,self).__getattr__(attr)

	def scaleEnergy( self, scale ):
		p4 = self.rawp4
		p4 *= scale
		self.lv = p4

