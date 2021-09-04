from setuptools import setup


setup(
    name="lab2_packer",
    packages=["serializer.parsers.toml", "serializer.parsers.yaml",
        "serializer.parsers.pickle", "serializer.parsers.json",
        "serializer.parsers", "serializer_factory"],
    scripts=["convert.py"]
)