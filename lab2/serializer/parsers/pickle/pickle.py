import pickle


class PickleParser:
    @staticmethod
    def dumps(obj) -> str:
        return pickle.dumps(obj)

    @staticmethod
    def dump(obj, file):
        return pickle.dump(obj, open(file, 'wb'))

    @staticmethod
    def loads(obj: str):
        return pickle.loads(obj)

    @staticmethod
    def load(file):
        return pickle.load(open(file, 'rb'))
