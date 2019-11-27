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


def test_generic_cmds():
    generic_cont = command.continuous_command("generic_cont", [0, 1])
    print("current structure:", generic_cont.get_structure())
    try:
        generic_cont.name = "hello world"
    except ValueError as v:
        print(f"got error: {v}")
    print("current structure:", generic_cont.get_structure())
    new_cont = command.continuous_command("new_cont", [0, 1])
    print("current structure:", new_cont.get_structure())


def run_all_tests():
    globs = globals()
    test_fns = {}
    for name, item in globs.items():
        if "test_" in name:
            test_fns[name] = item
    for name, fn in test_fns.items():
        print(f"\n\n----- Test: {name} -----\n")
        fn()


# basic_command_functionality()
# test_cmd_set_continued()
# test_generic_cmds()
# test_cmd_set()
run_all_tests()
