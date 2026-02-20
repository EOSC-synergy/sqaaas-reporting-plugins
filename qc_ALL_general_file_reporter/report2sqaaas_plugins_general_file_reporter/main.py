# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import json

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.general_file_reporter')


class GeneralFilesValidator(sqaaas_utils.BaseValidator):
    valid = False
    
    
    def validate(self):
        res = False
        validation = json.loads(sqaaas_utils.load_data(self.opts.stdout.strip()))

        if validation["result"]:
            res = True
        subcriteria =  [{'id': 'QC.Sty01', 'description': 'Is the software product following a style standard for notebook files?', 'hint': 'Please check & solve the security weaknesses found by the linter tool', 'valid': True, 'evidence': 'Python files are compliant with flake8 (pycodestyle, pyflakes, mccabe) standard', 'requirement_level': 'RECOMMENDED'}]
        standard = {}
        data_unstructured = {
            "passed": validation["passed_list"],
            "failed": validation["failed_list"],
            "reasons_passed": validation["passed_reasons_list"],
            "reasons_failed": validation["failed_reasons_list"],
        }
        
        final_product={
            "valid": res,
            "subcriteria": subcriteria,
            "standard": standard,
            "data_unstructured": data_unstructured,
        }
        print('reporter39')
        print(final_product['subcriteria'])
        return (final_product)
