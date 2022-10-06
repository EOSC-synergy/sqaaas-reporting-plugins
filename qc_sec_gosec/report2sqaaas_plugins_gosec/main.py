import logging
import re

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.gosec')


class GoSecValidator(sqaaas_utils.BaseValidator):
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
        criterion = 'QC.Sec'
        criterion_data = sqaaas_utils.load_criterion_from_standard(
            criterion
        )
        subcriteria = []
        try:
            data = sqaaas_utils.load_json(self.opts.stdout)
            logger.debug('Parsing output: %s' % data)
        except ValueError:
            data = {}
            logger.error('Input data does not contain a valid JSON')
        else:
            subcriterion = 'QC.Sec02'
            subcriterion_data = criterion_data[subcriterion]
            subcriterion_valid = False
            evidence = None
            if len(data['Issues']) > 0:
                subcriterion_valid = False
                evidence = subcriterion_data['evidence']['failure']
                logger.warning((
                    'Gosec found %s high rated security '
                    'issues' % len(data['Issues'])
                ))
            else:
                evidence = subcriterion_data['evidence']['success']
                logger.info(evidence)
            evidence = evidence % self.opts.tool_name

            requirement_level = subcriterion_data['requirement_level']
            subcriteria.append({
                'id': subcriterion,
                'description': subcriterion_data['description'],
                'hint': subcriterion_data['hint'],
                'valid': subcriterion_valid,
                'evidence': evidence,
                'requirement_level': requirement_level
            })

            self.valid = subcriterion_valid
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
