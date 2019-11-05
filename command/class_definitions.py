import json


# all commands inherit from this, can be used to generate jsons
class command_primative:
    """
    usage
    -----
        Do not use
        use this as a base class. Instances can then be used to hold
        command information, including other classes
    """
    name: str
    excluded_properties: set

    def __init__(self):
        raise NotImplementedError("create a subclass of this")

    def __new__(cls, *args, **kwargs):
        """
        usage
        -----
            On creation of an instance of the class, (or subclasses) the 
            methods of the class are added to `exclusion_list`. This 
            exclusion list is part of every subclass, and will stop
            `get_structure` from including non-data attributes, which are
            defined by being included in the class definition, and not added
            in the __init__ constructor method. This allows for the hacky
            but quick `self.__dict__.update(locals())` to be used.

        returns
        -------
            new instance of the class
        """
        inst = super().__new__(cls)
        inst.excluded_properties = set(cls.__dict__.keys())
        inst.excluded_properties.add('excluded_properties')
        return inst

    def get_structure(self) -> dict:
        """
        usage
        -----
            returns a structural (__dict__) representation of the command sans
            `excluded_properties`, which should contain all the classes' base
            attributes

        returns
        -------
            dict of all attributes
        """
        structure_dict = {}
        for key, value in self.__dict__.items():
            if key not in self.excluded_properties:
                if issubclass(value, command_primative):
                    value=value.get_structure()
                structure_dict[key] = value
                
        return structure_dict

    @classmethod
    def from_structure(cls, structure) -> cls:
        new_obj = cls()
        new_obj.__dict__.update(structure)
        return new_obj

    def get_json(self) -> str:
        return json.dumps(self.get_structure())

    @classmethod
    def from_json(cls, json_string: str) -> cls:
        structure = json.loads(json_string)
        new_obj = cls().from_structure(structure)
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



class command_set:
    """
    usage
    -----
        this is used to create a fixed set of commands each of which can be 
        updated continuously throught the code. This allows for multi-command
        'states' to be constructed.
        Teal dear: this is a command state
    """
    def __init__(self, *command_list: command_primative, raise_=True):
        self._command_set_dict = {}
        self.raise_ = raise_
        for command in command_list:
            self._command_set_dict[command.name] = command

    def __getitem__(self, command_name) -> command_primative:
        return self._command_set_dict[command_name]

    def __setitem__(self, command_name: str, new_command: command_primative, raise_=True):
        if (new_command.name == command_name):
            self._command_set_dict[command_name] = new_command
        elif raise_:
            raise ValueError("Can only update commands in set")
