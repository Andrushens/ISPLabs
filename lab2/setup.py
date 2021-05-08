from setuptools import setup


setup(
    name="lab2_packer",
    packages=["json_serializer", "toml_serializer", "yaml_serializer",
                "pickle_serializer", "packer", "serializer_factory"],
    scripts=["convert.py"]
)