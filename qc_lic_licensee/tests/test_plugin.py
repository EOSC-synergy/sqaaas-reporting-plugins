import pytest
from types import SimpleNamespace

from report2sqaaas_plugins_licensee.main import LicenseeValidator


# fixture for <stdout>??
licensee_stdout = """
{
    "matched_files": []
}
"""

@pytest.fixture
def validator_opts():
    class_args = {
        'validator': 'licensee',
        'stdout': licensee_stdout
    }
    return SimpleNamespace(**class_args)


def test_is_validate_method_defined(validator_opts):
    try:
        LicenseeValidator(validator_opts).validate()
    except TypeError:
        pytest.fail('LicenseeValidator class does not implement validate() method')
