"""Work in progress

Objectives:

    - Write a pytest plugin that will collect "test*.yaml" files and executed the yaml-formatted content as custom tests

"""
from py._path.local import LocalPath
import typing

from _pytest import nodes
import pytest
import yaml

from kapla.test.specs import YamlFileSpec, YamlItemSpec


class YamlItem(pytest.Item):
    def __init__(
        self,
        parent: nodes.Node,
        spec: YamlItemSpec,
    ) -> None:
        """YamlItem should never be created manually.

        The YamlFile.collect() method is responsible for iterating over a
        YAML test file and creating YamlItem instances.
        """
        super().__init__(spec.name, parent=parent)
        self.spec = spec

    def runtest(self) -> None:
        """A dummy function to run tests.

        It is possible to access to `self.spec` attribute within this function.
        """
        assert True


class YamlFile(pytest.File):
    def collect(self) -> typing.Iterable[typing.Union[pytest.Item, pytest.Collector]]:
        """Yield test items from given YAML file.

        Pytest is designed so that once test files are discovered, tests are discovered within test files.
        Each discovered file is represented as an instance of a child class of `pytest.File` abstract class.

        Tests are discovered within file using the `pytest.File.collect()` method.

        In this method, we parse the content of a YAML file and expect it to match a specific schema.
        Once content is validated, we iterate over tests present in file and yield them as instances
        """
        raw = yaml.safe_load(self.fspath.open())
        spec = YamlFileSpec.parse_obj(raw)
        for test in spec.tests:
            # Let's build variables and groups using both global values and test values
            # If variables are specified both globally and locally, local value (test value) is used
            variables = {**spec.variables, **test.variables}
            groups = list(set([*spec.groups, *test.groups]))
            spec = YamlItemSpec.construct(
                name=test.name,
                description=test.description,
                variables=variables,
                groups=groups,
            )
            yield YamlItem.from_parent(self, spec=spec)


def pytest_collect_file(parent: nodes.Node, path: LocalPath) -> typing.Any:
    """Magic function used by pytest to collect files."""
    if path.ext.lower() in (".yaml", ".yml") and path.basename.startswith("test"):
        return YamlFile.from_parent(parent, fspath=path)
