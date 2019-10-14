# Reading Nano AOD

Follow [The usual instructions](https://github.com/GaelTouquet/cmgtools-lite/tree/htt_9_4_11_cand1_v1/H2TauTau#installation-recipe). 

Update to these branches: 

* CMGTools : cbernet/nano_aod
* CMSSW : cbernet/nano_aod

Get a test file: 

xrdcp root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv5/VBFHToTauTau_M125_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/260000/90DCD1FC-D0FD-C04D-ACAE-926D2D153A3B.root test.root

Run: 

```
heppy Trash diTau_2018_nano_cfg.py 
```

Check the results: 

```
cat Trash/sync/CMGTools.H2TauTau.heppy.analyzers.colin.Printer.Printer_1/Counter.txt
```

