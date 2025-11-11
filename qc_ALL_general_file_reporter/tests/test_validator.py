# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from types import SimpleNamespace

from report2sqaaas_plugins_general_file_reporter.main import GeneralFilesValidator


@pytest.fixture
def general_file_reporter_stdout():
    # FIXME Return a sample tool's stdout as string
    return ""


@pytest.fixture
def validator_opts(general_file_reporter_stdout):
    class_args = {
        'validator': 'general_file_reporter',
        'stdout': general_file_reporter_stdout
    }
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return GeneralFilesValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert GeneralFilesValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert 'valid' in list(result)
    assert 'subcriteria' in list(result)
    assert type(result['subcriteria']) is list
