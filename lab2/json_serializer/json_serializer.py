import json
from packer.packer import pack, unpack


class JsonSerializer:
    def dump(self, obj, fp):
        return json.dump(pack(obj), open(fp, 'w'))

    def dumps(self, obj):
        return json.dumps(pack(obj))

    def load(self, fp):
        return unpack(json.load(open(fp, 'r')))

    def loads(self, s):
        return unpack(json.loads(s))