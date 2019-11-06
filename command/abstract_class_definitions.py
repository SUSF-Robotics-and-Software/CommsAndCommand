import json


# all commands inherit from this, can be used to generate jsons
#   usage:
#   create subclass from this, overwrite the __init__ function
#   with all of the variables that the command has.


class command_primitive:
    """
        usage
        -----
            Do not use
            use this as a base class. Instances can then be used to hold
            command information, including other classes
    """
    name: str
    _excluded_properties: set

    def __init__(self):
        raise NotImplementedError(
            "create a subclass of this, overwrite __init__"
        )

    def __new__(cls, *args, **kwargs):
        """
            usage
            -----
                On creation of an instance of the class, (or subclasses) the
                methods of the class are added to `exclusion_list`. This
                exclusion list is part of every subclass, and will stop
                `get_structure` from including non-data attributes, which are
                defined by being included in the class definition, and not
                added in the __init__ constructor method. This allows for the
                hacky but quick `self.__dict__.update(locals())` to be used.

            returns
            -------
                new instance of the class, pre __init__
        """
        inst = super().__new__(cls)
        inst._excluded_properties = set(cls.__dict__.keys())
        inst._excluded_properties.add('_excluded_properties')
        return inst

    def get_non_excluded_attrs(self):
        non_excluded_dict = {}
        # iterates over the instance's __dict__ (contains all attributes)
        # if it's not excluded, it gets returned in a dict resembling
        # a trimmed __dict__
        # but Richard, why not just assume that people use public and private
        # properly?
        # good question...
        for key, value in self.__dict__.items():
            if key not in self.excluded_properties:
                non_excluded_dict[key] = value

        return non_excluded_dict

    def get_structure(self) -> dict:
        """
            usage
            -----
                returns a structural (__dict__) representation of the command
                sans `excluded_properties`, which should contain all the
                classes' base attributes

            returns
            -------
                dict of all attributes
        """
        structure_dict = {}
        for key, value in self.__dict__.items():
            if key not in self.excluded_properties:
                if issubclass(value, command_primative):
                    value = value.get_structure()
                structure_dict[key] = value
                
        return structure_dict

    @classmethod
    def from_structure(cls, structure):
        new_obj = cls.__new__()
        new_obj.__init__(**structure)
        return new_obj

    def get_json(self) -> str:
        return json.dumps(self.get_structure())

    @classmethod
    def from_json(cls, json_string: str):
        structure = json.loads(json_string)
        new_obj = cls.from_structure(structure)
        return new_obj

    def flatten(self):
        """
            usage
            -----
                makes the given command flat: appends all member object
                attributes to this object.
        """
        for value in self.__dict__.values():
            if issubclass(value, object):
                self.__dict__.update(value.__dict__)


# eventually this might actually inherit from command_primative
class command_set:
    """
        usage
        -----
            this is used to create a fixed set of commands each of which can be 
            updated continuously throught the code. This allows for
            multi-command 'states' to be constructed.

            TL;DR: this is a command state
    """
    def __init__(self, *command_list: command_primative,
                 name=None,
                 raise_=True):

        if name is None and raise_:
            raise ValueError(
                "please give the command set a name with kwarg: \
                `name='namestr'`"
            )

        self.raise_ = raise_
        self._command_set_dict = {}
        for command in command_list:
            self._command_set_dict[command.name] = command

    def __getitem__(self, command_name) -> command_primative:
        return self._command_set_dict[command_name]

    def __setitem__(self, command_name: str, new_command: command_primative,
                    raise_=True):
        if (new_command.name == command_name):
            self._command_set_dict[command_name] = new_command
        elif raise_:
            raise ValueError("Can only update commands in set")

    def __iter__(self):
        # TODO
        pass

    def __next__(self):
        # TODO
        pass

    def __repr__(self):
        out_str = ""
        for name, value in self._command_set_dict.items():
            # "value" currently returns the repr of the command
            # we ideally want a list of properties... TODO
            out_str += f"\t{name} {value}\n"
        return out_str
