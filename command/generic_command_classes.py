from .abstract_class_definitions import command_primitive


class checked_command(command_primitive):
    def __init__(self, name):
        self.name = name

    def __setattr__(self, attrname, value):
        if (attrname in self.get_non_excluded_attrs()):
            if self.check_function(attrname, value):
                super().__setattr__(attrname, value)
            else:
                pass  # TODO - probably want some debug
        else:
            raise ValueError(f"Cannot change {attrname} after init")

    def check_function(self, attrname, value):
        raise NotImplementedError


class single_value_command(checked_command):
    def __init__(self, name, value=None):
        self.name = name
        self.value = value


class continuous_command(checked_command):
    limits = None

    def __init__(self, name, limits, value=None):
        super().__init__(name)
        self.limits = limits

    def check_function(self, attrname, value):
        if (self.limits[0] <= value <= self.limits[-1]):
            return True
        else:
            return False


class discrete_command(checked_command):
    limits = None

    def __init__(self, name, limits, value=None):
        super().__init__(name)
        for lim in limits:
            assert (type(lim) == int) \
                "cannot use non ints in discrete commands"
        self.limits = limits

    def check_function(self, attrname, value):
        if (value in list(range(self.limits[0], self.limits[-1] + 1))):
            return True
        else:
            return False


class enum_command(buffer_command):
    acceptable_values = None

    def __init__(self, name, acceptable_values, value=None):
        super().__init__(name)
        self.acceptable_values = acceptable_values

    def check_function(self, attrname, value):
        if (value in acceptable_values):
            return True
        else:
            return False
