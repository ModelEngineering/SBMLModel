"""
Adapations of pickle to make it more robust to changes in pickled objects.

Provides robustness by not serializing the methods of the target object, only
its __dict__. Deserializer involves: (a) create a default instantiation
of the object and (b) re-assigning its __dict__.

Objects for which this behavior is desired must inherit RPickler and
override the following methods as required:
    rpSerialize(self, dct): updates the __dict__ that is being serialized
    rpConstruct(cls): constructor used for a deserialized object
    rpDeserialize(self): updates the deserialized object

The folling is usage for an object obj.
    # Serialize the object and write to a file
    with open(path, "wb") as fd:
        dump(obj, fd)
    # Deserialize
    with open(path, "rb") as fd:
        new_obj = load(fd)

"""

import copy
import os
import pickle


class Serializer(object):
    """RPickler serializer of an object and its sub-objects."""

    def __init__(self, obj):
        """
        Parameters
        ----------
        obj: Object being serialized
        """
        self.cls = obj.__class__  # Class being serialized
        self.obj_dct = dict(obj.__dict__)  # __dict__ for the instance
        obj.rpSerialize(self.obj_dct)  # Optional editing of the instance dictionary

    def serialize(self):
        """
        Recursively constructs the serializer of the object.
        """
        for key, value in self.obj_dct.items():
            if issubclass(value.__class__, RPickler):
                self.obj_dct[key] = Serializer(value)
                self.obj_dct[key].serialize()

    def deserialize(self):
        """
        Recursively deserializes objects.

        Returns
        -------
        object
        """
        obj = self.cls.rpConstruct()
        # Recursively instantiate serialized objects.
        # Save as instances of the constructed object.
        for key, value in self.obj_dct.items():
            if isinstance(value, Serializer):
                obj.__dict__[key] = value.deserialize()
            else:
                obj.__dict__[key] = copy.deepcopy(value)
        # Revise the obj as required
        obj.rpDeserialize()
        #
        return obj

    

    def __repr__(self):
        return "Serializer of %s" % str(self.cls)


class RPickler():
    # Used by classes that implement robust pickling.

    def rpSerialize(self, dct):
        """
        Edits the serializer dictionary of what is serialized.
        
        Parameters
        ----------
        dct: dict
        """

    @classmethod
    def rpConstruct(cls):
        """
        Provides a default construction of an object.

        Returns
        -------
        Instance of cls
        """
        return cls()

    def rpDeserialize(self):
        """
        Provides a hook to modify instance variables after they have
        been initialized by RPickle.
        """


def dump(obj, fd):
    """
    Dumps the objects to a file.

    Parameters
    ----------
    obj: object to be serialized
    fd: file descriptor
    """
    # Construct the serializer
    serializer = Serializer(obj)
    serializer.serialize()
    # Serialize
    pickle.dump(serializer, fd)

def load(fd):
    """
    Restores a serialized object.

    Parameters
    ----------
    fd: file descriptor

    Returns
    -------
    object
    """
    serializer = pickle.load(fd)
    return serializer.deserialize()
