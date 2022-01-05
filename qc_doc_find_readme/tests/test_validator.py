import pytest
from types import SimpleNamespace

from report2sqaaas_plugins_find_readme.main import FindReadmeValidator


@pytest.fixture
def find_readme_stdout():
    # FIXME Return a sample tool's stdout as string
    return """
    [
        {
            'README.md': {
                'size': 280
            }
        }
    ]
    """

@pytest.fixture
def validator_opts(find_readme_stdout):
    class_args = {
        'validator': 'find_readme',
        'stdout': find_readme_stdout
    }
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return FindReadmeValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert FindReadmeValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert 'valid' in list(result)
