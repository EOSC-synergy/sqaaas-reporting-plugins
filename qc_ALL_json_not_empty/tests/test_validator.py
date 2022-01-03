import pytest
from types import SimpleNamespace

from report2sqaaas_plugins_json_not_empty.main import JsonNotEmptyValidator


@pytest.fixture
def json_not_empty_stdout():
    return """{"foo": "bar"}"""

@pytest.fixture
def validator_opts(json_not_empty_stdout):
    class_args = {
        'validator': 'json_not_empty',
        'stdout': json_not_empty_stdout
    }
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return JsonNotEmptyValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert JsonNotEmptyValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert 'valid' in list(result)
