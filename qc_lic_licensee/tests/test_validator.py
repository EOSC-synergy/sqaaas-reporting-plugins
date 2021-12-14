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
def validator(licensee_stdout):
    class_args = {
        'validator': 'licensee',
        'stdout': licensee_stdout
    }
    opts = SimpleNamespace(**class_args)
    return LicenseeValidator(opts)


def test_is_validate_method_defined(validator):
    try:
        validator.validate()
    except TypeError:
        pytest.fail('LicenseeValidator class does not implement validate() method')


def test_is_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert 'valid' in list(result)
