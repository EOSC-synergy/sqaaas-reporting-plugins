# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project <sqaaas@ibergrid.eu>
# SPDX-FileContributor: 2017-2024 Pablo Orviz <orviz@ifca.unican.es>
#
# SPDX-License-Identifier: GPL-3.0-only

from types import SimpleNamespace

import pytest
from report2sqaaas_plugins_pytest.main import PytestValidator


@pytest.fixture
def pytest_stdout():
    # FIXME Return a sample tool's stdout as string
    return ""


@pytest.fixture
def validator_opts(pytest_stdout):
    class_args = {"validator": "pytest", "stdout": pytest_stdout}
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return PytestValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert PytestValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert "valid" in list(result)
