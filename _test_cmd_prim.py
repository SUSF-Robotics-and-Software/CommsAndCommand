from command import command_primative


class test_cmd(command_primative):
    def __init__(self):
        self.name = test_cmd
        self.list_of_floats: [float]
