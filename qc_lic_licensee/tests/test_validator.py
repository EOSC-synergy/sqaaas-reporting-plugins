import json
import pathlib
import pytest
from types import SimpleNamespace

from report2sqaaas_plugins_licensee.main import LicenseeValidator


@pytest.fixture
def licensee_stdout(request):
    file = pathlib.Path(request.node.fspath.strpath)
    stdout = file.with_name('licensee.out.json')
    with stdout.open() as fp:
        json_data = json.load(fp)
        return json.dumps(json_data)


@pytest.fixture
def validator_opts(licensee_stdout):
    class_args = {
        'validator': 'licensee',
        'stdout': licensee_stdout
    }
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return LicenseeValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert LicenseeValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert 'valid' in list(result)
