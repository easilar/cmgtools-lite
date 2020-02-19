from nano_object import NanoObject

class Jet(NanoObject):
	def __init__(self, *args, **kwargs):
		super(Jet, self).__init__(*args, **kwargs)

	def jetID(self, id_name):
		if id_name=="POG_PFID_Tight": return self.jetId()>=2
		if id_name=="POG_PFID_Loose": return self.jetId()>=1
		if id_name=="POG_PFOD_tightLepVeto" : return self.jetId()>=3
		else: return -999
