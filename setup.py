import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="libbisca",
    version="0.0.1",
    description="Bisca card game library",
    long_description=README,
    long_description_content_type="text/markdown",
    # TODO: url="https://github.com/",
    author="Nuno Miguel Casteloa da Silva",
    author_email="NunoMCSilva@gmail.com",
    # TODO: license="",
    classifiers=[
        # TODO: add classifiers
    ],
    packages=find_packages(exclude=("tests",)),     # TODO: not sure about this...
    # include_package_data=True,
    # TODO: what about tests?
    # install_requires=[],   # TODO: install_requires? check this...
    # TODO: doesn't have entry_points?
)
# TODO: add keywords, platform?
