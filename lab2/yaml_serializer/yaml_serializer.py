import yaml
from packer.packer import pack, unpack


class YamlSerializer:
    def dump(self, obj, fp):
        return yaml.dump(pack(obj), open(fp, 'w'))

    def dumps(self, obj):
        return yaml.dump(pack(obj))

    def load(self, fp):
        return unpack(yaml.load(open(fp, 'r')))

    def loads(self, s):
        return unpack(yaml.load(s))