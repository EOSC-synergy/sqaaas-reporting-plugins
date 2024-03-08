import logging

import semver
from report2sqaaas import utils as sqaaas_utils

logger = logging.getLogger("sqaaas.reporting.plugins.is_semver")


class IsSemverValidator(sqaaas_utils.BaseValidator):
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
        """Expects a list of Git tags ordered by creation time (from more
        recent to older)"""
        criterion = "QC.Ver"
        criterion_data = sqaaas_utils.load_criterion_from_standard(criterion)
        subcriteria = []
        subcriteria_validity = {}
        standard_kwargs = {}
        has_release_tags = False
        latest_tag = None
        tags_semver = {}  # semver-compliance for tags

        try:
            # FIXME Do this at sqaaas_utils.load_json
            new_stdout = self.opts.stdout.replace("'", '"')
            data = sqaaas_utils.load_json(new_stdout)
            logger.debug("Parsing output: %s" % data)
        except ValueError:
            data = {}
            logger.error("Input data does not contain a valid JSON")
        else:
            if data:
                has_release_tags = True
                # Check QC.Ver01 & QC.Ver02
                latest_tag = data[0]  # expects latest tag on first element
                for tag in data:
                    # is semver?
                    _is_tag_semver = False
                    if semver.VersionInfo.isvalid(tag):
                        _is_tag_semver = True
                    tags_semver[tag] = _is_tag_semver

        standard_kwargs["latest_tag"] = latest_tag

        # QC.Ver01.0: uses tags for releases
        # QC.Ver01: latest tag is semver
        # QC.Ver02: all tags are semver
        subcriteria_validity["QC.Ver01.0"] = has_release_tags
        subcriteria_validity["QC.Ver01"] = tags_semver.get(latest_tag, False)
        subcriteria_validity["QC.Ver02"] = all(tags_semver.values())

        must_subcriteria = []
        for subcriterion in ["QC.Ver01.0", "QC.Ver01", "QC.Ver02"]:
            subcriterion_data = criterion_data[subcriterion]
            _valid = subcriteria_validity[subcriterion]

            evidence_data = subcriterion_data["evidence"]
            if _valid:
                evidence = evidence_data["success"]
            else:
                evidence = evidence_data["failure"]

            requirement_level = subcriterion_data["requirement_level"]
            subcriteria.append(
                {
                    "id": subcriterion,
                    "description": subcriterion_data["description"],
                    "hint": subcriterion_data["hint"],
                    "valid": _valid,
                    "evidence": evidence.format(**standard_kwargs),
                    "requirement_level": requirement_level,
                }
            )

            if requirement_level in ["MUST"]:
                must_subcriteria.append(_valid)

        self.valid = all(must_subcriteria)
        logger.debug(subcriteria)
        return {
            "valid": self.valid,
            "subcriteria": subcriteria,
            "standard": self.standard,
            "data_unstructured": data,
        }
