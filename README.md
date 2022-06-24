# ANALYZE SBML
This package provides infrastructure for analyzing SBML models using Tellurium.
The scope includes:
* convenient access to static model inforation (parameters, species, reactions)
* support for retrieving and setting values of parameters
* creating a roadrunner from any source that roadrunner supports using a single constructor
* common data structure for simulation results
* flexible and simplified plotting

# Details
The main class is ``Model``, an analysis abstraction for an SBML model.
Key properties are:
* ``roadrunner``: a roadrunner object
* species_names: a list of all species names
* reaction_names: a list of all reaction names
* parameter_names: a list of all parameter names

Key methods are:
* simulate(start_time, end_time, points_per_time, variables)->Timeseries
* set(name, value) - set a name to a value
* get(name) - retrieve the value of a name
* getTime(): returns the current simulation time
* setTime(time): runs the simulation from time 0 to the specified time
* diagram: display a diagram of the reaction network

The ``Timeseries`` class provides a way to contain data taken from the same times
* Timeseries(dataframe)
* mat2TS: converts a matrix to a timeseries

The ``Parameter`` class describes parameter constraints.
* Constructor: parameterName, lower_bound, upper_bound
* value: value of the parameter
* name: name of the parameter

# Developer Notes
1. Graphics on Ubuntu requires tkinter. Use ``sudo apt install python3.8-tk``.

# Release Notes
* Version 0.1.1
