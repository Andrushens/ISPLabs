from serializer.serializer import Serializer
from serializer.parsers.toml.toml_serialization import serialize_toml, deserialize_toml


class TomlParser:

    @staticmethod
    def dumps(obj) -> str:
        obj = Serializer.serialize(obj)
        return f"tuple = {serialize_toml(obj)}"

    @staticmethod
    def dump(obj, fp):
        with open(fp, 'w+') as f:
            f.write(TomlParser.dumps(obj))

    @staticmethod
    def loads(obj: str):
        obj = obj.split('=', 1)[1]
        obj = deserialize_toml(obj.replace("\\n", "\n").strip())
        return Serializer.deserialize(obj)

    @staticmethod
    def load(fp):
        with open(fp, 'r') as f:
            return TomlParser.loads(f.read())