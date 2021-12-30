import pytest
from types import SimpleNamespace

from report2sqaaas_plugins_markdownlint.main import MarkdownLintValidator


@pytest.fixture
def markdownlint_stdout():
    # FIXME Return a sample tool's stdout as string
    return ""

@pytest.fixture
def validator_opts(markdownlint_stdout):
    class_args = {
        'validator': 'markdownlint',
        'stdout': markdownlint_stdout
    }
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return MarkdownLintValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert MarkdownLintValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert 'valid' in list(result)
