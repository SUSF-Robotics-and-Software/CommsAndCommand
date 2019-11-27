import json


# all commands inherit from this, can be used to generate jsons
#   usage:
#   create subclass from this, overwrite the __init__ function
#   with all of the variables that the command has.

_template_cmdset = "{}\n"
_template_cmd = "\t| {}\n"
_template_cmdattr = "\t\t| {} = {}\n"


class command_primitive:
    """
        usage
        -----
            Do not use
            use this as a base class. Instances can then be used to hold
            command information, including other classes
    """
    name: str = ""
    _excluded_properties: set = set()

    def __init__(self):
        raise NotImplementedError(
            "create a subclass of this, overwrite __init__"
        )

    def __new__(cls, *args, **kwargs):
        """
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
        inst._excluded_properties = set(dir(cls))
        return inst

    def get_non_excluded_attrs(self) -> dict:
        """
            iterates over the instance's __dict__ (contains all attributes)
            if it's not excluded, it gets returned in a dict resembling
            a trimmed __dict__
        """
        # but Richard, why not just assume that people use public and private
        # properly?
        # good question...
        # does this even work?
        non_excluded_dict = {}
        for key, value in self.__dict__.items():
            if key not in self._excluded_properties:
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
        structure_dict = {"name": self.name}
        for key, value in self.__dict__.items():
            if key not in self._excluded_properties:
                # type_of_value = type(value)
                # result = issubclass(type_of_value, command_primitive)
                if issubclass(type(value), command_primitive):
                    value = value.get_structure()
                structure_dict[key] = value
                
        return structure_dict

    @classmethod
    def from_structure(cls, structure) -> object:
        new_obj = cls.__new__(cls)
        new_obj.__init__(**structure)
        return new_obj

    def get_json(self) -> str:
        return json.dumps(self.get_structure())

    @classmethod
    def from_json(cls, json_string: str) -> object:
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


class command_set(command_primitive):
    """
        usage
        -----
            this is used to create a fixed set of commands each of which can be 
            updated continuously throught the code. This allows for
            multi-command 'states' to be constructed.

            TL;DR: this is a command state
    """
    raise_ = True
    _command_names_in_set = []

    def __init__(self, *command_in_set: command_primitive,
                 name=None,
                 raise_=True):

        if name is None and raise_:
            raise ValueError(
                "please give the command set a name with kwarg: \
                `name='namestr'`"
            )
        
        self.name = name
        self.raise_ = raise_
        for command in command_in_set:
            if issubclass(type(command), command_primitive):
                self._command_names_in_set.append(command.name)
                self.__dict__[command.name] = command
            elif raise_:
                raise ValueError("commands included in a set must \
                                  be a subclass of command primative")

    def __getitem__(self, command_name) -> command_primitive:
        if command_name in self._command_names_in_set:
            return self.__dict__[command_name]
        elif self.raise_:
            raise ValueError("Can only get commands from a set")

    def __setitem__(self, command_name: str, new_command: command_primitive,
                    raise_=True):
        if (new_command.name == command_name and
                command_name in self._command_names_in_set):
            self.__dict__[command_name] = new_command
        elif raise_:
            raise ValueError("Can only update commands in set")

    def __iter__(self):
        # TODO - this function
        pass

    def __next__(self):
        # os.walk's really odd 'dir, subdirs, files' thing might
        # go really well here. Definately a generator thing.
        # I've seen the source, but it's pretty high IQ
        # TODO - this function
        pass

    def __str__(self):
        """
            produces a representation of the command set.
        """
        out_str = _template_cmdset.format(self.name)
        for cmd_name, cmd_obj in self.__dict__.items():
            # for -> if not nice
            if cmd_name in self._command_names_in_set:
                # adds command name to output
                out_str += _template_cmd.format(cmd_name)
                # gets attr dict
                attr_dict = cmd_obj.get_non_excluded_attrs()
                for attr_name, attr_val in attr_dict.items():
                    # adds command attributes to output
                    if attr_name == "name":
                        continue
                    out_str += _template_cmdattr.format(
                        attr_name, attr_val
                    )
        return out_str
