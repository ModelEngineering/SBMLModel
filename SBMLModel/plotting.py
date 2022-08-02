import SBMLModel as ta
import SBMLModel.constants as cn
from SBMLModel import util
from SBMLModel.option_manager import OptionManager
from SBMLModel.options import Options

from docstring_expander.expander import Expander
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


@Expander(cn.KWARGS, cn.PLOT_KWARGS)
def plotOneTS(ts, **kwargs):
    """
    Plots a dataframe as multiple lines on a single plot. The
    columns are legends.

    Parameters
    ----------
    ts: TimeSeries
    #@expand
    """
    mgr = OptionManager(kwargs)
    mgr.plot_opts.set(cn.O_XLABEL, default="time")
    ax = mgr.plot_opts.get(cn.O_AX)
    if ax is None:
        _, ax = plt.subplots(1)
    ax.plot(ts.times, ts)
    legend_spec = cn.LegendSpec(ts.columns, crd=mgr.plot_opts[cn.O_LEGEND_CRD])
    mgr.plot_opts.set(cn.O_LEGEND_SPEC, default=legend_spec)
    mgr.doPlotOpts()
    mgr.doFigOpts()

@Expander(cn.KWARGS, cn.PLOT_KWARGS)
def plotManyTS(*tss, ncol=1, names=None, **kwargs):
    """
    Plots multiple Timeseries with the same columns so that each column
     is a different plot.

    Parameters
    ----------
    tss: sequence of Timeseries
    ncol: int (number of columns)
    names: list-str
        Names of the dataframes
    #@expand
    """
    mgr = OptionManager(kwargs)
    mgr.plot_opts.set(cn.O_XLABEL, default="time")
    nrow = int(np.ceil(len(tss[0].columns)/ncol))
    fig, axes = plt.subplots(nrow, ncol)
    axes = np.reshape(axes, (nrow, ncol))
    columns = list(tss[0].columns)
    for idx, col in enumerate(columns):
        new_mgr = mgr.copy()
        irow = int(np.floor(idx/ncol))
        icol = idx - irow*ncol
        ax = axes[irow, icol]
        new_mgr.plot_opts.set(cn.O_AX, default=ax)
        new_mgr.plot_opts.set(cn.O_TITLE, default=col)
        for ts_idx, ts in enumerate(tss):
            try:
                values = ts[col]
            except KeyError:
                raise ValueError("DataFrame %d lacks column %s"
                      % (ts_idx, col))
            ax.plot(ts.times, ts[col])
        if names is not None:
            legend_spec = cn.LegendSpec(names,
                   crd=new_mgr.plot_opts[cn.O_LEGEND_CRD])
            new_mgr.plot_opts.set(cn.O_LEGEND_SPEC, default=legend_spec)
        new_mgr.doPlotOpts()
    mgr.doFigOpts()

def plotMat(mat, column_names=None, row_names=None, is_plot=True, **kwargs):
    """
    Creates a heatmap for the matrix.

    Parameters
    ----------
    mat: np.Array, NamedArray, DataFrame
    column_names: list-str
    row_names: list-str
    """
    df = util.mat2DF(mat, column_names=column_names, row_names=row_names)
    if is_plot:
        mgr = OptionManager(kwargs)
        ax = mgr.getAx()
        sns.heatmap(df, cmap="seismic", ax=ax)
        mgr.doPlotOpts()
        mgr.doFigOpts()
