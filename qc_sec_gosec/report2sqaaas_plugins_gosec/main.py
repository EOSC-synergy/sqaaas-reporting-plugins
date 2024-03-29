# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project <sqaaas@ibergrid.eu>
# SPDX-FileContributor: 2017-2024 Pablo Orviz <orviz@ifca.unican.es>
#
# SPDX-License-Identifier: GPL-3.0-only

import logging

from report2sqaaas import utils as sqaaas_utils

logger = logging.getLogger("sqaaas.reporting.plugins.gosec")


class GoSecValidator(sqaaas_utils.BaseValidator):
    valid = False
    standard = {
        "title": (
            "A set of Common Software Quality Assurance Baseline Criteria for "
            "Research Projects"
        ),
        "version": "v4.0",
        "url": "https://github.com/indigo-dc/sqa-baseline/releases/tag/v4.0",
    }

    def validate(self):
        criterion = "QC.Sec"
        criterion_data = sqaaas_utils.load_criterion_from_standard(criterion)
        subcriteria = []
        standard_kwargs = {"lang_name": "Go", "tool_name": "gosec"}

        try:
            data = sqaaas_utils.load_json(self.opts.stdout)
            logger.debug("Parsing output: %s" % data)
        except ValueError:
            data = {}
            logger.error("Input data does not contain a valid JSON")
        else:
            subcriterion = "QC.Sec02"
            subcriterion_data = criterion_data[subcriterion]
            subcriterion_valid = False
            evidence = None
            if len(data["Issues"]) > 0:
                subcriterion_valid = False
                evidence = subcriterion_data["evidence"]["failure"]
                logger.warning(
                    (
                        "Gosec found %s high rated security "
                        "issues" % len(data["Issues"])
                    )
                )
            else:
                evidence = subcriterion_data["evidence"]["success"]
                logger.info(evidence)
            evidence = evidence.format(**standard_kwargs)

            requirement_level = subcriterion_data["requirement_level"]
            subcriteria.append(
                {
                    "id": subcriterion,
                    "description": subcriterion_data["description"].format(
                        **standard_kwargs
                    ),
                    "hint": subcriterion_data["hint"],
                    "valid": subcriterion_valid,
                    "evidence": evidence,
                    "requirement_level": requirement_level,
                }
            )

            self.valid = subcriterion_valid
            if (not subcriterion_valid) and (requirement_level in ["MUST"]):
                self.valid = False

        return {
            "valid": self.valid,
            "subcriteria": subcriteria,
            "standard": self.standard,
            "data_unstructured": data,
        }
