from toml_serializer.toml_serializer import TomlSerializer
from json_serializer.json_serializer import JsonSerializer
from yaml_serializer.yaml_serializer import YamlSerializer
from pickle_serializer.pickle_serializer import PickleSerializer


class SerializerFactory:
    def __init__(self):
        self.serializers = {
            'json': JsonSerializer(),
            'toml': TomlSerializer(),
            'yaml': YamlSerializer(),
            'pickle': PickleSerializer()
        }

    def create_serializer(self, serializer_type):
        try:
            return self.serializers[serializer_type]
        except Exception as ex:
            print("Unknown type {}".format(ex))