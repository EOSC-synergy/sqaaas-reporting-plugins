# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from types import SimpleNamespace

from report2sqaaas_plugins_Ophidia.main import OphidiaValidator


@pytest.fixture
def Ophidia_stdout():
    # FIXME Return a sample tool's stdout as string
    return ""


@pytest.fixture
def validator_opts(Ophidia_stdout):
    class_args = {
        'validator': 'Ophidia',
        'stdout': Ophidia_stdout
    }
    return SimpleNamespace(**class_args)


@pytest.fixture
def validator(validator_opts):
    return OphidiaValidator(validator_opts)


@pytest.mark.dependency()
def test_is_validate_method_defined(validator_opts):
    assert OphidiaValidator(validator_opts).validate()


@pytest.mark.dependency(depends=["test_is_validate_method_defined"])
def test_validate_method_output(validator):
    result = validator.validate()
    assert type(result) is dict
    assert 'valid' in list(result)
