from serializer_factory import SerializerFactory
import unittest
import test_data


class SerializeTester(unittest.TestCase):
#---------JSON---------
    def test_json_dict(self):
        self.s = SerializerFactory().create_serializer('json')
        old_obj = test_data.test_dict
        self.s.dump(old_obj, 'test.json')
        new_obj = self.s.load('test.json')
        self.assertEqual(old_obj, new_obj)

    def test_json_list(self):
        self.s = SerializerFactory().create_serializer('json')
        old_obj = test_data.test_list
        self.s.dump(old_obj, 'test.json')
        new_obj = self.s.load('test.json')
        self.assertEqual(old_obj, new_obj)

    def test_json_lambda(self):
        self.s = SerializerFactory().create_serializer('json')
        old_obj = test_data.test_lambda
        self.s.dump(old_obj, 'test.json')
        new_obj = self.s.load('test.json')
        self.assertEqual(old_obj(test_data.test_number), new_obj(test_data.test_number))
        
    def test_json_recursion(self):
        self.s = SerializerFactory().create_serializer('json')
        old_obj = test_data.test_recursion
        self.s.dump(old_obj, 'test.json')
        new_obj = self.s.load('test.json')
        self.assertEqual(old_obj(test_data.test_number), new_obj(test_data.test_number))

#---------YAML---------
    def test_yaml_list(self):
        self.s = SerializerFactory().create_serializer('yaml')
        old_obj = test_data.test_list
        self.s.dump(old_obj, 'test.yaml')
        new_obj = self.s.load('test.yaml')
        self.assertEqual(old_obj, new_obj)

    def test_yaml_lambda(self):
        self.s = SerializerFactory().create_serializer('yaml')
        old_obj = test_data.test_lambda
        self.s.dump(old_obj, 'test.yaml')
        new_obj = self.s.load('test.yaml')
        self.assertEqual(old_obj(test_data.test_number), new_obj(test_data.test_number))
        
    def test_yaml_recursion(self):
        self.s = SerializerFactory().create_serializer('yaml')
        old_obj = test_data.test_recursion
        self.s.dump(old_obj, 'test.yaml')
        new_obj = self.s.load('test.yaml')
        self.assertEqual(old_obj(test_data.test_number), new_obj(test_data.test_number))

#---------TOML---------
    def test_toml_list(self):
        self.s = SerializerFactory().create_serializer('toml')
        old_obj = test_data.test_list
        self.s.dump(old_obj, 'test.toml')
        new_obj = self.s.load('test.toml')
        self.assertEqual(old_obj, new_obj)

    def test_toml_lambda(self):
        self.s = SerializerFactory().create_serializer('toml')
        old_obj = test_data.test_lambda
        self.s.dump(old_obj, 'test.toml')
        new_obj = self.s.load('test.toml')
        self.assertEqual(old_obj(test_data.test_number), new_obj(test_data.test_number))
        
    def test_toml_recursion(self):
        self.s = SerializerFactory().create_serializer('toml')
        old_obj = test_data.test_recursion
        self.s.dump(old_obj, 'test.toml')
        new_obj = self.s.load('test.toml')
        self.assertEqual(old_obj(test_data.test_number), new_obj(test_data.test_number))

#---------PICKLE---------
    def test_pickle_list(self):
        self.s = SerializerFactory().create_serializer('pickle')
        old_obj = test_data.test_list
        self.s.dump(old_obj, 'test.pickle')
        new_obj = self.s.load('test.pickle')
        self.assertEqual(old_obj, new_obj)

    def test_pickle_recursion(self):
        self.s = SerializerFactory().create_serializer('pickle')
        old_obj = test_data.test_recursion
        self.s.dump(old_obj, 'test.pickle')
        new_obj = self.s.load('test.pickle')
        self.assertEqual(old_obj(test_data.test_number), new_obj(test_data.test_number))
