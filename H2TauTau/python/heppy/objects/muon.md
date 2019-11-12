#Notes on variables:

##iso_htt : 
	the origin is `relIso` which can be found [here](https://github.com/cbernet/cmg-cmssw/blob/htt_9_4_11_cand1_v1/PhysicsTools/Heppy/python/physicsobjects/Lepton.py#L52)
	relIso uses `absIso` [here](https://github.com/cbernet/cmg-cmssw/blob/35a2337d63b683b79b63407fb5dcaeb00a8e5688/PhysicsTools/Heppy/python/physicsobjects/Lepton.py#L17)
	the isolation variables used in `absIso` can be found [here](https://github.com/cbernet/cmg-cmssw/blob/35a2337d63b683b79b63407fb5dcaeb00a8e5688/PhysicsTools/Heppy/python/physicsobjects/Muon.py#L119-L143)
	in `nanoaod`: [pfRelIso04_all](https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/muons_cff.py#L147)holds our definition of iso_htt with delta beta 0.5, cone radius (R) = 0.4
