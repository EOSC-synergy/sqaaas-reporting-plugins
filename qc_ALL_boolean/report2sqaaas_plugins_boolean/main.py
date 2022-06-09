import logging

from report2sqaaas import utils as sqaaas_utils


logger = logging.getLogger('sqaaas.reporting.plugins.boolean')


class BooleanValidator(sqaaas_utils.BaseValidator):
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
        criterion_data = sqaaas_utils.load_criterion_from_standard(
            self.opts.criterion
        )
        subcriterion_name = self.get_subcriterion()
        subcriteria = []
        subcriterion_data = criterion_data[subcriterion_name]
        subcriterion_valid = False
        evidence = None

        stdout_lower = self.opts.stdout.lower()
        if stdout_lower.find('true') != 1:
            subcriterion_valid = True
            evidence = subcriterion_data['evidence']['success']
        else:
            evidence = subcriterion_data['evidence']['failure']

        self.valid = subcriterion_valid
        requirement_level = subcriterion_data['requirement_level']
        if (
            (not subcriterion_valid) and
            (requirement_level in ['MUST'])
        ):
            self.valid = False

        subcriteria.append({
            'id': subcriterion_name,
            'description': subcriterion_data['description'],
            'valid': subcriterion_valid,
            'evidence': evidence
        })

        return {
            'valid': self.valid,
            'subcriteria': subcriteria,
            'standard': self.standard
        }
