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
    criterion = "QC.Sty"
    def validate(self):
        res = False
        criterion = "QC.Sty"
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
        for file_ in validation["passed_list"]:
            sub={}
            sub["id"]= file_
            sub["valid"]= True
            sub["description"]="Is workflow valid?"
            sub["evidence"]="According to Pyophidia tools workflow is valid"
            sub["hint"]=''
            subcriteria.append(sub)
            
        for file_index in range(len(validation["failed_list"])):
            sub={}
            sub["id"]= validation["failied_list"][file_index]
            sub["valid"]= False
            sub["description"]="Is workflow valid?"
            sub["evidence"]=validation["reasons_list"][file_index]
            sub["hint"]=''
            subcriteria.append(sub)
        return {
            "valid": res,
            "subcriteria": subcriteria,
            "standard": standard,
            "data_unstructured": data_unstructured,
        }
