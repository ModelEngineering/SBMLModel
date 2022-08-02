import SBMLModel.constants as cn
from SBMLModel.option_manager import OptionManager
from SBMLModel.options import Options

from docstring_expander.expander import Expander
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def makeSimulationTimes(start_time=cn.START_TIME, end_time=cn.END_TIME,
      points_per_time=cn.POINTS_PER_TIME):
    """
    Constructs the times for a simulation using the simulation options.

    Parameters
    ----------
    start_time: float
    end_time: float
    points_per_time: int
    
    Returns
    -------
    np.ndarray
    """
    num_point = int(points_per_time*(end_time - start_time))
    dt = (end_time - start_time)/num_point
    times = [start_time + dt*n for n in range(num_point)]
    times.append(end_time)  # Include the endpoint
    return np.array(times)

def mat2DF(mat, column_names=None, row_names=None):
    """
    Converts a numpy ndarray or array-like to a DataFrame.

    Parameters
    ----------
    mat: np.Array, NamedArray, DataFrame
    column_names: list-str
    row_names: list-str
    """
    if isinstance(mat, pd.DataFrame):
        df = mat
    else:
        if len(np.shape(mat)) == 1:
            mat = np.reshape(mat, (len(mat), 1))
        if column_names is None:
            if hasattr(mat, "colnames"):
                column_names = mat.colnames
        if column_names is not None:
            if len(column_names) == 0:
                column_names = None
        if row_names is None:
            if hasattr(mat, "rownames"):
                if len(mat.rownames) > 0:
                    row_names = mat.rownames
        if row_names is not None:
            if len(row_names) == 0:
                row_names = None
        df = pd.DataFrame(mat, columns=column_names, index=row_names)
    return df

def ppMat(mat, column_names=None, row_names=None, is_print=True):
    """
    Provides a pretty print for a matrix or DataFrame)

    Parameters
    ----------
    mat: np.Array, NamedArray, DataFrame
    column_names: list-str
    row_names: list-str
    """
    df = mat2DF(mat, column_names=column_names, row_names=row_names)
    if is_print:
        print(df)

# TODO: Tests
def makeRoadrunnerSer(roadrunner, names):
    """
    Contructs a Series for the roadrunner names.

    Parameters
    ----------
    roadrunner: ExtendedRoadrunner
    names: list-str

    Returns
    -------
    pd.Series
    """
    values = list(getRoadrunnerValue(roadrunner, names).values())
    return pd.Series(values, index=names)

# TODO: Tests
def getRoadrunnerValue(roadrunner, names):
    """
    Provides the roadrunner values for a name. If no name,
    then all values are given.

    Parameters
    ----------
    roadrunner: ExtendedRoadrunner
    name: str/list-str

    Returns
    -------
    object/dict
    """
    if isinstance(names, str):
        return roadrunner[names]
    if names is None:
        names = roadrunner.keys()
    return {n: roadrunner[n] for n in names}

# TODO: Tests
def setRoadrunnerValue(roadrunner, name_dct):
    """
    Sets the values of names and values.

    Parameters
    ----------
    name_dct: dict
        key: str
        value: value
    """
    for name, value in name_dct.items():
        if isinstance(value, int):
            value = float(value)
        roadrunner[name] = value

def isNumber(item):
    return isinstance(item, float) or isinstance(item, int)

def isEqual(items1, items2):
    """
    Checks for equality for lists of simple types.

    Parameters
    ----------
    items1: list-like or dict or simple type
    items2: list-like or dict or simple type
    
    Returns
    -------
    bool
    """
    is_simple = False
    for s_type in [int, str, float, bool]:
        is_simple = is_simple or isinstance(items1, s_type)
    if is_simple:
        return items1 == items2
    # Handle lists and dicts
    if isinstance(items1, dict):
        if isinstance(items2, dict):
            diff = set(items1.keys()).symmetric_difference(items2.keys())
            if len(diff) > 0:
                return False
            trues = [v1 == v2 for v1, v2 in zip(items1.values(), items2.values())]
        else:
            return False
    else:
        items1 = list(items1)
        items2 = list(items2)
        trues = [l1 == l2 for l1, l2 in zip(items1, items2)]
    #
    return all(trues)
