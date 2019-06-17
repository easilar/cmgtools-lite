import unittest
import copy
from datasetdb import DatasetDB
from dataset import Dataset
from test_dataset import dspath


writedb = DatasetDB('writer')
readdb = DatasetDB('reader')

class TestDatasetDB(unittest.TestCase):
    
    def test_1_read(self): 
        '''test that a test entry can be read, in reader mode'''
        readdb
        data = list(readdb.coll.find({'path':'a'}))
        self.assertEqual(len(data),1)

    def test_2_writedummy(self):
        '''test writer mode'''
        dsdb = writedb
        dsdb.coll.insert({"path" : "aa", "name" : "bb", "subdir_pattern" : "*", 
                          "subdirs" : [ 0, 1 ], "tgz_pattern" : "*", "tgzs" : [ 2, 3 ]})
        data = list(dsdb.coll.find({'path':'aa'}))
        self.assertEqual(len(data),1)
        dsdb.coll.remove({'path':'aa'})
        with self.assertRaises(ValueError): 
            DatasetDB('foo')

    def test_3_writeds(self):
        '''test writing a real dataset to the db'''
        dataset = Dataset(dspath)
        info = dataset.info()
        writedb.coll.remove({'path':info['path']})
        writedb.insert(info)
        # test that the information has been inserted. 
        # there was no such dataset before
        rinfos = list(writedb.coll.find({'path':info['path']}))
        self.assertEqual(len(rinfos), 1)
        rinfo = rinfos[0]
        self.assertEqual(rinfo['path'], info['path'] )
        # now test update
        tgzs = copy.deepcopy(info['tgzs'])
        info['tgzs']['0000'].append('heppyOutput_666.tgz')
        writedb.insert(info)
        rinfos = list(writedb.coll.find({'path':info['path']}))
        self.assertEqual(len(rinfos), 1)
        rinfo = rinfos[0]
        self.assertEqual(len(rinfo['tgzs']['0000']), len(tgzs['0000'])+1)
        writedb.coll.remove({'path':info['path']})
                

if __name__ == '__main__': 
    unittest.main()
