# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project <sqaaas@ibergrid.eu>
# SPDX-FileContributor: 2017-2024 Pablo Orviz <orviz@ifca.unican.es>
#
# SPDX-License-Identifier: GPL-3.0-only

from types import SimpleNamespace

import pytest
from report2sqaaas_plugins_boolean.main import BooleanValidator


@pytest.fixture
def boolean_stdout():
    return "False"


@pytest.fixture
def validator_opts(boolean_stdout):
    class_args = {
        "validator": "boolean",
        "stdout": boolean_stdout,
        "subcriterion": "QC.Met01",
    }
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return BooleanValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert BooleanValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert "valid" in list(result)
