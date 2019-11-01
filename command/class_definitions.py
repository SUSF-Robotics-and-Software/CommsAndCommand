import json


# all commands inherit from this, can be used to generate jsons
class command_primative:
    name: str
    excluded_properties: list = [] 

    def __new__(cls):
        inst = super().__new__(cls)
        inst.excluded_properties = cls.__dict__.keys()
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
