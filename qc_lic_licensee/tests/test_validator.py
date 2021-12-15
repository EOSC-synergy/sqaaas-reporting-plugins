import pytest
from types import SimpleNamespace

from report2sqaaas_plugins_licensee.main import LicenseeValidator


@pytest.fixture
def licensee_stdout():
    return """
    {
        "matched_files": []
    }
    """

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


def test_is_validate_method_defined(validator_opts):
    assert LicenseeValidator(validator_opts).validate()


def test_is_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert 'valid' in list(result)
