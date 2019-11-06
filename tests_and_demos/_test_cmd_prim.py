from CommsAndCommand.command import command_primitive


class test_cmd(command_primitive):
    def __init__(self):
        self.name = test_cmd
        self.list_of_floats: [float]
