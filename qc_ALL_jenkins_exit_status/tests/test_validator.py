# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project <sqaaas@ibergrid.eu>
# SPDX-FileContributor: 2017-2024 Pablo Orviz <orviz@ifca.unican.es>
#
# SPDX-License-Identifier: GPL-3.0-only

from types import SimpleNamespace

import pytest
from report2sqaaas_plugins_jenkins_exit_status.main import \
    JenkinsExitStatusValidator


@pytest.fixture
def jenkins_exit_status_stdout():
    return "None"


@pytest.fixture
def validator_opts(jenkins_exit_status_stdout):
    class_args = {
        "validator": "jenkins_exit_status",
        "criterion": "SvcQC.Dep",
        "subcriterion": "SvcQC.Dep01",
        "status": "SUCCESS",
    }
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return JenkinsExitStatusValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert JenkinsExitStatusValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert "valid" in list(result)
    assert "subcriteria" in list(result)
    assert type(result["subcriteria"]) is list
