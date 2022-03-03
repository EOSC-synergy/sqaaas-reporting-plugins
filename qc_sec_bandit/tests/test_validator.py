import pytest
from types import SimpleNamespace

from report2sqaaas_plugins_bandit.main import BanditValidator


@pytest.fixture
def bandit_stdout():
    # FIXME Return a sample tool's stdout as string
    return ""

@pytest.fixture
def validator_opts(bandit_stdout):
    class_args = {
        'validator': 'bandit',
        'stdout': bandit_stdout
    }
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return BanditValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert BanditValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert 'valid' in list(result)
    assert 'subcriteria' in list(result)
    assert type(result['subcriteria']) is list
    
