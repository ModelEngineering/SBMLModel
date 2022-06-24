# TELLURIUM ANALYSIS
This package provides infrastructure for analyzing SBML models using Tellurium.
The scope includes:
* convenient access to static model inforation (parameters, species, reactions)
* support for retrieving and setting values of parameters
* creating a roadrunner from any source that roadrunner supports using a single constructor
* common data structure for simulation results
* flexible and simplified plotting

# Details
The main class is ``TelluriumAnalyzer``. This has the properties:
* ``roadrunner``: a roadrunner object
* species_names: a list of all species names
* reaction_names: a list of all reaction names
* parameter_names: a list of all parameter names
Key methods are:
* getParameter(parameterName, lower_bound, upper_bound)->Parameter
* simulate(start_time, end_time, points_per_time)->Timeseries
* set(parameterName, value)
* get(parameterName)
* getTime(): returns the current simulation time
* setTime(time): runs the simulation from time 0 to the specified time

The ``Timeseries`` class provides a way to contain data taken from the same times
* Timeseries(dataframe)
* mat2TS: converts a matrix to a timeseries

# Release Notes
* Version 0.1.1
