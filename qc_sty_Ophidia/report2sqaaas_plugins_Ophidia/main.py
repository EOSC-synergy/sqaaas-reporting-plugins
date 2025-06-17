# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import logging

from report2sqaaas import utils as sqaaas_utils

logger = logging.getLogger("sqaaas.reporting.plugins.Ophidia")


class OphidiaValidator(sqaaas_utils.BaseValidator):
    valid = False
    threshold = 1

    def validate(self):
        res = False
        validation = json.loads(sqaaas_utils.load_data(self.opts.stdout.strip()))

        if validation["result"]:
            res = True
        subcriteria = []
        standard = {}
        data_unstructured = {
            "passed": validation["passed_list"],
            "failed": validation["failed_list"],
            "reasons": validation["reasons_list"],
        }

        return {
            "valid": res,
            "subcriteria": subcriteria,
            "standard": standard,
            "data_unstructured": data_unstructured,
        }
