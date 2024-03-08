# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project <sqaaas@ibergrid.eu>
# SPDX-FileContributor: 2017-2024 Pablo Orviz <orviz@ifca.unican.es>
#
# SPDX-License-Identifier: GPL-3.0-only

import json
import pathlib
from types import SimpleNamespace

import pytest
from report2sqaaas_plugins_fuji.main import FujiValidator


@pytest.fixture
def fuji_stdout(request):
    file = pathlib.Path(request.node.fspath.strpath)
    stdout = file.with_name("fuji.out.json")
    with stdout.open() as fp:
        json_data = json.load(fp)
        return json.dumps(json_data)


@pytest.fixture
def validator_opts(fuji_stdout):
    class_args = {"validator": "fuji", "stdout": fuji_stdout}
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return FujiValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert FujiValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert "valid" in list(result)
    assert "subcriteria" in list(result)
    assert type(result["subcriteria"]) is list
