from serializer.parsers.toml.toml import TomlParser
from serializer.parsers.json.json import JsonParser
from serializer.parsers.yaml.yaml import YamlParser
from serializer.parsers.pickle.pickle import PickleParser


class SerializerFactory:
    def __init__(self):
        self.serializers = {
            'json': JsonParser(),
            'toml': TomlParser(),
            'yaml': YamlParser(),
            'pickle': PickleParser()
        }

    def create_serializer(self, serializer_type):
        try:
            return self.serializers[serializer_type]
        except Exception as ex:
            print("Unknown type {}".format(ex))