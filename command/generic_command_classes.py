from .abstract_class_definitions import command_primitive


class single_value_command(command_primitive):
    def __init__(self, name):
        self.name = name
        self.value = None
