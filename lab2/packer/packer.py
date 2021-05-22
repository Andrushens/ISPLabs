import inspect
from types import MethodType, FunctionType, LambdaType, CodeType
import builtins


def pack(obj):
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    if isinstance(obj, (MethodType, FunctionType, LambdaType)):
        return pack_func(obj)
    if isinstance(obj, (list, set, tuple, dict)):
        return pack_collection(obj)
    return pack_class_obj(obj)

def unpack(obj):
    if isinstance(obj, dict):
        if '__func__' in obj.keys():
            return unpack_func(obj)
        if '__class__' in obj.keys():
            return unpack_class_obj(obj)
        return unpack_collection(obj)
    if isinstance(obj, (list, set, tuple)):
        return unpack_collection(obj)
    return obj

def pack_collection(obj):
    res = {}
    if isinstance(obj, (list, set, tuple)):
        res = []
        [res.append(pack(v)) for v in obj]
    else:
        for k, v in obj.items():
            res[k] = pack(v)
    return res

def unpack_collection(obj):
    res = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            res[k] = unpack(v)
        return res
    else:
        res = [unpack(v) for v in obj]
    return res
    
def pack_func(obj):
    res = {'__func__': obj.__name__}
    res['__globals__'] = {}
    for k in obj.__code__.__dir__():
        if k.startswith('co_'):
            v = getattr(obj.__code__, k)
            if isinstance(v, bytes):
                v = list(v)
            if inspect.iscode(v):
                v = pack_func(FunctionType(obj, {}))
            res[k] = pack(v)

    for k in res['co_names']:
        if k in obj.__globals__.keys():
            res['__globals__'][k] = obj.__globals__.__getitem__(k)
    return res

def unpack_func(obj):
    obj['__globals__']['__builtins__'] = builtins
    code = CodeType(obj['co_argcount'],
                        obj['co_posonlyargcount'],
                        obj['co_kwonlyargcount'],
                        obj['co_nlocals'],
                        obj['co_stacksize'],
                        obj['co_flags'],
                        bytes(obj['co_code']),
                        tuple(obj['co_consts']),
                        tuple(obj['co_names']),
                        tuple(obj['co_varnames']),
                        obj['co_filename'],
                        obj['co_name'],
                        obj['co_firstlineno'],
                        bytes(obj['co_lnotab']),
                        tuple(obj['co_freevars']),
                        tuple(obj['co_cellvars']))
    return FunctionType(code, obj['__globals__'], obj['co_name'])

def pack_class_obj(obj):
    res = {}
    res['__class__'] = type(obj).__name__

    for k, v in inspect.getmembers(obj):
        if not '__'in k:
            res[k] = pack(v)
    return res

def unpack_class_obj(obj):
    res = type(obj['__class__'], (), {})()
    for k, v in obj.items():
        if '__' in k:
            continue
        setattr(res, k, unpack(v))
    return res