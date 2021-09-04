from serializer.parsers.toml import TomlSerializer
from serializer.parsers.json import JsonSerializer
from serializer.parsers.yaml import YamlSerializer
from serializer.parsers.pickle import PickleSerializer


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