import inspect
from types import FunctionType, LambdaType, MethodType, CodeType
import builtins
from packer.packer import pack, unpack, unpack_func


class JsonSerializer:
    def __init__(self):
        self.pos = 0
        self.nums = [str(i) for i in range(10)]

    def dumps(self, obj):
        return self.to_str(pack(obj))

    def dump(self, obj, fp):
        with open(fp, 'w+') as f:
            f.write(self.dumps(obj))

    def loads(self, s):
        self.pos = 0
        return unpack(self.from_str(s))

    def load(self, fp):
        with open(fp, 'r') as f:
            return self.loads(f.read())

    def to_str(self, obj, name=''):
        if isinstance(obj, (int, float, str, bool, type(None))):
            return self.to_str_primitive(obj, name)
        if isinstance(obj, (MethodType, FunctionType, LambdaType)):
            return self.to_str_func(obj, name)
        if isinstance(obj, (list, tuple, set)):
            return self.to_str_collection(obj, name)
        if isinstance(obj, dict):
            return self.to_str_dict(obj, name)
        return self.to_str_class_obj(obj, name)

    def to_str_primitive(self, obj, name):
        res = ''
        if  name != '':
            res += f'"{name}": '
        
        if obj is None:
            res += 'null'
        elif isinstance(obj, bool):
            res += 'true' if obj else 'false'
        elif isinstance(obj, (int, float)):
            res += str(obj)
        elif isinstance(obj, str):
            res += f'"{obj}"'
        return res

    def to_str_func(self, obj, name):
        res = ''
        if len(name):
            res += f'"{name}": '
        res += '{' + f'"__func__": "{obj.__name__}", '
        f_globals = {}

        for k in obj.__code__.__dir__():
            if k.startswith('co_'):
                v = getattr(obj.__code__, k)
                
                if k == 'co_names':
                    for glob_k in obj.__code__.co_names:
                        if glob_k in obj.__globals__.keys():
                            f_globals[glob_k] = self.to_str(obj.__globals__.__getitem__(glob_k))
                if isinstance(v, bytes):
                    v = list(v)
                if inspect.iscode(v):
                    v = self.to_str_func(FunctionType(obj, {}), '')
                res += self.to_str(v, k) + ', '
        res += f'"__globals__": {f_globals}'
        res += '}'
        return res

    def to_str_collection(self, obj, name):
        res = ''
        if len(name):
            res += f'"{name}": '
        res += '[' + f'"__{type(obj).__name__}__", '

        for x in obj:
            res += self.to_str(x) + ', '

        if len(res) > 2 and res[-2] == ',':
            res = res[:-2]
        res += ']'
        return res

    def to_str_dict(self, obj, name):
        res = ''
        if len(name):
            res += f'"{name}": '
        res += '{'

        for k, v in obj.items():
            res += self.to_str(v, self.to_str(str(k))) + ', '
        
        if len(res) > 2 and res[-2] == ',':
            res = res[:-2]
            self.pos -= 2
        res += '}'
        self.pos += 2
        return res

    def to_str_class_obj(self, obj, name):
        res = ''
        if len(name):
            res += f'"{name}": '
        res += '{' + f'"__class__": ' + f'"{type(obj).__name__}", '

        for k, v in inspect.getmembers(obj):
            if not '__'in k:
                res += self.to_str(v, k) + ', '
        
        if len(res) > 2 and res[-2] == ',':
            res = res[:-2]
        res += '}'
        return res

    def from_str(self, s):
        if self.pos >= len(s):
            return
        if s[self.pos] in self.nums:
            return self.from_str_num(s)
        if s[self.pos] == 'n':
            return self.from_str_null(s)
        if s[self.pos] == 't':
            return self.from_str_true(s)
        if s[self.pos] == 'f':
            return self.from_str_false(s)
        if s[self.pos:self.pos+12] == '{"__class__"':
            return self.from_str_class_obj(s)
        if s[self.pos:self.pos+11] == '{"__func__"':
            return self.from_str_func(s)
        if s[self.pos] == '"':
            return self.from_str_str(s)
        if s[self.pos] == '[':
            return self.from_str_collection(s)
        if s[self.pos] == '{':
            return self.from_str_dict(s)

    def from_str_str(self, s):
        res = ""
        self.pos += 1

        if s[self.pos] == '"':
            self.pos += 1

        while self.pos < len(s) and s[self.pos] not in ('"', "'"):
            res += s[self.pos]
            self.pos += 1
        
        self.pos += 1
        return res

    def from_str_num(self, s):
        s_pos = self.pos
        while self.pos < len(s) and (s[self.pos] in self.nums or s[self.pos] == '.'):
            self.pos += 1
        num = s[s_pos:self.pos]

        return float(num) if '.' in str(num) else int(num)
    
    def from_str_null(self, s):
        self.pos += 4
        return None
    
    def from_str_true(self, s):
        self.pos += 4
        return True
    
    def from_str_false(self, s):
        self.pos += 5
        return False

    def from_str_func(self, s):
        obj = self.from_str_dict(s)
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
        f = FunctionType(code, obj['__globals__'], obj['co_name'])
        return f

    def from_str_collection(self, s):
        res = []
        self.pos += 1
        s_type = self.from_str_str(s)

        while self.pos < len(s) and s[self.pos] not in (']', '}', ')'):
            if s[self.pos] == ' ' or s[self.pos] == ',':
                self.pos += 1
                continue

            v = self.from_str(s)
            res.append(v)

            if self.pos < len(s) and s[self.pos] in (']', '}', ')'):
                break
            self.pos += 1

        if s_type == '__tuple__':
            res = tuple(res)
        elif s_type == '__set__':
            res = set(res)
        self.pos += 1
        return res

    def from_str_dict(self, s):
        res = {}
        self.pos += 1

        while self.pos < len(s) and s[self.pos] != '}':
            while s[self.pos] in (' ', ','):
                self.pos += 1
                continue
            
            k = self.from_str_str(s)
            self.pos = s.find(':', self.pos)+2
            #print('key:', k)
            v = self.from_str(s)
            #print('v:', v, '\n')
            res[k] = v
        self.pos += 1
        return res

    def from_str_class_obj(self, s):
        obj = self.from_str_dict(s)
        res = type(obj['__class__'], (), {})()

        for k, v in obj.items():
            if '__' in k:
                continue
            setattr(res, k, v)
        self.pos += 1
        return res