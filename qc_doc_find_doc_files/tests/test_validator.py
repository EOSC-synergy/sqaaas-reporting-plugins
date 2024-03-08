import json
import pathlib
from types import SimpleNamespace

import pytest
from report2sqaaas_plugins_find_doc_files.main import FindDocFilesValidator


@pytest.fixture
def find_doc_files_stdout(request):
    file = pathlib.Path(request.node.fspath.strpath)
    stdout = file.with_name("find_doc_files.out.json")
    with stdout.open() as fp:
        json_data = json.load(fp)
        return json.dumps(json_data)


@pytest.fixture
def validator_opts(find_doc_files_stdout):
    class_args = {"validator": "find_doc_files", "stdout": find_doc_files_stdout}
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return FindDocFilesValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert FindDocFilesValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert "valid" in list(result)
