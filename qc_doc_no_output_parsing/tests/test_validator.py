import json
import pathlib
import pytest
from types import SimpleNamespace

from report2sqaaas_plugins_no_output_parsing.main import NoOutputParsingValidator


@pytest.fixture
def no_output_parsing_stdin(request):
    file = pathlib.Path(request.node.fspath.strpath)
    stdout = file.with_name('stdin.json')
    with stdout.open() as fp:
        json_data = json.load(fp)
        return json_data


@pytest.fixture
def validator_opts(no_output_parsing_stdin):
    class_args = {
        'validator': 'no_output_parsing',
        'stdin': no_output_parsing_stdin
    }
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return NoOutputParsingValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert NoOutputParsingValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert 'valid' in list(result)
    assert 'subcriteria' in list(result)
    assert type(result['subcriteria']) is list

