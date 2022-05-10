import logging
import json
import semver

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.is_semver')


class IsSemverValidator(sqaaas_utils.BaseValidator):
    valid = False
    standard = {
        'title': (
            'A set of Common Software Quality Assurance Baseline Criteria for '
            'Research Projects'
        ),
        'version': 'v4.0',
        'url': 'https://github.com/indigo-dc/sqa-baseline/releases/tag/v4.0',
    }

    def validate(self):
        criterion = 'QC.Ver'
        criterion_data = sqaaas_utils.load_criterion_from_standard(
            criterion
        )
        subcriteria = []

        subcriterion = 'QC.Ver01'
        subcriterion_data = criterion_data[subcriterion]
        subcriterion_valid = False
        evidence = None
        has_release_tag = False

        try:
            data = sqaaas_utils.load_json(self.opts.stdout)
            logger.debug('Parsing output: %s' % data)
        except ValueError:
            data = {}
            logger.error('Input data does not contain a valid JSON')
        else:
            if data:
                has_release_tag = True
                latest_tag = data[0]
                for tag in data:
                    if semver.VersionInfo.isvalid(tag):
                        subcriterion_valid = True
                        if semver.compare(latest_tag, tag) < 0:
                            latest_tag = tag

        if subcriterion_valid:
            evidence = subcriterion_data['evidence']['success'] % latest_tag
        else:
            if has_release_tag:
                evidence = subcriterion_data['evidence']['failure'] % latest_tag
            else:
                evidence = subcriterion_data['evidence']['failure_no_tag']

        subcriteria.append({
            'id': subcriterion,
            'description': subcriterion_data['description'],
            'valid': subcriterion_valid,
            'evidence': evidence
        })

        self.valid = subcriterion_valid
        requirement_level = subcriterion_data['requirement_level']
        if (
            (not subcriterion_valid) and
            (requirement_level in ['MUST'])
        ):
            self.valid = False

        return {
            'valid': self.valid,
            'subcriteria': subcriteria,
            'standard': self.standard,
            'data_unstructured': data
        }
