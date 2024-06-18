# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import re

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger("sqaaas.reporting.plugins.goblint")


class goblintValidator(sqaaas_utils.BaseValidator):
    valid = True
    threshold = 1

    def validate(self):

        valid = False
        data = sqaaas_utils.load_data(self.opts.stdout.strip())

        clean = []
        categories = []
        lines = data.splitlines()
        race = 0
        race_evidence = "The memory locations evaluation has not been realised"
        code = 0
        code_evidence = "The lines of code  evaluation has not been realised"
        for line in lines:

            remove1 = line.replace("\x1b[0;34m", "")
            remove2 = remove1.replace("\u001b[0;0;00m", "")
            if not (line == remove1 or remove1 == remove2):
                clean.append(remove2)

        for i in range(len(clean)):
            line = clean[i]
            if line[:6] == "[Info]":
                categories.append(i)

        for i in categories:
            if "Deadcode" in clean[i]:
                numbers = [
                    int(s)
                    for s in re.findall(
                        r"\b\d+\b", clean[i + 1] + clean[i + 2] + clean[i + 3]
                    )
                ]
                # dead=(str(clean[i+1]+','+clean[i+2]+','+clean[i+3]))
                if (
                    numbers[0] == numbers[2]
                ):  # numbers[0] is the number of live lines and numbers[2] the total number of lines
                    code = True
                    code_evidence = (
                        "The number of live lines is equal to the total number of lines"
                    )
                else:
                    code_evidence = "The number of live lines is not equal to the total number of lines"
            if "Race" in clean[i]:
                numbers = [
                    int(s)
                    for s in re.findall(
                        r"\b\d+\b",
                        clean[i + 1] + clean[i + 2] + clean[i + 3] + clean[i + 4],
                    )
                ]
                if (
                    numbers[0] == numbers[3]
                ):  # numbers[0] is the number of safe memory locations and numbers[3] the total memory locations
                    race = True
                    race_evidence = "The number of safe memory locations is equal to the total number of memory locations"
                else:
                    race_evidence = "The number of safe memory locations is not equal to the total number of memory locations"

        if race == True and code == True:
            valid = True

        subcriteria = [
            {
                "id": "QC.Sec",
                "valid": race,
                "description": "Memory locations race safety",
                "evidence": race_evidence,
            },
            {
                "id": "QC.Sec",
                "valid": code,
                "description": "Logical lines of code",
                "evidence": code_evidence,
            },
        ]
        return {
            "valid": valid,
            "subcriteria": subcriteria,
            "standard": "",
            "data_unstructured": [race_evidence, code_evidence],
        }
