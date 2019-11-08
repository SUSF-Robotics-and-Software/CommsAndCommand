from CommsAndCommand import command


def print_troubling_set_attrs(generic_set):
    print(
        "set excluded_properties",
        generic_set._excluded_properties,
        "---",
        "set structure",
        generic_set.get_structure(),
        "---",
        "set json",
        generic_set.get_json(),
        "---",
        "set repr",
        generic_set,
        sep="\n"
    )


def test_json():
    # proof test json
    generic_command = command.single_value_command(name="generic_command")
    print(generic_command.get_json())
    generic_command.value = "generic_str_value"
    print(generic_command.get_json())


def test_cmd_set():
    generic_command_1 = command.single_value_command(name="generic_command_1")
    generic_command_2 = command.single_value_command(name="generic_command_2")
    generic_command_3 = command.single_value_command(name="generic_command_3")
    generic_set = command.command_set(
        generic_command_1,
        generic_command_2,
        generic_command_3,
        name="generic_set"
    )
    print_troubling_set_attrs(generic_set)


def test_cmd_set_continued():
    generic_command_1 = command.single_value_command(name="generic_command_1")
    generic_command_2 = command.single_value_command(name="generic_command_2")
    generic_command_3 = command.single_value_command(name="generic_command_3")
    generic_set = command.command_set(
        generic_command_1,
        generic_command_2,
        generic_command_3,
        name="generic_set"
    )
    print("update test: before")
    print_troubling_set_attrs(generic_set)
    generic_command_1.value = "dumb value"
    print("update test: after setting command_1 value")
    print_troubling_set_attrs(generic_set)


# basic_command_functionality()
test_cmd_set_continued()
