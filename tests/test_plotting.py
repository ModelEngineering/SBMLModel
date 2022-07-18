import analyzeSBML as ans
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

    def testPlotOneTS(self):
        if IGNORE_TEST:
          return
        ans.plotOneTS(TS, ylabel="values", xlabel="sec",
              is_plot=IS_PLOT)

    def testPlotManyTS(self):
        if IGNORE_TEST:
          return
        df = TS.applymap(lambda v: 100*v)
        ts = Timeseries(df, times=df.index)
        ans.plotManyTS(TS, ts, ylabel="values", xlabel="sec",
              is_plot=IS_PLOT, names=["first", "second"])
        ans.plotManyTS(TS, ts, ylabel="values", xlabel="sec",
              is_plot=IS_PLOT, names=["first", "second"], ncol=2)

    def testPlotMat(self):
        if IGNORE_TEST:
          return
        for mat in [MAT, NAMED_ARRAY, DF]:
            ans.plotMat(mat, title="test", figsize=(5,5), is_plot=IS_PLOT)

if __name__ == '__main__':
  unittest.main()
