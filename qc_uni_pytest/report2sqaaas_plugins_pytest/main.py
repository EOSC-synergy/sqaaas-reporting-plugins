# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project <sqaaas@ibergrid.eu>
# SPDX-FileContributor: 2017-2024 Pablo Orviz <orviz@ifca.unican.es>
#
# SPDX-License-Identifier: GPL-3.0-only

import logging

from report2sqaaas import utils as sqaaas_utils

logger = logging.getLogger("sqaaas.reporting.plugins.pytest")


class PytestValidator(sqaaas_utils.BaseValidator):
    valid = False
