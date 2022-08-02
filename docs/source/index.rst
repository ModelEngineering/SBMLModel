.. analyzeSBML documentation master file, created by
   sphinx-quickstart on Mon Aug  1 12:04:43 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SBMLModel: A simple abstraction for simulation and analysis of SBML Models
==========================================================================

SBMLModel provides simple abtractions for doing simulation studies of individual
SBML Models as well as collections of SBML Models.
Some key features are:

#. A single constructor for many representations of an SBML model: antimony string, antimony file, XML string, XML file, ``roadrunner`` object.
#. ``get`` and ``set`` methods for any muteable simulation variable.
#. Properties for: ``species_names``, ``reaction_names``, ``kinetic_dct``, ``antimony`` for model.
#. ``pandas.DataFrame`` representation of simulation outputs via ``Timeseries``.
#. Plotting for single and multiple simulations using ``Timeseries``.



.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
