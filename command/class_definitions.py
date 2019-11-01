import json


# all commands inherit from this, can be used to generate jsons
#   usage:
#   create primat
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
        raise NotImplementedError("Do not use the command primative")

    def __new__(cls, *args, **kwargs):
        """
        On creation of an instance of the class, (or subclasses) the methods
        of _this_ class are added to an exclusion list. This exclusion list
        is part of every subclass, but will stop `get_structure` from
        including attributes of the instance that are
        """
        inst = super().__new__(cls)
        inst.excluded_properties = set(cls.__dict__.keys())
        inst.excluded_properties.add('excluded_properties')
        return inst

    def get_structure(self) -> dict:
        structure_dict = {}
        for key, value in self.__dict__.items():
            if key not in self.excluded_properties:
                structure_dict[key] = value
        return structure_dict

    @classmethod
    def from_structure(cls, structure):
        new_obj = cls()
        cls.__dict__.update(structure)

    def get_json(self) -> str:
        return json.dumps(self.get_json())

    @classmethod
    def from_json(cls, json_string: str):
        structure = json.loads()
        new_obj = cls()

    def flatify(self):
        """
        makes the given command flat: appends all member object
        attributes to this object.
        """
        for name, value in self.__dict__.items():
            if issubclass(value, object):
                self.__dict__.update(value.__dict__)


class command_set:
    def __init__(self, *command_list: command_primative, raise_=True):
        self._command_set_dict = {}
        self.raise_ = raise_
        for command in command_list:
            self._command_set_dict[command.name] = command

    def __getitem__(self, command_name) -> command_primative:
        return self._command_set_dict[command_name]

    def __setitem__(self, command_name: str, new_command: command_primative):
        if (new_command.name == command_name):
            self._command_set_dict[command_name] = new_command
        elif raise_:
            raise ValueError("Can only update commands in set")
