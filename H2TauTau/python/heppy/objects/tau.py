import ROOT
from nano_object import NanoObject

class Tau(NanoObject):


	def leadChargedHadrCand(self):
		return self #FIXME

	def tauID(self, mode):
		tauID_dict = {
		"decayModeFinding":self.idDecayMode(),
		"decayModeFindingNewDMs":self.idDecayModeNewDMs(),
		"byVVLooseIsolationMVArun2017v2DBoldDMwLT2017":self.idMVAoldDM2017v2()==0, # VVLoose: 2^0=1  
		"byIsolationMVArun2017v2DBoldDMwLTraw2017":self.rawMVAoldDM2017v2()
		}
		return tauID_dict[mode]

	def pdgId(self):
		return 15*self.charge()

	def p4(self):
		p4 = ROOT.TLorentzVector()
		p4.SetPtEtaPhiM(self.pt(),self.eta(),self.phi(),self.mass())
		return p4

	def __getattr__(self, attr):
		if attr == 'gen_match':
			return self.genPartFlav()
		else:
			return super(Tau,self).__getattr__(attr)

	def scaleEnergy( self, scale ):
		p4 = self.p4()
		p4 *= scale 
		return p4  


