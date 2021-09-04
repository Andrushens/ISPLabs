from serializer.serializer import Serializer
from serializer.parsers.json.json_serialization import serialize_json, deserialize_json


class JsonParser:

    @staticmethod
    def dumps(obj) -> str:
        obj = Serializer.serialize(obj)
        return serialize_json(obj).replace("\n", "\\n")

    @staticmethod
    def dump(obj, fp):
        with open(fp, 'w+') as f:
            f.write(JsonParser.dumps(obj))

    @staticmethod
    def loads(obj: str):
        obj = deserialize_json(obj.replace("\\n", "\n"))
        return Serializer.deserialize(obj)

    @staticmethod
    def load(fp):
        with open(fp, 'r') as f:
            return JsonParser.loads(f.read())
