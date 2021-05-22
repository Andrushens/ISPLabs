import toml
from packer.packer import pack, unpack


class TomlSerializer:
    def dump(self, obj, fp):
        return toml.dump(pack(obj), open(fp, 'w'))

    def dumps(self, obj):
        return toml.dumps(pack(obj))

    def load(self, fp):
        return unpack(toml.load(open(fp, 'r')))

    def loads(self, s):
        return unpack(toml.loads(s))