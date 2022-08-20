"""Creates a Roadrunner instance from a model reference."""


ANT = "ant"
XML = "xml"

def makeRoadrunner(model_reference):
    """
    Creates a roadrunner instance from a model reference.

    Parameters
    ----------
    model_reference: str/ExtendedRoadrunner
        Roadrunner object
        URL (http:...)
        Antimony file (extension is .ant)
        XML file (extension is .xml)
        XML string
        Antimony string
    
    Returns
    -------
    ExtendedRoadrunner object
    """
    import tellurium as te
    if "RoadRunner" in str(type(model_reference)):
        return model_reference
    #
    if not isinstance(model_reference, str):
        raise ValueError("Invalid model reference")
    #
    if model_reference[0:4] == "http":
        return te.loadSBMLModel(model_reference)
    #
    parts = model_reference.split(".")
    if len(parts) == 2:
        if parts[1] == XML:
            return te.loadSBMLModel(model_reference)
        elif parts[1] == ANT:
            return te.loadAntimonyModel(model_reference)
        else:
            # Assume string for antimony model
            return te.loada(model_reference)
    else:
        if XML in model_reference[0:10]:
            try:
                return te.loads(model_reference)
            except RuntimeError:
                idx = model_reference.find("BIOMD")
                if idx < 0:
                    model_descriptor = model_reference
                else:
                    model_descriptor = model_reference[idx:idx+15]
                raise ValueError("Cannot create model %s"
                      % model_descriptor)
        return te.loada(model_reference)
