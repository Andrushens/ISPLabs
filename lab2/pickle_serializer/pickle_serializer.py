import pickle
from packer.packer import pack, unpack


class PickleSerializer:
    def dump(self, obj, fp):
        return pickle.dump(pack(obj), open(fp, 'wb'))

    def dumps(self, obj):
        return pickle.dumps(pack(obj))

    def load(self, fp):
        return unpack(pickle.load(open(fp, 'rb')))

    def loads(self, s):
        return unpack(pickle.loads(s))