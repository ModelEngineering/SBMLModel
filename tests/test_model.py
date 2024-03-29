import SBMLModel.constants as cn
import SBMLModel as anl
import SBMLModel.model as mdl
from SBMLModel import rpickle
from SBMLModel import util

import os
import pandas as pd
import numpy as np
import tellurium as te
import unittest


IGNORE_TEST = False
IS_PLOT = False
SIZE = 10
times = [1.0*n for n in range(SIZE)]
MODEL = """
J1: A->B; k1*A; 
J2: B->A; k2*B; 
k1 = 1
k2 = 1
A=10; B=0;
"""
#MODEL = "A -> B; 1"
MODEL_RR = te.loada(MODEL)
DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE1 = os.path.join(DIR, "test_model_serializer.pcl")
FILES = [TEST_FILE1]
        

#############################
# Tests
#############################
class TestModel(unittest.TestCase):

    def setUp(self):
        self._remove()
        self.model_reference = MODEL
        self.model = anl.Model(self.model_reference)

    def tearDown(self):
        self._remove()

    def _remove(self):
        for ffile in FILES:
            if os.path.isfile(ffile):
                os.remove(ffile)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertEqual(self.model.model_reference, self.model_reference)
        for idx in [1, 2]:
            parameter_name = "k%d" % idx
            reaction_name = "J%d" % idx
            self.assertTrue(parameter_name in self.model.kinetic_dct[reaction_name])

    def testGet(self):
        if IGNORE_TEST:
            return
        dct = {"A": 10, "k1": 1, "J1": 10.0}
        for name, value in dct.items():
            self.assertEqual(self.model.get(name), value, "No match for %s" % name)

    def testSet(self):
        if IGNORE_TEST:
            return
        dct = {"A": 20, "k1": 2}
        self.model.set(dct)
        for name, value in dct.items():
            self.assertEqual(self.model.get(name), value, "No match for %s" % name)

    def testSetTime(self):
        if IGNORE_TEST:
            return
        self.model.setTime(0)
        A_0 = self.model.get("A")
        self.model.setTime(5)
        A_5 = self.model.get("A")
        self.assertGreater(A_0, A_5)

    def testSimulate(self):
        if IGNORE_TEST:
            return
        num_point = 100
        ts = self.model.simulate(0, 20, num_point)
        diff = np.abs(self.model.get("A") - self.model.get("B"))
        self.assertLess(diff, 0.001)
        self.assertEqual(len(ts), num_point)
        #
        noise_ts = self.model.simulate(0, 20, num_point, noise_mag=0.1)
        diff_df = noise_ts - ts
        variance = np.var(diff_df.values.flatten())
        expected = 1/12*1/len(diff_df)
        self.assertLess(np.abs(variance - expected), 0.01)

    def testRpSerialize(self):
        if IGNORE_TEST:
            return
        dct = dict(self.model.__dict__)
        self.model.rpSerialize(dct)
        self.assertEqual(dct[mdl.ANTIMONY], self.model.antimony)
        self.assertTrue(mdl.DESERIALIZATION_DCT in dct.keys())

    def testRpDeserialize(self):
        if IGNORE_TEST:
            return
        # Construct the full dictionary
        model = anl.Model(self.model_reference)
        dct = dict(self.model.__dict__)
        self.model.rpSerialize(dct)
        self.model.__dict__ = dct
        self.model.rpDeserialize()
        self.assertTrue(model.isEqual(self.model))

    def testCopy(self):
        if IGNORE_TEST:
            return
        model = self.model.copy()
        self.assertTrue(model.isEqual(self.model))

    def testSerializeDeserialize(self):
        if IGNORE_TEST:
            return
        model = self.model.copy()
        with open(TEST_FILE1, "wb") as fd:
            rpickle.dump(model, fd)
        with open(TEST_FILE1, "rb") as fd:
            new_model = rpickle.load(fd)
        self.assertTrue(model.isEqual(new_model))

    def testGetBiomodel(self):
        if IGNORE_TEST:
            return
        model = anl.Model.getBiomodel(12)
        self.assertTrue("Model" in str(type(model)))
        self.assertGreater(len(model.species_names), 0)

    def testIterateBiomodels(self):
        if IGNORE_TEST:
            return
        def test(start_num, min_count):
            count = 0
            for num, model in \
                  anl.Model.iterateBiomodels(start_num=start_num, num_model=2):
                count += 1
                if model is not None:
                    self.assertTrue("Model" in str(type(model)))
            self.assertGreaterEqual(count, min_count)
        #
        test(1, 1)
        test(2000, 0)

    def testCalculateStds(self):
        if IGNORE_TEST:
            return
        ser = self.model.calculateStds()
        self.assertTrue(np.isclose(ser["A"], ser["B"]))
        

if __name__ == '__main__':
  unittest.main()
