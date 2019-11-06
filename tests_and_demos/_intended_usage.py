"""
    Example usage of command package
    author: Richard A, 2019
"""

from CommsAndCommand import command

"""
    both of these ideally should be done in the module namespace
    to conform to the "if __name__ == "__main__": init()" structure,
    you may return a dict which is then accepted by loop:

    ```
    def init():
        # tasks to init module here
        variables_needed_dict = {
            "variable_1": variable_1
        }
        return variables_needed_dict
    ```

    or, if you're incredibly lazy

    
    ```
    def init():
        # tasks to init module here
        return locals()
    ```
"""

# create the command objects
forward_velocity_command = command.single_value_data('forward_velocity')
curvature_command = command.single_value_data('curvature')

# print(forward_velocity_command.name)

# create a command set containing the basic commands
locomotion_control_commands = command.command_set(
    forward_velocity_command,
    curvature_command,
    name="locomotion_control_commands"
)


def main_loop():
    # typical usage, you'd gather external data from either:
    # 1) controller:
    #   current_controller_values = example_controller.get_controls()
    # 2) the newtork:
    #   network_output = example_network.get_buffer()
    forward_velocity_command.value = 0.75
    curvature_command.value = 0.1


# normally, you'd want a loop to continuously update the variables
# while 1:
#     main_loop()

print("pre loop:", locomotion_control_commands, sep="\n")
main_loop()
print("post loop:", locomotion_control_commands, sep="\n")
