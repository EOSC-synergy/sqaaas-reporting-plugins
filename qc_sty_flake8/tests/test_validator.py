import pathlib
from types import SimpleNamespace

import pytest
from report2sqaaas_plugins_flake8.main import Flake8Validator


@pytest.fixture
def flake8_stdout(request):
    file = pathlib.Path(request.node.fspath.strpath)
    stdout = file.with_name("flake8.out")
    # stdout = file.with_name('empty.out')
    with stdout.open() as fp:
        return fp.read()


@pytest.fixture
def validator_opts(flake8_stdout):
    class_args = {"validator": "flake8", "stdout": flake8_stdout}
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return Flake8Validator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert Flake8Validator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert "valid" in list(result)
    assert "subcriteria" in list(result)
    assert type(result["subcriteria"]) is list
