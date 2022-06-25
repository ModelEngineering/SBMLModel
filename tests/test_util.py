import analyzeSBML as ta
from analyzeSBML import util
from analyzeSBML.timeseries import Timeseries
import analyzeSBML.constants as cn

import pandas as pd
import numpy as np
import tellurium as te
import unittest


IGNORE_TEST = False
IS_PLOT = False
SIZE = 10
if IS_PLOT:
    import matplotlib
    matplotlib.use('TkAgg')
times = [1.0*n for n in range(SIZE)]
TS = Timeseries(pd.DataFrame({"a": range(SIZE)}), times=times)
TS["b"] = 10*TS["a"]
MDL = "A->B; 1; A=0; B=0;"
MDL_RR = te.loada(MDL)
NAMED_ARRAY = MDL_RR.simulate()
MAT = np.array(range(10))
MAT = np.reshape(MAT, (2, 5))
DF = pd.DataFrame(NAMED_ARRAY, columns=NAMED_ARRAY.colnames)
        

#############################
# Tests
#############################
class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass
 
    def testPlotOneTS(self):
        if IGNORE_TEST:
          return
        ta.plotOneTS(TS, ylabel="values", xlabel="sec",
              is_plot=IS_PLOT)

    def testPlotManyTS(self):
        if IGNORE_TEST:
          return
        df = TS.applymap(lambda v: 100*v)
        ts = Timeseries(df, times=df.index)
        util.plotManyTS(TS, ts, ylabel="values", xlabel="sec",
              is_plot=IS_PLOT, names=["first", "second"])
        ta.plotManyTS(TS, ts, ylabel="values", xlabel="sec",
              is_plot=IS_PLOT, names=["first", "second"], ncol=2)

    def testMakeSimulationTimes(self):
        if IGNORE_TEST:
          return
        times = util.makeSimulationTimes()
        self.assertTrue(isinstance(times, np.ndarray))
        #
        times = util.makeSimulationTimes(start_time=1, end_time=4)
        self.assertTrue(times[0] == 1)
        self.assertTrue(times[-1] == 4)
        #
        time1s = util.makeSimulationTimes(start_time=1, end_time=4,
            points_per_time=100)
        self.assertGreater(len(time1s), len(times))

    def testPpMat(self):
        if IGNORE_TEST:
          return
        mat = np.array(range(10))
        result1 = util.ppMat(mat, column_names=["a"], is_print=IS_PLOT)
        mat = np.reshape(mat, (5,2))
        result2 = util.ppMat(mat, column_names=["a", "b"], is_print=IS_PLOT)

    def testMat2DF(self):
        if IGNORE_TEST:
          return
        for mat in [NAMED_ARRAY, DF]:
            df = util.mat2DF(mat)
            self.assertTrue(isinstance(df, pd.DataFrame))
            self.assertTrue(any(["A" in c for c in df.columns]))
        df = util.mat2DF(MAT)
        self.assertTrue(isinstance(df, pd.DataFrame))

    def testPlotMat(self):
        if IGNORE_TEST:
          return
        for mat in [MAT, NAMED_ARRAY, DF]:
            util.plotMat(mat, title="test", figsize=(5,5), is_plot=IS_PLOT)


if __name__ == '__main__':
  unittest.main()
