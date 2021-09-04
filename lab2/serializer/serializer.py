import inspect
import re
from types import CodeType, FunctionType
from pydoc import locate

FUNC_ATTRS = [
    '__code__',
    '__name__',
    '__defaults__',
    '__closure__'
]

CODE_OBJECT_ARGS = [
    'co_argcount',
    'co_posonlyargcount',
    'co_kwonlyargcount',
    'co_nlocals',
    'co_stacksize',
    'co_flags',
    'co_code',
    'co_consts',
    'co_names',
    'co_varnames',
    'co_filename',
    'co_name',
    'co_firstlineno',
    'co_lnotab',
    'co_freevars',
    'co_cellvars'
]

class Serializer:
    @staticmethod
    def serialize(obj):
        res = {}
        obj_type = type(obj)
        if obj_type == dict:
            res['type'] = 'dict'
            res['value'] = {}
            for i in obj:
                key = Serializer.serialize(i)
                value = Serializer.serialize(obj[i])
                res['value'][key] = value
            res['value'] = tuple((k, res['value'][k]) for k in res['value'])
        elif obj_type == list:
            res['type'] = 'list'
            res['value'] = tuple([Serializer.serialize(i) for i in obj])
        elif obj_type == tuple:
            res['type'] = 'tuple'
            res['value'] = tuple([Serializer.serialize(i) for i in obj])
        elif obj_type == bytes:
            res['type'] = 'bytes'
            res['value'] = tuple([Serializer.serialize(i) for i in obj])
        elif obj is None:
            res['type'] = 'NoneType'
            res['value'] = None
        elif inspect.isroutine(obj):
            res['type'] = 'function'
            res['value'] = {}
            func_members = inspect.getmembers(obj)
            func_members = [i for i in func_members if i[0] in FUNC_ATTRS]
            for i in func_members:
                key = Serializer.serialize(i[0])
                if i[0] != '__closure__':
                    value = Serializer.serialize(i[1])
                else:
                    value = Serializer.serialize(None)
                res['value'][key] = value
                if i[0] == '__code__':
                    key = Serializer.serialize('__globals__')
                    res['value'][key] = {}
                    names = i[1].__getattribute__('co_names')
                    glob = obj.__getattribute__('__globals__')
                    globals_d = {}
                    for name in names:
                        if name == obj.__name__:
                            globals_d[name] = obj.__name__
                        elif name in glob and not inspect.ismodule(name) and name not in __builtins__:
                            globals_d[name] = glob[name]
                    res['value'][key] = Serializer.serialize(globals_d)
            res['value'] = tuple((k, res['value'][k]) for k in res['value'])
        elif isinstance(obj, (int, float, complex, bool, str)):
            typestr = re.search(r"\'(\w+)\'", str(obj_type)).group(1)
            res['type'] = typestr
            res['value'] = obj
        else:
            res['type'] = 'instance'
            res['value'] = {}
            class_members = inspect.getmembers(obj)
            class_members = [i for i in class_members if not callable(i[1])]
            for i in class_members:
                key = Serializer.serialize(i[0])
                value = Serializer.serialize(i[1])
                res['value'][key] = value
            res['value'] = tuple((k, res['value'][k]) for k in res['value'])
        res = tuple((k, res[k]) for k in res)
        return res

    @staticmethod
    def deserialize(obj):
        d = dict((a, b) for a, b in obj)
        obj_type = d['type']
        res = None
        if obj_type == 'list':
            res = [Serializer.deserialize(i) for i in d['value']]
        elif obj_type == 'tuple':
            res = tuple([Serializer.deserialize(i) for i in d['value']])
        elif obj_type == 'dict':
            res = {}
            for i in d['value']:
                value = Serializer.deserialize(i[1])
                res[Serializer.deserialize(i[0])] = value
        elif obj_type == 'function':
            func = [0] * 4
            code = [0] * 16
            glob = {'__builtins__': __builtins__}
            for i in d['value']:
                key = Serializer.deserialize(i[0])
                if key == '__globals__':
                    global_d = Serializer.deserialize(i[1])
                    for global_key in global_d:
                        glob[global_key] = global_d[global_key]
                elif key == '__code__':
                    value = i[1][1][1]
                    for arg in value:
                        codeArgKey = Serializer.deserialize(arg[0])
                        if codeArgKey != '__doc__':
                            codeArgVal = Serializer.deserialize(arg[1])
                            index = CODE_OBJECT_ARGS.index(codeArgKey)
                            code[index] = codeArgVal
                    code = CodeType(*code)
                else:
                    index = FUNC_ATTRS.index(key)
                    func[index] = (Serializer.deserialize(i[1]))
            func[0] = code
            func.insert(1, glob)
            res = FunctionType(*func)
            if res.__name__ in res.__getattribute__('__globals__'):
                res.__getattribute__('__globals__')[res.__name__] = res
        elif obj_type == 'NoneType':
            res = None
        elif obj_type == 'bytes':
            res = bytes([Serializer.deserialize(i) for i in d['value']])
        else:
            if obj_type == 'bool':
                res = d['value'] == 'True'
            else:
                res = locate(obj_type)(d['value'])
        return res
