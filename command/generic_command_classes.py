from .abstract_class_definitions import command_primitive


class single_value_command(command_primitive):
    def __init__(self, name, value=None):
        self.name = name
        self.value = value


class checked_command(command_primitive):
    acceptable_values = None
    _attrfn = command_primitive.__setattr__

    def __init__(self, name, acceptable_values):
        self.name = name
        self.acceptable_values = acceptable_values
        self._attrfn = self._instance_setattr

    def __setattr__(self, attrname, value):
        self._attrfn(attrname, value)

    def _instance_setattr(self, attrname, value):
        if (attrname not in self._excluded_properties):
            if self.check_function(attrname, value):
                self.__dict__[attrname] =  value
            else:
                pass  # TODO - probably want some debug
        else:
            raise ValueError(f"Cannot change {attrname} after init")


    def check_function(self, attrname, value):
        raise NotImplementedError


class continuous_command(checked_command):

    def check_function(self, attrname, value):
        if (self.acceptable_values[0] <= value <= self.acceptable_values[-1]):
            return True
        else:
            return False


class discrete_command(checked_command):

    def __init__(self, name, acceptable_values, value=None):
        super().__init__(name, acceptable_values)
        for lim in acceptable_values:
            if self._raise and type(lim) is not int:
                raise TypeError("Limits must be ints for discrete_commands")
        self.limits = limits

    def check_function(self, attrname, value):
        if (value in list(range(
                self.acceptable_values[0],
                self.acceptable_values[-1] + 1))):
            return True
        else:
            return False


class enum_command(checked_command):

    def check_function(self, attrname, value):
        if (value in acceptable_values):
            return True
        else:
            return False
