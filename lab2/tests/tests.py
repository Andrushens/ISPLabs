import unittest
from serializer_factory.serializer_factory import SerializerFactory
import test_data


class SerializeTester(unittest.TestCase):
#---------JSON---------
    def test_json_primitive(self):
        self.s = SerializerFactory().create_serializer('json')
        old_obj = test_data.int_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_collection(self):
        self.s = SerializerFactory().create_serializer('json')
        old_obj = test_data.list_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_dict(self):
        self.s = SerializerFactory().create_serializer('json')
        old_obj = test_data.dict_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj[None], new_obj['None'])

    def test_json_lambda(self):
        self.s = SerializerFactory().create_serializer('json')
        old_obj = test_data.simple_lambda
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(5), new_obj(5))

    def test_json_simple_func(self):
        self.s = SerializerFactory().create_serializer('json')
        old_obj = test_data.simple_func
        self.s.dump(old_obj, 'test.json')
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(4), new_obj(4))

    def test_json_cmplx_func(self):
        self.s = SerializerFactory().create_serializer('json')
        old_obj = test_data.cmplx_func
        old_obj_2 = test_data.simple_lambda
        new_obj = self.s.loads(self.s.dumps(old_obj))
        new_obj_2 = self.s.loads(self.s.dumps(old_obj_2))
        self.assertEqual(old_obj(4), new_obj(4))
        self.assertEqual(old_obj_2(4), new_obj_2(4))

    def test_json_simple_class_obj(self):
        self.s = SerializerFactory().create_serializer('json')
        old_obj = test_data.SimpleClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.suicide(), new_obj.suicide(0))
        self.assertEqual(old_obj.name, new_obj.name)

    def test_json_cmplx_class_obj(self):
        self.s = SerializerFactory().create_serializer('json')
        old_obj = test_data.ComplexClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.teammate.name, new_obj.teammate.name)
        self.assertEqual(old_obj.kill(), new_obj.kill(self))
        self.assertEqual(old_obj.const, new_obj.const)
        self.assertEqual(old_obj.teammate.suicide(), new_obj.teammate.suicide(self))
        self.assertEqual(old_obj.tuple[1](), new_obj.tuple[1](self))
        self.assertEqual(old_obj.tuple[0].name, new_obj.tuple[0].name)

#---------YAML---------
    def test_yaml_primitive(self):
        self.s = SerializerFactory().create_serializer('yaml')
        old_obj = test_data.int_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_collection(self):
        self.s = SerializerFactory().create_serializer('yaml')
        old_obj = test_data.list_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_lambda(self):
        self.s = SerializerFactory().create_serializer('yaml')
        old_obj = test_data.simple_lambda
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(5), new_obj(5))

    def test_yaml_simple_func(self):
        self.s = SerializerFactory().create_serializer('yaml')
        old_obj = test_data.simple_func
        self.s.dump(old_obj, 'test.yaml')
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(4), new_obj(4))

    def test_yaml_cmplx_func(self):
        self.s = SerializerFactory().create_serializer('yaml')
        old_obj = test_data.cmplx_func
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(4), new_obj(4))

    def test_yaml_simple_class_obj(self):
        self.s = SerializerFactory().create_serializer('yaml')
        old_obj = test_data.SimpleClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.suicide(), new_obj.suicide(0))
        self.assertEqual(old_obj.name, new_obj.name)

    def test_yaml_dict(self):
        self.s = SerializerFactory().create_serializer('yaml')
        old_obj = test_data.dict_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_cmplx_class_obj(self):
        self.s = SerializerFactory().create_serializer('yaml')
        old_obj = test_data.ComplexClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.teammate.name, new_obj.teammate.name)
        self.assertEqual(old_obj.kill(), new_obj.kill(self))
        self.assertEqual(old_obj.const, new_obj.const)
        self.assertEqual(old_obj.teammate.suicide(), new_obj.teammate.suicide(self))
        self.assertEqual(old_obj.tuple[1](), new_obj.tuple[1](self))
        self.assertEqual(old_obj.tuple[0].name, new_obj.tuple[0].name)
    
#---------TOML---------
    def test_toml_lambda(self):
        self.s = SerializerFactory().create_serializer('toml')
        old_obj = test_data.simple_lambda
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(5), new_obj(5))

    def test_toml_simple_func(self):
        self.s = SerializerFactory().create_serializer('toml')
        old_obj = test_data.simple_func
        self.s.dump(old_obj, 'test.toml')
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(4), new_obj(4))

    def test_toml_simple_class_obj(self):
        self.s = SerializerFactory().create_serializer('toml')
        old_obj = test_data.SimpleClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.suicide(), new_obj.suicide(0))
        self.assertEqual(old_obj.name, new_obj.name)

#---------PICKLE---------
    def test_pickle_primitive(self):
        self.s = SerializerFactory().create_serializer('pickle')
        old_obj = test_data.int_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_pickle_collection(self):
        self.s = SerializerFactory().create_serializer('pickle')
        old_obj = test_data.list_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)
        
    def test_pickle_dict(self):
        self.s = SerializerFactory().create_serializer('pickle')
        old_obj = test_data.dict_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_pickle_lambda(self):
        self.s = SerializerFactory().create_serializer('pickle')
        old_obj = test_data.simple_lambda
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(5), new_obj(5))

    def test_pickle_simple_func(self):
        self.s = SerializerFactory().create_serializer('pickle')
        old_obj = test_data.simple_func
        self.s.dump(old_obj, 'test.pickle')
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(4), new_obj(4))

    def test_pickle_cmplx_func(self):
        self.s = SerializerFactory().create_serializer('pickle')
        old_obj = test_data.cmplx_func
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(4), new_obj(4))

    def test_pickle_simple_class_obj(self):
        self.s = SerializerFactory().create_serializer('pickle')
        old_obj = test_data.SimpleClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.suicide(), new_obj.suicide(0))
        self.assertEqual(old_obj.name, new_obj.name)

    def test_pickle_cmplx_class_obj(self):
        self.s = SerializerFactory().create_serializer('pickle')
        old_obj = test_data.ComplexClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.teammate.name, new_obj.teammate.name)
        self.assertEqual(old_obj.kill(), new_obj.kill(self))
        self.assertEqual(old_obj.const, new_obj.const)
        self.assertEqual(old_obj.teammate.suicide(), new_obj.teammate.suicide(self))
        self.assertEqual(old_obj.tuple[1](), new_obj.tuple[1](self))
        self.assertEqual(old_obj.tuple[0].name, new_obj.tuple[0].name)