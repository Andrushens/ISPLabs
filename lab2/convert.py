from serializer_factory import SerializerFactory
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--fp', dest='file_path', help='Input file path')
parser.add_argument('--nf', dest='new_format', help='New format of file')
args = parser.parse_args()

try:
    new_fp, old_f = args.file_path.split('.')
    new_fp += '.' + args.new_format

    if old_f == args.new_format:
        raise ValueError('Same in/out formats')

    f = SerializerFactory()
    s = f.create_serializer(old_f)
    obj = s.load(args.file_path)
    s = f.create_serializer(args.new_format)
    s.dump(obj, new_fp)
except Exception as ex:
    print(ex)