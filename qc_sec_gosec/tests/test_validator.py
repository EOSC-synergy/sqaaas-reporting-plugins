import pathlib
import pytest
from types import SimpleNamespace

from report2sqaaas_plugins_gosec.main import GoSecValidator


@pytest.fixture
def gosec_stdout(request):
    file = pathlib.Path(request.node.fspath.strpath)
    stdout = file.with_name('gosec.out')
    with stdout.open() as fp:
        return fp.read()


@pytest.fixture
def validator_opts(gosec_stdout):
    class_args = {
        'validator': 'gosec',
        'stdout': gosec_stdout
    }
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return GoSecValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert GoSecValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert 'valid' in list(result)
    assert 'subcriteria' in list(result)
    assert type(result['subcriteria']) is list
