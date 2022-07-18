Overview
========

``analyzeSBML`` simplifies
analysis of simulation outputs of SBML models
by providing simple interfaces for viewing and manipulating the model state
as well as saving models.
Also provided is a flexible system for plotting simulation outputs.
The core classes are:
* ``Model``, which provides an abstraction of an SBML model
* ``Timeseies``, which provides an abstraction of output of a dynamical simulation

``Model`` describes an SBML model in terms of following properties:
* ``antimony`` is a string representation of the model
* ``kinetic_dct`` is a dicionary with reaction name as key and the kinetics
formula as its value
* ``parameter_names`` is a list of strings of names of parameters
* ``reaction_names`` is a list of names of parameters
* ``species_names`` is a list of strings of names of floating species

Methods supported by ``Model`` include:
* ``copy`` creates a copy of the model, retaining the current time
* ``get`` retrieves the value of a parameter or species
* ``getTime`` returns the current simulation time
* ``isEqual`` tests if two models have the same values of the above properties
* ``set`` assigns a value to a parameter or species in the model
* ``setTime`` changes the simulation time to the desired value
* ``simulate`` runs the simulation from the current time

``Timeseries`` is a thin layer on top of a ``pandas`` ``DataFrame``.
``Timeseries`` is the common data structure used to represent simulation outputs.
The columns are names of species and/or reactions,
and the index is time in integer milliseconds.
The ``simulate`` method creates a ``Timeseries``,
and ``plotOneTS`` and ``plotManyTS`` require a ``Timeseries`` as input.

Several plots are available.
* ``plotOneTS`` plots all columns in a single graph
* ``plotManyTS`` plots multiple time series with the same columns;
there is one plot for each column.

In addition the following functions are available:
* ``dump`` saves a model to a file
* ``load`` creates a ``Model`` instance from an instance that was previously
saved to a file
* ``makeSimulationTimes`` provides a convenient way to construct an array
of simulation times based on start time, end time, and
the density of of points (points per time unit).
