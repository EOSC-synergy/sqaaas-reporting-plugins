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
        lang_name = self.opts.lang_name if hasattr(self.opts, "lang_name") else None
        tool_name = self.opts.tool_name if hasattr(self.opts, "tool_name") else None
        standard_kwargs = {"lang_name": lang_name, "tool_name": tool_name}
        logger.debug("Standard keywords generated: %s" % standard_kwargs)
        standard = {}#self.standard
        data_unstructured = {
            "passed": validation["passed_list"],
            "failed": validation["failed_list"],
            "reasons_passed": validation["passed_reasons_list"],
            "reasons_failed": validation["failed_reasons_list"],
        }
        print('reporter32')
        print(validation.keys())
        print(validation['subcriterion'])
        subcriteria=validation['subcriterion']
        final_product={
            "valid": res,
            "subcriteria": subcriteria,
            "standard": standard,
            "data_unstructured": data_unstructured,
        }
        print('reporter39')
        print(standard)
        print(validation['subcriterion'])
        print(final_product['subcriteria'])
        return (final_product)
